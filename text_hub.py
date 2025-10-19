"""
ComfyUI Custom Node: Text Hub
Версія: 1.0 - Універсальна нода для передачі та відображення тексту. \\\ Version: 1.0 - A universal node for transferring and displaying text.
"""
from typing import Tuple, Dict

class TextHub:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls) -> Dict:

        return {
            "required": {
                "text_1": ("STRING", {"multiline": True, "default": ""}),
                "text_2": ("STRING", {"multiline": True, "default": ""}),
                "text_3": ("STRING", {"multiline": True, "default": ""}),
                "text_4": ("STRING", {"multiline": True, "default": ""}),
                "text_5": ("STRING", {"multiline": True, "default": ""}),
                "text_6": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES: Tuple[str, ...] = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING",)

    RETURN_NAMES: Tuple[str, ...] = ("text_1", "text_2", "text_3", "text_4", "text_5", "text_6",)

    FUNCTION: str = "transfer"
    CATEGORY: str = "Prompting"

    def transfer(self, text_1: str, text_2: str, text_3: str, text_4: str, text_5: str, text_6: str) -> Tuple[str, ...]:

        return (text_1, text_2, text_3, text_4, text_5, text_6)

NODE_CLASS_MAPPINGS = {"TextHubNode": TextHub}
NODE_DISPLAY_NAME_MAPPINGS = {"TextHubNode": "Text Hub 📝"}