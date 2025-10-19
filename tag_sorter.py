"""
ComfyUI Custom Node: Tag Sorter
Версія: 4.3 - Покращено надійність парсингу JSON для уникнення помилок.
Version: 4.3 - Improved JSON parsing reliability to prevent errors.
"""

import sys
import os
import json
import subprocess
import importlib.metadata
import re
from typing import Tuple, Dict, List, Optional, Any

# Менеджер залежностей \\ Dependency Manager
def install_package(command: list) -> bool:
    try:
        print(f"    -> Running command: {' '.join(command)}")
        full_command = [sys.executable, "-m"] + command
        subprocess.run(full_command, check=True, capture_output=True, text=True, encoding='utf-8')
        print(f"    -> Command successful.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"    -> [COMMAND FAILED]. Error: {e.stderr[:1000]}...")
        return False

def manage_dependencies() -> Dict:
    print("─" * 50)
    print("### Smart Deps Manager: Tag Sorter ###")
    issues = {"errors": [], "restart_needed": False}

    try:
        importlib.metadata.version("llama-cpp-python")
        print("  - [✅ OK] llama-cpp-python is installed.")
    except importlib.metadata.PackageNotFoundError:
        print("  - [⚠️ WARN] llama-cpp-python not found. Starting one-time setup process...")
        issues["restart_needed"] = True

        req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
        if not os.path.exists(req_path):
            issues["errors"].append("requirements.txt not found!")
            return issues

        print("\n  Step 1: Installing build tools...")
        if not install_package(["pip", "install", "-r", req_path]):
            issues["errors"].append("Failed to install build tools from requirements.txt.")
            return issues

        print("\n  Step 2: Installing llama-cpp-python with CUDA support...")
        try:
            env = os.environ.copy()
            env['CMAKE_ARGS'] = "-DLLAMA_CUBLAS=on"
            command = [sys.executable, "-m", "pip", "install", "llama-cpp-python"]
            subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8', env=env)
            print("    -> Successfully compiled and installed llama-cpp-python with CUDA support!")
        except subprocess.CalledProcessError as e:
            error_msg = "Failed to compile llama-cpp-python with CUDA. Check NVIDIA CUDA Toolkit installation."
            print(f"    -> [FATAL ERROR] {error_msg}")
            print(f"    -> Error: {e.stderr[:1000]}...")
            issues["errors"].append(error_msg)

    if issues["restart_needed"] and not issues["errors"]:
        issues["errors"].append("One-time setup is complete. PLEASE RESTART COMFYUI.")

    if not issues["errors"]:
        print("### All dependencies are OK. ###")
    print("─" * 50)
    return issues

dependency_issues = manage_dependencies()

# Main Node Code
try:
    from llama_cpp import Llama
    from huggingface_hub import hf_hub_download
except ImportError:
    pass

# Глобальна конфігурація \\ Global Configuration
CACHED_MODELS: Dict[str, "Llama"] = {}
NODE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(NODE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

class TagSorter:
    MODEL_LIST: Dict[str, Dict] = {
        "Hermes-2-Pro-Llama-3-8B LowCensored": {
            "repo": "NousResearch/Hermes-2-Pro-Llama-3-8B-GGUF",
            "file": "Hermes-2-Pro-Llama-3-8B-Q4_K_M.gguf"
        }
    }

    def __init__(self):
        self.issues = dependency_issues
        self.task_instruction = self.load_instruction()

    def load_instruction(self) -> str:
        try:
            config_path = os.path.join(NODE_DIR, "prompt_config.json")
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            instruction = config.get("task_instruction", "")
            print("### TagSorter: Config loaded from prompt_config.json.")
            return instruction
        except Exception as e:
            print(f"### TagSorter: Using default instruction. Error loading config: {e}")
            return """Analyze the input tags... (Ваша інструкція)""" # Скорочено для прикладу

    @classmethod
    def INPUT_TYPES(cls) -> Dict:
        return {
            "required": {
                "raw_tags": ("STRING", {"multiline": True, "default": "Paste tags here..."}),
                "model_name": (list(cls.MODEL_LIST.keys()), {"default": "Nous Hermes 2 Pro (Llama-3 8B)"}),
                "gpu_layers": ("INT", {"default": -1, "min": -1, "max": 999}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("character", "clothing", "location", "enhancement")
    FUNCTION = "sort_tags"
    CATEGORY = "Prompting"

    def load_model(self, model_info: Dict, gpu_layers: int) -> Optional[Llama]:
        repo_id, filename = model_info["repo"], model_info["file"]
        cache_key = f"{repo_id}/{filename}"

        if cache_key in CACHED_MODELS:
            print("### TagSorter: Using cached model.")
            return CACHED_MODELS[cache_key]

        local_model_path = os.path.join(MODELS_DIR, filename)

        if not os.path.exists(local_model_path):
            print(f"### TagSorter: Downloading model '{filename}'...")
            try:
                hf_hub_download(
                    repo_id=repo_id,
                    filename=filename,
                    local_dir=MODELS_DIR,
                    local_dir_use_symlinks=False
                )
                print(f"### TagSorter: Model downloaded successfully.")
            except Exception as e:
                error_str = str(e)
                if any(err_code in error_str for err_code in ["401", "404", "Repository Not Found"]):
                    return f"[❌ ERROR] Model not found: '{repo_id}/{filename}'. Check MODEL_LIST."
                return f"FATAL: Could not download model '{filename}'. Error: {e}"

        try:
            print(f"### TagSorter: Loading model into memory...")
            model = Llama(
                model_path=local_model_path,
                n_gpu_layers=gpu_layers,
                n_ctx=8192,
                verbose=False
            )
            CACHED_MODELS[cache_key] = model
            print("### TagSorter: Model loaded successfully.")
            return model
        except Exception as e:
            return f"FATAL: Could not load model. Error: {e}"

    def clean_json_response(self, text: str) -> str:
        try:
            start_brace_index = text.find('{')
            if start_brace_index == -1: return ""
            brace_count = 0
            end_brace_index = -1
            for i, char in enumerate(text[start_brace_index:]):
                if char == '{': brace_count += 1
                elif char == '}': brace_count -= 1
                if brace_count == 0:
                    end_brace_index = start_brace_index + i
                    break
            if end_brace_index != -1:
                return text[start_brace_index : end_brace_index + 1]
            else: return ""
        except Exception: return ""

    def parse_llm_response(self, response_text: str) -> Dict:
        cleaned_json = self.clean_json_response(response_text)
        if not cleaned_json:
            print("### TagSorter: No valid JSON block found, using fallback parser.")
            return self.fallback_parse(response_text)
        try:
            data = json.loads(cleaned_json)
            for key in ["character", "clothing", "location", "enhancement"]:
                data.setdefault(key, [])
            return data
        except json.JSONDecodeError:
            print("### TagSorter: JSON decode failed after cleaning, using fallback parser.")
            return self.fallback_parse(response_text)

    def fallback_parse(self, text: str) -> Dict:
        result = {"character": [], "clothing": [], "location": [], "enhancement": []}
        lines = text.split('\n')
        current_category = None
        for line in lines:
            line = line.strip().lower()
            if 'character' in line: current_category = "character"
            elif 'clothing' in line or 'clothes' in line: current_category = "clothing"
            elif 'location' in line or 'background' in line: current_category = "location"
            elif 'enhancement' in line or 'quality' in line: current_category = "enhancement"
            elif current_category and line and not line.startswith(('{', '}', '[', ']')):
                tags = [tag.strip() for tag in line.split(',') if tag.strip()]
                result[current_category].extend(tags)
        return result

    def sort_tags(self, raw_tags: str, model_name: str, gpu_layers: int, **kwargs) -> Tuple[str, ...]:
        max_tokens = 800
        temperature = 0.0
        print(f"### TagSorter: Parameters (hardcoded) - max_tokens={max_tokens}, temperature={temperature}")

        empty_result = ("", "", "", "")
        if not raw_tags or not raw_tags.strip() or raw_tags == "Paste tags here...":
            print("### TagSorter: Input is empty, ignoring.")
            # --- ЗМІНА 2: Повертаємо простий кортеж, а не словник з "ui" ---
            return empty_result

        if self.issues["errors"]:
            error_report = "ERROR: Cannot run. Issues:\n\n" + "\n".join([f"- {e}" for e in self.issues["errors"]])
            return (error_report,) + empty_result[1:]

        model_info = self.MODEL_LIST[model_name]
        model = self.load_model(model_info, gpu_layers)

        if isinstance(model, str):
            return (model,) + empty_result[1:]

        final_prompt = f"{self.task_instruction}\n\nInput: '{raw_tags}'\nOutput:"

        try:
            print("### TagSorter: Generating response...")
            response = model(
                prompt=final_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=[],
                echo=False
            )

            llm_output = response['choices'][0]['text'].strip()
            print("--- RAW LLM OUTPUT ---\n", ll_output, "\n--- END RAW LL-M OUTPUT ---")
            print(f"### TagSorter: LLM response received ({len(ll_output)} chars)")

            sorted_tags_dict = self.parse_llm_response(ll_output)

            char_tags = ", ".join(sorted_tags_dict.get("character", []))
            cloth_tags = ", ".join(sorted_tags_dict.get("clothing", []))
            loc_tags = ", ".join(sorted_tags_dict.get("location", []))
            enhance_tags = ", ".join(sorted_tags_dict.get("enhancement", []))

            print("### TagSorter: Tags sorted successfully.")
            result_tuple = (char_tags, cloth_tags, loc_tags, enhance_tags)

            return result_tuple

        except Exception as e:
            error_msg = f"ERROR during tag sorting: {e}"
            print(error_msg)
            return (error_msg,) + empty_result[1:]

if 'llama_cpp' in sys.modules:
    NODE_CLASS_MAPPINGS = {"TagSorterNode": TagSorter}
    NODE_DISPLAY_NAME_MAPPINGS = {"TagSorterNode": "Tag Sorter ✨"}
else:
    NODE_CLASS_MAPPINGS = {}
    NODE_DISPLAY_NAME_MAPPINGS = {}