import json

class TagRecommenderNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"log_file": ("STRING",)} }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "recommend"
    CATEGORY = "tag_extraction"

    def recommend(self, log_file):
        # Placeholder: read log and suggest based on frequency
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                lines = f.readlines()
            # Simple: most common tags
            all_tags = []
            for line in lines[-10:]:  # last 10
                entry = json.loads(line)
                all_tags.extend(entry['semantic_tags'] + entry['style_tags'])
            from collections import Counter
            common = Counter(all_tags).most_common(5)
            recommended = ', '.join(tag for tag, _ in common)
        else:
            recommended = "No log available"
        return (recommended,)