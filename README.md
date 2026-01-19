# Progressive Tag Extraction

A ComfyUI extension for progressive tag extraction from generated images using dual [LLM + Vision] stacks.

## Purpose

Extract, arbitrate, and log semantic and stylistic tags from images to build a high-quality tag vocabulary for prompt optimization, dataset curation, and LoRA training.

## Installation

1. Ensure ComfyUI is installed and running.
2. Copy this folder (`progressive-tag-extraction`) to your ComfyUI `custom_nodes` directory.
3. Install Python dependencies: `pip install -r requirements.txt`
4. Install Nexa CLI: `pip install nexa-cli`
5. Pull the required models:
   - `nexa pull qwen3` (for semantic extraction)
   - `nexa pull wizardlm` (for style extraction)

## Nodes Overview

### VisionTagExtractorNodeA
- **Input**: Image (tensor)
- **Output**: String (semantic tags)
- **Function**: Extracts semantic tags (objects, actions, scenes) using nexa_qwen3.

### VisionTagExtractorNodeB
- **Input**: Image (tensor)
- **Output**: String (style tags)
- **Function**: Extracts style/aesthetic tags (lighting, medium, color, composition) using nexa_wizard.

### TagArbiterNode
- **Inputs**: Semantic tags (string), Style tags (string)
- **Output**: String (unified tags)
- **Function**: Merges, deduplicates, and ranks tags from both sources.

### PromptTagComparatorNode
- **Inputs**: Prompt (string), Extracted tags (string)
- **Outputs**: Missing tags (string), Emergent tags (string)
- **Function**: Compares prompt to tags, identifies gaps and emergent concepts.

### TagLoggerNode
- **Inputs**: Image path (string), Prompt (string), Semantic tags (string), Style tags (string), Missing tags (string), Emergent tags (string)
- **Output**: None (logs to file)
- **Function**: Logs all data to `tags.jsonl` file.

### TagRecommenderNode (Optional)
- **Input**: Log file path (string)
- **Output**: String (recommended tags)
- **Function**: Suggests tags based on historical frequency.

## Usage

1. Load ComfyUI and ensure the extension is loaded (check console for "Progressive Tag Extraction loaded").
2. In the ComfyUI workflow editor, search for the nodes (e.g., "Vision Tag Extractor A").
3. Connect an image source (e.g., Load Image node) to both VisionTagExtractorNodeA and VisionTagExtractorNodeB.
4. Connect their outputs to TagArbiterNode.
5. Optionally, connect to PromptTagComparatorNode with a prompt input.
6. Connect to TagLoggerNode to save results.
7. Queue the workflow to process.

### Sample Workflow

See `examples/sample_workflow.json` for a complete workflow JSON that can be loaded in ComfyUI.

## Outputs

- **tags.jsonl**: A JSON Lines file with entries like:
  ```json
  {
    "image": "image_001.png",
    "prompt": "a wizard in a forest",
    "semantic_tags": ["wizard", "forest"],
    "style_tags": ["cinematic lighting"],
    "missing_tags": ["glowing"],
    "emergent_tags": ["soft focus"],
    "timestamp": "2026-01-18T12:00:00Z"
  }
  ```

## Dependencies

- ComfyUI
- Nexa CLI with qwen3 and wizardlm models
- Python: pillow, torch, numpy

## Troubleshooting

- Ensure Nexa CLI is installed and models are pulled.
- Check ComfyUI console for errors.
- Temp images are saved as `temp_image.png`; ensure write permissions.

## License

MIT