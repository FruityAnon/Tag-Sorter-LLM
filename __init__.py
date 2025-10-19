"""
ComfyUI Custom Nodes Package: Text Processing Nodes
Цей пакет містить кастомні ноди для обробки тексту в ComfyUI.
This package contains custom nodes for text processing in ComfyUI.

Включає наступні ноди:
- Text Blending: Змішування тексту з роздільниками BREAK
- Text Hub: Універсальна нода для передачі та відображення тексту
- Tag Sorter: Сортування тегів за категоріями з використанням LLM

Includes the following nodes:
- Text Blending: Text blending with BREAK separators
- Text Hub: Universal node for text transfer and display
- Tag Sorter: Tag sorting by categories using LLM
"""

from .text_blending import NODE_CLASS_MAPPINGS as TEXT_BLENDING_MAPPINGS
from .text_blending import NODE_DISPLAY_NAME_MAPPINGS as TEXT_BLENDING_DISPLAY_MAPPINGS

from .text_hub import NODE_CLASS_MAPPINGS as TEXT_HUB_MAPPINGS
from .text_hub import NODE_DISPLAY_NAME_MAPPINGS as TEXT_HUB_DISPLAY_MAPPINGS

from .tag_sorter import NODE_CLASS_MAPPINGS as TAG_SORTER_MAPPINGS
from .tag_sorter import NODE_DISPLAY_NAME_MAPPINGS as TAG_SORTER_DISPLAY_MAPPINGS

NODE_CLASS_MAPPINGS = {**TEXT_BLENDING_MAPPINGS, **TEXT_HUB_MAPPINGS, **TAG_SORTER_MAPPINGS}

NODE_DISPLAY_NAME_MAPPINGS = {**TEXT_BLENDING_DISPLAY_MAPPINGS, **TEXT_HUB_DISPLAY_MAPPINGS, **TAG_SORTER_DISPLAY_MAPPINGS}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']