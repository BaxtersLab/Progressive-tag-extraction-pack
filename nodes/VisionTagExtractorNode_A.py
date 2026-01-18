import subprocess
import torch
from PIL import Image
import numpy as np

class VisionTagExtractorNodeA:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"image": ("IMAGE",)} }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "extract"
    CATEGORY = "tag_extraction"

    def extract(self, image):
        # Convert tensor to PIL
        image_np = np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8)
        pil_image = Image.fromarray(image_np)
        temp_path = "temp_image.png"
        pil_image.save(temp_path)
        # Call Nexa CLI for semantic tags
        result = subprocess.run(['nexa', 'run', 'qwen3', '--image', temp_path, '--prompt', 'Extract semantic tags: objects, actions, scenes'], capture_output=True, text=True)
        tags = result.stdout.strip() if result.returncode == 0 else "Error extracting tags"
        return (tags,)