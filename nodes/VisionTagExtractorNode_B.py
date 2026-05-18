import base64
import hashlib
import io

import numpy as np
import requests
from PIL import Image


class VisionTagExtractorNodeB:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "vision_url": ("STRING", {"default": "http://127.0.0.1:8082/v1"}),
                "n_predict": ("INT", {"default": 300, "min": 50, "max": 2000}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_tags",)
    FUNCTION = "extract"
    CATEGORY = "progressive_tags"

    @classmethod
    def IS_CHANGED(cls, image, vision_url, n_predict):
        arr = image.cpu().numpy()
        return hashlib.md5(arr.tobytes()[:65536]).hexdigest()

    def extract(self, image, vision_url, n_predict):
        try:
            img_np = np.clip(255.0 * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8)
            if img_np.ndim == 2:
                img_np = np.stack([img_np] * 3, axis=-1)
            pil_img = Image.fromarray(img_np, "RGB")
            buf = io.BytesIO()
            pil_img.save(buf, format="JPEG", quality=85)
            b64 = base64.b64encode(buf.getvalue()).decode()

            resp = requests.post(
                f"{vision_url.rstrip('/')}/chat/completions",
                json={
                    "messages": [{
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                            {"type": "text", "text": (
                                "Extract style and aesthetic tags from this image as a comma-separated list. "
                                "Include: art style, medium (photography/painting/digital etc.), lighting quality, "
                                "color palette, mood, composition style, texture, time period, visual aesthetic, "
                                "and rendering technique. "
                                "Output ONLY the comma-separated tags, nothing else."
                            )},
                        ],
                    }],
                    "max_tokens": n_predict,
                },
                timeout=120,
            )
            resp.raise_for_status()
            tags = resp.json()["choices"][0]["message"]["content"].strip()
            return (tags,)
        except (requests.RequestException, KeyError, IndexError) as e:
            return (f"vision_server_error: {e}",)
        except Exception as e:
            return (f"error: {e}",)
