"""
generate_image.py — Nano Banana 2 Image Generation Script
Uses: google-genai SDK, Vertex AI ADC, gemini-3.1-flash-image-preview
Saves: output/images/*.png + output/prompts/*.json
"""

import base64
import json
import os
import sys
import time
import mimetypes
from pathlib import Path
from datetime import datetime, timezone

from google import genai
from google.genai import types

# ─── Config ──────────────────────────────────────────────────────────────────

PROJECT   = os.environ.get("GOOGLE_CLOUD_PROJECT", "anti-gravity-489010")
LOCATION  = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")  # Must be 'global' for gemini image models
MODEL     = "gemini-3.1-flash-image-preview"

# ─── Argument ─────────────────────────────────────────────────────────────────

prompt_text  = sys.argv[1] if len(sys.argv) > 1 else "A fierce Pomeranian dog warrior in ornate silver plate armor, standing on a rocky cliff, golden hour, epic fantasy illustration, 8K"
raw_input    = sys.argv[2] if len(sys.argv) > 2 else prompt_text
style        = sys.argv[3] if len(sys.argv) > 3 else "Fantasy Art"
aspect_ratio = sys.argv[4] if len(sys.argv) > 4 else "1:1"
image_size   = sys.argv[5] if len(sys.argv) > 5 else "1K"
reference_images = sys.argv[6:] if len(sys.argv) > 6 else []

# ─── Output dirs ──────────────────────────────────────────────────────────────

out_images  = Path("output/images")
out_prompts = Path("output/prompts")
out_images.mkdir(parents=True, exist_ok=True)
out_prompts.mkdir(parents=True, exist_ok=True)

timestamp = int(time.time())

# ─── Client — ADC, no API key needed ─────────────────────────────────────────

client = genai.Client(
    vertexai=True,
    project=PROJECT,
    location=LOCATION,
)

# ─── Generation config ────────────────────────────────────────────────────────

config = types.GenerateContentConfig(
    temperature=1,
    top_p=0.95,
    max_output_tokens=32768,
    response_modalities=["TEXT", "IMAGE"],
    safety_settings=[
        types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH",        threshold="OFF"),
        types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT",   threshold="OFF"),
        types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT",   threshold="OFF"),
        types.SafetySetting(category="HARM_CATEGORY_HARASSMENT",          threshold="OFF"),
    ],
    image_config=types.ImageConfig(
        aspect_ratio=aspect_ratio,
        image_size=image_size,
        output_mime_type="image/png",
    ),
)

parts_list = []
for ref_img in reference_images:
    if os.path.exists(ref_img):
        mime_type, _ = mimetypes.guess_type(ref_img)
        if not mime_type:
            mime_type = "image/jpeg"
        with open(ref_img, "rb") as f:
            img_bytes = f.read()
        parts_list.append(types.Part.from_bytes(data=img_bytes, mime_type=mime_type))
        print(f"🖼️  Loaded reference image: {ref_img}")

parts_list.append(types.Part.from_text(text=prompt_text))

contents = [
    types.Content(
        role="user",
        parts=parts_list,
    )
]

# ─── Generate ─────────────────────────────────────────────────────────────────

print(f"⏳ Generating with {MODEL} (Fast mode, no preliminary thinking)...")
print(f"   Prompt: {prompt_text[:80]}...")

image_index = 1
saved_files = []

for chunk in client.models.generate_content_stream(
    model=MODEL,
    contents=contents,
    config=config,
):
    for part in chunk.candidates[0].content.parts if (chunk.candidates and chunk.candidates[0].content) else []:
        if part.inline_data and part.inline_data.data:
            # Decode and save image
            img_data  = base64.b64decode(part.inline_data.data) if isinstance(part.inline_data.data, str) else part.inline_data.data
            img_file  = out_images / f"generated_image_{timestamp}_{image_index}.png"
            img_file.write_bytes(img_data)
            print(f"✅ Image saved: {img_file}")

            # Save prompt metadata JSON
            meta = {
                "id":             f"{timestamp}_{image_index}",
                "timestamp_utc":  datetime.now(timezone.utc).isoformat(),
                "model":          MODEL,
                "skill":          "image-generation",
                "style":          style,
                "aspect_ratio":   aspect_ratio,
                "image_size":     image_size,
                "raw_user_input": raw_input,
                "enhanced_prompt": prompt_text,
                "parameters": {
                    "temperature":       1,
                    "top_p":             0.95,
                    "thinking_level":    "OFF",
                    "responseModalities": ["TEXT", "IMAGE"],
                },
                "output_file": str(img_file),
            }
            meta_file = out_prompts / f"prompt_{timestamp}_{image_index}.json"
            meta_file.write_text(json.dumps(meta, indent=4))
            print(f"✅ Prompt metadata: {meta_file}")

            saved_files.append(str(img_file))
            image_index += 1

        elif part.text:
            print(f"   Model: {part.text}", end="", flush=True)

print(f"\n\n🎉 Done! {len(saved_files)} image(s) saved.")
for f in saved_files:
    print(f"   → {f}")
