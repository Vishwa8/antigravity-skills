---
name: generating-images
description: Generates AI images via the Vertex AI Gemini image generation API (Nano Banana 2) with automatic prompt enhancement. Handles the full pipeline — prompt crafting, style detection, API submission, response parsing, and structured output delivery. Use when the user mentions generating, creating, or making an image, asks for help writing or improving image prompts, discusses AI visual content creation, wants variations or batch generation, requests a specific visual style (cinematic, anime, product shot, logo, etc.), or asks for image-to-image generation. Proactively offer this skill if the user is thinking about visual content.
---

# 🎨 Image Generation Skill

Generate professional-quality AI images using **`gemini-3.1-flash-image-generation`** (Nano Banana 2) via Vertex AI, with automatic prompt enhancement. Uses ADC — no API key required.

---

## Authentication

**Auth: ✅ ADC (Application Default Credentials) — no API key required.**

1. `gcloud auth application-default login` completed
2. `GOOGLE_CLOUD_PROJECT` env var set to your GCP project ID
3. `pip install google-genai` installed
4. Vertex AI API enabled on the project
5. Billing enabled (required for `gemini-3.1-flash-image-preview`)

> **Location must be `global`** — `us-central1` returns 404 for this model.

Resolve project: `GOOGLE_CLOUD_PROJECT` env var → ask the user.

> **If hanging with no response:** The model is not yet enabled. Tell the user to visit the [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) and enable `gemini-3.1-flash-image-generation`, or fall back to `imagen-3.0-generate-002`.

---

## When to Use This Skill

- User mentions generating, creating, or making an image
- User asks for help writing or improving image prompts
- User wants variations or batch generation
- User requests a specific visual style (cinematic, anime, product shot, logo, etc.)
- User says things like *"make me a picture of X"* or *"I need a thumbnail"*
- Proactively offer if the user is thinking about visual content

---

## Core Workflow

Every image generation request follows these steps. Do not skip or reorder.

### Step 1 — Parse the Request

Extract from the user's message. Fill in sensible defaults rather than asking:

| Field | Required? | Default |
| --- | --- | --- |
| Subject / scene | Yes | — |
| Style | No | Photorealistic |
| Aspect ratio | No | `1:1` |
| Number of images | No | `1` |
| Reference images | No | None (Can accept up to 14 absolute paths) |
| Special instructions | No | None |

**Auto-detect style and ratio from common phrases:**

| User Says | Style | Ratio | Enhancement Focus |
| --- | --- | --- | --- |
| "headshot" / "portrait" | Photorealistic | 3:4 | Shallow DOF, portrait lens, studio lighting |
| "wallpaper" / "desktop" | Any | 16:9 | Ultra-wide composition, high detail |
| "phone wallpaper" / "story" | Any | 9:16 | Vertical composition, mobile framing |
| "product photo" | Product Shot | 1:1 | Clean background, commercial lighting |
| "logo" | Logo Design | 1:1 | Vector-clean, minimal, scalable |
| "thumbnail" | Cinematic | 16:9 | High contrast, bold focal point |
| "social media post" | Any | 1:1 | Vibrant, scroll-stopping |
| "concept art" | Concept Art | 16:9 | Dynamic, atmospheric |
| "anime character" | Anime | 3:4 | Expressive, detailed |

---

### Step 2 — Enhance the Prompt

This is the most important step. **Skip only** if the user says "use my exact prompt" or "no enhancement."

Read `references/prompt-enhancement.md` for the full enhancement engine. Apply it to every generation.

**Always show the user your enhanced prompt** before and after generation. Append the aspect ratio as a natural language instruction at the end:

> *"...Generate as a 16:9 widescreen landscape image."*

---

### Step 3 — Submit to the API

Use the **Python SDK** via the `generate_image.py` script provided with this skill.

**Quick call:**
Locate the script `generate_image.py` within this skill's `scripts` directory. Always use the **absolute path** to the script when invoking from your workspace. For example, if this skill is installed globally, the script is located at `~/.agent/skills/nano-banana-2-image-generation/scripts/generate_image.py`.

```bash
# Basic usage
python "C:\Users\VISHWA\.agent\skills\nano-banana-2-image-generation\scripts\generate_image.py" "ENHANCED_PROMPT" "RAW_USER_INPUT" "Fantasy Art" "1:1" "1K"

# With image-to-image / multi-image references (Append up to 14 absolute paths at the end)
python "C:\Users\VISHWA\.agent\skills\nano-banana-2-image-generation\scripts\generate_image.py" "ENHANCED_PROMPT" "RAW_USER_INPUT" "Fantasy Art" "1:1" "1K" "C:\absolute\path\to\ref1.jpg" "C:\absolute\path\to\ref2.png"
```

*(Note: The script outputs to `output/images/` and `output/prompts/` relative to your **current working directory**, which is exactly what we want).*

The script uses `google-genai` SDK with:
- `vertexai=True`, `project=GOOGLE_CLOUD_PROJECT`, `location=global`
- `ThinkingConfig(thinking_level="HIGH")` — model reasons before drawing
- `ImageConfig(aspect_ratio=...`

Supported sizes: `1K`, `2K`, `4K`
Supported ratios: `1:1`, `3:4`, `4:3`, `9:16`, `16:9`, `auto`

---

### Step 4 — Extract, Decode, and Save

This step is completely handled automatically by the `generate_image.py` script. The script decodes the stream and automatically persists outputs relative to your workspace root.

Ensure outputs are verified in the `output/` folder:

```
output/
├── images/
│   └── generated_image_{timestamp}_{index}.png
└── prompts/
    └── prompt_{timestamp}_{index}.json
```

Read the standard output from the Python script to see exactly where the files were saved so you can deliver those paths to the user.

---

### Step 5 — Deliver

Tell the user:
1. The **saved image path** in `output/images/`
2. The **prompt JSON path** in `output/prompts/`
3. The **enhanced prompt** used (so they can iterate)
4. Any **text** the model returned alongside the image

---

## Error Recovery

1. **Hanging with no response** → Model not enabled. Fall back to `imagen-3.0-generate-002` (uses `predict` API — see `references/api-reference.md`). Tell the user to enable the model in [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden).
2. **First real failure** → Retry with same parameters *(transient)*
3. **Second failure** → Simplify the prompt — strip modifiers *(prompt too complex)*
4. **`400` error** → Safety filter triggered. Rephrase prompt.
5. **`401/403`** → ADC not configured or model not enabled. Check IAM + Model Garden.
6. **`429`** → Rate limited. Wait 30 seconds, retry.
7. **Still failing** → Show raw API response.

---

## Batch Generation

- For multiple variations, send **separate requests** with prompt tweaks (vary lighting, color palette, angle, or mood)
- Each must be saved with its own timestamped image + prompt JSON
- Deliver all results together

---

## Supported Parameters

| Parameter | Notes |
| --- | --- |
| Model | `gemini-3.1-flash-image-generation` (default) |
| Aspect ratio | Pass in prompt: *"Generate as a 16:9 widescreen image."* |
| Temperature | `1.0` default. Lower = more literal, Higher = more creative |
| Image-to-Image | Pass reference image as `inlineData` in the `parts[]` array |

---

## Checklist

- [ ] Subject/scene identified
- [ ] Style detected (or defaulted to Photorealistic)
- [ ] Aspect ratio determined
- [ ] Prompt enhanced (`references/prompt-enhancement.md`)
- [ ] Enhanced prompt shown to user
- [ ] API called with `generateContent` format (NOT `predict`)
- [ ] Parts iterated — `inlineData` extracted
- [ ] Image saved to `output/images/`
- [ ] Prompt JSON saved to `output/prompts/`
- [ ] File paths + enhanced prompt delivered to user

---

## Reference Files

- **[`references/prompt-enhancement.md`](references/prompt-enhancement.md)** — 14 style categories, 6 enhancement rules, camera/lens language, art direction, assembly template. **Read before every generation.**
- **[`references/api-reference.md`](references/api-reference.md)** — Full SDK usage, `ImageConfig` params, streaming, response parsing, output structure. **Read when making API calls.**
- **[`scripts/generate_image.py`](scripts/generate_image.py)** — The confirmed working generation script. Run directly or use as reference for inline calls.
