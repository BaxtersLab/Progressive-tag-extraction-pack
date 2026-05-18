import re

_STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "has", "have",
    "that", "this", "it", "its", "not", "be", "as", "into", "over", "out",
}


class PromptTagComparatorNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": ""}),
                "extracted_tags": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("missing_tags", "emergent_tags")
    FUNCTION = "compare"
    CATEGORY = "progressive_tags"

    def compare(self, prompt, extracted_tags):
        prompt_words = {
            w for w in re.findall(r"\b\w{3,}\b", prompt.lower())
            if w not in _STOP_WORDS
        }
        tag_set = {
            t.strip().lower()
            for t in re.split(r"[,\n;]+", extracted_tags)
            if len(t.strip()) > 1
        }

        # concepts in prompt not represented in any extracted tag
        missing = {w for w in prompt_words if not any(w in t or t in w for t in tag_set)}
        # tags that don't correspond to any prompt word
        emergent = {t for t in tag_set if not any(w in t or t in w for w in prompt_words)}

        return (", ".join(sorted(missing)), ", ".join(sorted(emergent)))
