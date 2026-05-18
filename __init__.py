from .nodes.VisionTagExtractorNode_A import VisionTagExtractorNodeA
from .nodes.VisionTagExtractorNode_B import VisionTagExtractorNodeB
from .nodes.TagArbiterNode import TagArbiterNode
from .nodes.PromptTagComparatorNode import PromptTagComparatorNode
from .nodes.TagLoggerNode import TagLoggerNode
from .nodes.TagRecommenderNode import TagRecommenderNode
from .nodes.LlamaCppServerNode import LlamaCppServerNode

NODE_CLASS_MAPPINGS = {
    "ProgTag_LlamaCppServerNode": LlamaCppServerNode,
    "ProgTag_VisionTagExtractorA": VisionTagExtractorNodeA,
    "ProgTag_VisionTagExtractorB": VisionTagExtractorNodeB,
    "ProgTag_TagArbiterNode": TagArbiterNode,
    "ProgTag_PromptTagComparatorNode": PromptTagComparatorNode,
    "ProgTag_TagLoggerNode": TagLoggerNode,
    "ProgTag_TagRecommenderNode": TagRecommenderNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ProgTag_LlamaCppServerNode": "Vision Server (GGUF Chatbox)",
    "ProgTag_VisionTagExtractorA": "Vision Tag Extractor A (Semantic)",
    "ProgTag_VisionTagExtractorB": "Vision Tag Extractor B (Style)",
    "ProgTag_TagArbiterNode": "Tag Arbiter",
    "ProgTag_PromptTagComparatorNode": "Prompt Tag Comparator",
    "ProgTag_TagLoggerNode": "Tag Logger",
    "ProgTag_TagRecommenderNode": "Tag Recommender",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
