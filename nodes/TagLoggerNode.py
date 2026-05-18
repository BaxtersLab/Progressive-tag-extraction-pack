import json
import re
from datetime import datetime
from pathlib import Path

_LOG_DIR = Path(__file__).parent.parent / "logs"


class TagLoggerNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_path": ("STRING", {"default": ""}),
                "prompt": ("STRING", {"default": ""}),
                "semantic_tags": ("STRING", {"default": ""}),
                "style_tags": ("STRING", {"default": ""}),
                "missing_tags": ("STRING", {"default": ""}),
                "emergent_tags": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "log"
    CATEGORY = "progressive_tags"
    OUTPUT_NODE = True

    def log(self, image_path, prompt, semantic_tags, style_tags, missing_tags, emergent_tags):
        def split_tags(s):
            return [t.strip() for t in re.split(r"[,\n;]+", s) if t.strip()]

        _LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = _LOG_DIR / "tags.jsonl"

        entry = {
            "image": image_path,
            "prompt": prompt,
            "semantic_tags": split_tags(semantic_tags),
            "style_tags": split_tags(style_tags),
            "missing_tags": split_tags(missing_tags),
            "emergent_tags": split_tags(emergent_tags),
            "timestamp": datetime.now().isoformat(),
        }

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

        return {"ui": {"text": [
            f"Logged to {log_file} | missing: {len(entry['missing_tags'])} | emergent: {len(entry['emergent_tags'])}"
        ]}}
