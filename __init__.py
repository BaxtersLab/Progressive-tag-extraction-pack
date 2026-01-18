from .nodes.VisionTagExtractorNode_A import VisionTagExtractorNodeA
from .nodes.VisionTagExtractorNode_B import VisionTagExtractorNodeB
from .nodes.TagArbiterNode import TagArbiterNode
from .nodes.PromptTagComparatorNode import PromptTagComparatorNode
from .nodes.TagLoggerNode import TagLoggerNode
from .nodes.TagRecommenderNode import TagRecommenderNode

NODE_CLASS_MAPPINGS = {
    "VisionTagExtractorNodeA": VisionTagExtractorNodeA,
    "VisionTagExtractorNodeB": VisionTagExtractorNodeB,
    "TagArbiterNode": TagArbiterNode,
    "PromptTagComparatorNode": PromptTagComparatorNode,
    "TagLoggerNode": TagLoggerNode,
    "TagRecommenderNode": TagRecommenderNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VisionTagExtractorNodeA": "Vision Tag Extractor A (Semantic)",
    "VisionTagExtractorNodeB": "Vision Tag Extractor B (Style)",
    "TagArbiterNode": "Tag Arbiter",
    "PromptTagComparatorNode": "Prompt Tag Comparator",
    "TagLoggerNode": "Tag Logger",
    "TagRecommenderNode": "Tag Recommender",
}