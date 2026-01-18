class PromptTagComparatorNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"prompt": ("STRING",), "extracted_tags": ("STRING",)} }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("missing_tags", "emergent_tags")
    FUNCTION = "compare"
    CATEGORY = "tag_extraction"

    def compare(self, prompt, extracted_tags):
        prompt_words = set(word.lower() for word in prompt.split() if len(word) > 2)
        tag_words = set(tag.lower() for tag in extracted_tags.split(',') if tag.strip())
        missing = prompt_words - tag_words
        emergent = tag_words - prompt_words
        missing_str = ', '.join(missing)
        emergent_str = ', '.join(emergent)
        return (missing_str, emergent_str)