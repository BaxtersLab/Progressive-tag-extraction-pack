import json
import os
from datetime import datetime

class TagLoggerNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"image_path": ("STRING",), "prompt": ("STRING",), "semantic_tags": ("STRING",), "style_tags": ("STRING",), "missing_tags": ("STRING",), "emergent_tags": ("STRING",)} }

    RETURN_TYPES = ()
    FUNCTION = "log"
    CATEGORY = "tag_extraction"
    OUTPUT_NODE = True

    def log(self, image_path, prompt, semantic_tags, style_tags, missing_tags, emergent_tags):
        log_entry = {
            "image": image_path,
            "prompt": prompt,
            "semantic_tags": semantic_tags.split(', ') if semantic_tags else [],
            "style_tags": style_tags.split(', ') if style_tags else [],
            "missing_tags": missing_tags.split(', ') if missing_tags else [],
            "emergent_tags": emergent_tags.split(', ') if emergent_tags else [],
            "timestamp": datetime.now().isoformat()
        }
        log_file = "tags.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        return ()