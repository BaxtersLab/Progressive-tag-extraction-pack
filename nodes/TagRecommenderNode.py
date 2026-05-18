import json
from collections import Counter
from pathlib import Path

_LOG_FILE = Path(__file__).parent.parent / "logs" / "tags.jsonl"


class TagRecommenderNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "log_file": ("STRING", {"default": str(_LOG_FILE)}),
                "top_n": ("INT", {"default": 10, "min": 1, "max": 50}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("recommended_tags",)
    FUNCTION = "recommend"
    CATEGORY = "progressive_tags"

    def recommend(self, log_file, top_n):
        path = Path(log_file)
        if not path.exists():
            return ("No log file found. Run the full pipeline first.",)

        all_tags = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    all_tags.extend(entry.get("semantic_tags", []))
                    all_tags.extend(entry.get("style_tags", []))
                except json.JSONDecodeError:
                    continue

        if not all_tags:
            return ("Log is empty.",)

        common = Counter(all_tags).most_common(top_n)
        recommended = ", ".join(f"{tag}({count})" for tag, count in common)
        return (recommended,)
