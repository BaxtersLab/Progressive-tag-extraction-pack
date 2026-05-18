import re


class TagArbiterNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "semantic_tags": ("STRING", {"default": ""}),
                "style_tags": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("unified_tags",)
    FUNCTION = "arbitrate"
    CATEGORY = "progressive_tags"

    def arbitrate(self, semantic_tags, style_tags):
        def parse(s):
            return set(t.strip().lower() for t in re.split(r"[,\n;]+", s) if len(t.strip()) > 1)

        unified = parse(semantic_tags) | parse(style_tags)
        return (", ".join(sorted(unified)),)
