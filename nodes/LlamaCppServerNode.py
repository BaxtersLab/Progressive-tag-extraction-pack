import requests

_PORTS = {"chat": 8080, "vision": 8082, "listening": 8083}


def _ping(host, port):
    try:
        r = requests.get(f"http://{host}:{port}/health", timeout=3)
        return "online" if r.ok else "error"
    except requests.RequestException:
        return "offline"


class LlamaCppServerNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "host": ("STRING", {"default": "127.0.0.1"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("chat_url", "vision_url", "listening_url", "status")
    FUNCTION = "check"
    CATEGORY = "progressive_tags"

    @classmethod
    def IS_CHANGED(cls, host):
        return float("nan")

    def check(self, host):
        statuses = {name: _ping(host, port) for name, port in _PORTS.items()}
        status_str = " | ".join(f"{name}:{state}" for name, state in statuses.items())
        return (
            f"http://{host}:{_PORTS['chat']}/v1",
            f"http://{host}:{_PORTS['vision']}/v1",
            f"http://{host}:{_PORTS['listening']}",
            status_str,
        )
