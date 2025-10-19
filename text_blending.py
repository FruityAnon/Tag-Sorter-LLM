"""
ComfyUI Custom Node: TextBlending
Версія: 1.1 - Оновлено назви входів та виходу.
\\\ Version: 1.1 - Updated input and output names.
"""
import re


class TokenBlending:
    # --- ПОЧАТОК ЗМІН 1 --- \\\ START OF CHANGES 1 ---
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Назви змінено на валідні імена змінних
                # \\\ Names changed to valid variable names
                "Unit_spec": ("STRING", {"default": ""}),
                "Eyes_Hair": ("STRING", {"default": ""}),
                "Body_details_Pose": ("STRING", {"default": ""}),
                "Clothing": ("STRING", {"default": ""}),
                "Background": ("STRING", {"default": ""}),
                "Add_details": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)

    # Додано назву для виходу
    # \\\ Added a name for the output
    RETURN_NAMES = ("Text Encode",)

    FUNCTION = "process"
    CATEGORY = "Custom/TextBlending"

    def process(self, unit_spec, eyes_hair, body_details_pose, clothing, background, add_details):
        # Список аргументів тепер відповідає INPUT_TYPES
        # \\\ The argument list now matches INPUT_TYPES
        inputs = [
            unit_spec,
            eyes_hair,
            body_details_pose,
            clothing,
            background,
            add_details,
        ]
        # --- КІНЕЦЬ ЗМІН 1 --- \\\ END OF CHANGES 1 ---

        blended = ""
        first_block_added = False
        for text in inputs:
            if text is None or not text.strip():
                continue
            text = text.strip()
            if not first_block_added:
                blended += text
                first_block_added = True
            else:
                blended += " BREAK, " + text

        return (blended,)

class TokenTextBlending:
    DISPLAY_NAME = "Token Text Blending"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "process"
    CATEGORY = "Custom/TextBlending"

    def process(self, text):
        if text is None:
            text = ""
        text = text.strip()
        return (text,)


class TokenTextPreview:
    DISPLAY_NAME = "Token Text Preview"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "process"
    CATEGORY = "Custom/TextBlending"

    def process(self, text):
        return ()

NODE_CLASS_MAPPINGS = {
    "TextBlending": TokenBlending,
    "TokenTextBlending": TokenTextBlending,
    "TokenTextPreview": TokenTextPreview
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextBlending": "Text Blending 📦",
    "TokenTextBlending": "Token Text Blending",
    "TokenTextPreview": "Token Text Preview"
}