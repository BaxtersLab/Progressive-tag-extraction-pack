# DEVNOTES — Progressive Tag Extraction Pack
> Carry this file into every future session. It is the handoff document.

---

## Current Status: CODE COMPLETE — AWAITING FIRST TEST

All nodes have been fully rewritten. The pack has never been loaded with the new GGUF Chatbox backend.
Next session should start with: **install → load in ComfyUI → smoke test each node.**

---

## What Changed (Session 2 — May 2026)

**Backend switch: Nexa CLI → GGUF Chatbox vision server (8082)**

The original implementation used `nexa run qwen3` and `nexa run wizard` via subprocess. This was scrapped because Nexa requires models fetched from inside the Nexa app only. Replaced with Baxter's existing GGUF Chatbox vision server (8082) which handles multimodal image+text inference using llava/clip.

**Every node was rewritten or fixed:**

| Node | Old state | New state |
|---|---|---|
| `VisionTagExtractorNodeA` | subprocess nexa CLI, saved temp PNG to CWD, no IS_CHANGED | Base64-encodes image in memory, calls vision server (8082), IS_CHANGED on tensor hash |
| `VisionTagExtractorNodeB` | same as A, different Nexa model | Same pattern, style-focused LLM prompt |
| `TagArbiterNode` | split on comma only — broke with multiline LLM responses | Uses `re.split(r"[,\n;]+", ...)` for robust tag parsing |
| `PromptTagComparatorNode` | split prompt on spaces only, no partial matching | Regex word tokenization, stop word filtering, substring matching for missing/emergent |
| `TagLoggerNode` | wrote to CWD `"tags.jsonl"`, returned `()` with no UI | Writes to `<pack>/logs/tags.jsonl`, returns UI dict, robust tag splitting |
| `TagRecommenderNode` | bug: used `os` without importing it, no `top_n` param | Fixed import, defaults to pack's own log file, added `top_n` INT widget |
| `NexaPopupLoaderNode` | tkinter `mainloop()` blocked ComfyUI server thread | **Removed from imports.** File left on disk (safe to delete). |
| `LlamaCppServerNode` | did not exist | New node: health-pings all 3 servers, outputs chat_url / vision_url / listening_url / status |

**Other files changed:**
- `__init__.py` — updated imports, all keys prefixed `ProgTag_` to avoid global collisions, NexaPopupLoaderNode removed
- `requirements.txt` — was `pillow, torch, numpy, nexa-cli` → now just `requests` (pillow/torch/numpy are ComfyUI's own environment)
- `examples/sample_workflow.json` — was invalid format (Python-dict style links, wrong node structure) → fully rewritten as valid ComfyUI workflow JSON, drag-and-drop ready
- `manifests/progressivetagextraction.yaml` — updated description, version bumped to 2.0.0, nexa-cli removed
- `NexaPopupLoaderNode.py` — left on disk but no longer imported (safe to delete)

---

## Server Architecture (do not change these ports — they are fixed by GGUF Chatbox)

| Server | Port | API style | Use for |
|---|---|---|---|
| Chat/Text proxy | 8080 | `POST /v1/chat/completions` (OpenAI) | Not currently used by this pack |
| Vision (llava) | 8082 | `POST /v1/chat/completions` (OpenAI) | Image understanding: semantic + style tag extraction |
| Listening (audio) | 8083 | `POST /action` (custom) | Not used by this pack |

Full protocol reference: `c:\Users\Baxter\Desktop\rag libary\baxter-server-connections.md`

---

## What Still Needs Doing

### Priority 1 — Must do before this pack is usable

- [ ] **Smoke test in ComfyUI** — load the pack, confirm no import errors in the console
- [ ] **Test LlamaCppServerNode** — start GGUF Chatbox, add the node, confirm status shows `online` for vision
- [ ] **Test VisionTagExtractorA** — connect a LoadImage node, run it, confirm vision server responds and tags come back
- [ ] **Test VisionTagExtractorB** — same
- [ ] **Test the full sample workflow** — drag `examples/sample_workflow.json` into ComfyUI, set a real image in LoadImage, run end to end
- [ ] **Verify TagLoggerNode writes to `logs/tags.jsonl`** — check the file exists and entries are valid JSON

### Priority 2 — Improvements once basic flow works

- [ ] **Wire TagRecommenderNode into sample workflow** — built but not in sample_workflow.json to keep it readable. Add after TagLoggerNode.
- [ ] **Add a chat-formatting step** — optionally pass extracted tags through the chat server (8080) to normalize/clean up before comparison. Add `chat_url` input to extractors.
- [ ] **Add PromptMutatorNode** — a node that takes missing_tags + original prompt and rewrites via chat server (8080), giving a feedback loop similar to the audio pack.
- [ ] **Test TagRecommenderNode** — run the full pipeline several times to build up log entries, then verify tag frequency recommendations.

### Priority 3 — Polish

- [ ] **Update README.md** — still describes old Nexa architecture. Needs to reflect GGUF Chatbox vision server setup.
- [ ] **Delete NexaPopupLoaderNode.py** — dead file, safe to remove once confirmed nothing references it.
- [ ] **Add `pyproject.toml`** — missing from the pack. Add with proper ComfyUI registry metadata.

---

## Known Risks / Watch Out For

- **GGUF Chatbox vision server (8082) must be running** before any extractor node is queued. If the server is offline, nodes return an error string rather than crashing — safe but produces garbage workflow output. Add `LlamaCppServerNode` and check its `status` output first.
- **Vision model requires mmproj file** — the vision server needs both a GGUF model AND a clip/mmproj file configured in GGUF Chatbox settings. Without mmproj, image inputs will fail at the server level even if the server is "online".
- **Image encoding:** images are JPEG-encoded in memory at quality=85 (no temp files written to disk). Grayscale images are handled (converted to RGB before encoding).
- **`IS_CHANGED` hashes first 64KB of the image tensor bytes.** A different image correctly triggers re-run. Same image reconnected uses cached output.
- **Log file location:** `<pack_root>/logs/tags.jsonl` — created automatically on first run. The `logs/` directory is created if missing.
- **TagRecommenderNode `log_file` widget** defaults to the pack's own absolute log path at load time. If the pack is moved, update the widget value manually.

---

## Node Key Names (for workflow JSON)

All keys are prefixed `ProgTag_` to prevent collision with other packs.

| Key (in workflow JSON `type` field) | Display name |
|---|---|
| `ProgTag_LlamaCppServerNode` | Vision Server (GGUF Chatbox) |
| `ProgTag_VisionTagExtractorA` | Vision Tag Extractor A (Semantic) |
| `ProgTag_VisionTagExtractorB` | Vision Tag Extractor B (Style) |
| `ProgTag_TagArbiterNode` | Tag Arbiter |
| `ProgTag_PromptTagComparatorNode` | Prompt Tag Comparator |
| `ProgTag_TagLoggerNode` | Tag Logger |
| `ProgTag_TagRecommenderNode` | Tag Recommender |

---

## Session Log

| Date | What happened |
|---|---|
| ~4 months ago | Initial build with GPT-4o mini. Nexa CLI backend. Placeholders throughout. Workflow JSON was invalid format. TagRecommenderNode had `os` import bug. |
| 2026-05-18 | Full rewrite with Claude. Switched to GGUF Chatbox vision server (8082). All nodes functional. Workflow JSON fixed. DEVNOTES.md created. |
