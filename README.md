# Progressive Tag Extraction

A ComfyUI extension for progressive tag extraction from generated images using dual [LLM + Vision] stacks.

## Purpose

Extract, arbitrate, and log semantic and stylistic tags from images to build a high-quality tag vocabulary for prompt optimization, dataset curation, and LoRA training.

## Nodes

- **VisionTagExtractorNodeA**: Extracts semantic tags (objects, actions, scenes) using nexa_qwen3.
- **VisionTagExtractorNodeB**: Extracts style/aesthetic tags (lighting, medium, color, composition) using nexa_wizard.
- **TagArbiterNode**: Merges, deduplicates, and ranks tags from both sources.
- **PromptTagComparatorNode**: Compares original prompt to extracted tags, identifies gaps or emergent concepts.
- **TagLoggerNode**: Logs image, prompt, tags, and analysis to JSONL file.
- **TagRecommenderNode**: Suggests new tags based on historical data.

## Installation

1. Install ComfyUI.
2. Place this folder in ComfyUI/custom_nodes/.
3. Install dependencies: `pip install -r requirements.txt`
4. Ensure Nexa CLI is installed with qwen3 and wizard models.

## Usage

Load the sample workflow in examples/ and connect to your image generation pipeline.

## Outputs

- tags.jsonl: Structured log of extractions and comparisons.

## Dependencies

- ComfyUI
- Nexa CLI (2 instances)
- Python packages: pillow, torch, numpy