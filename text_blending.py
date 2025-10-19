"""
ComfyUI Custom Node: TextBlending
Версія: 1.1 - Оновлено назви входів та виходу.
\\\ Version: 1.1 - Updated input and output names.
"""
import re


class TokenBlending:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "unit_spec": ("STRING", {"default": ""}),
                "eyes_hair": ("STRING", {"default": ""}),
                "body_details_pose": ("STRING", {"default": ""}),
                "clothing": ("STRING", {"default": ""}),
                "background": ("STRING", {"default": ""}),
                "add_details": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("blended_text",)
    FUNCTION = "process"
    CATEGORY = "Custom/TextBlending"

    def process(self, unit_spec, eyes_hair, body_details_pose, clothing, background, add_details):
        inputs = [
            unit_spec,
            eyes_hair,
            body_details_pose,
            clothing,
            background,
            add_details,
        ]

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