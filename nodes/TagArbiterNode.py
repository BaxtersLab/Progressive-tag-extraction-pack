class TagArbiterNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"semantic_tags": ("STRING",), "style_tags": ("STRING",)} }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "arbitrate"
    CATEGORY = "tag_extraction"

    def arbitrate(self, semantic_tags, style_tags):
        # Merge and deduplicate
        sem_tags = set(tag.strip() for tag in semantic_tags.split(',') if tag.strip())
        sty_tags = set(tag.strip() for tag in style_tags.split(',') if tag.strip())
        unified_tags = sem_tags | sty_tags
        unified = ', '.join(sorted(unified_tags))
        return (unified,)