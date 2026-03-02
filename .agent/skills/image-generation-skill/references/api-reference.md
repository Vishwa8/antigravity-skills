# Image Generation API Reference

Full API reference for generating images using **`gemini-3.1-flash-image-generation`** (Nano Banana 2) via Vertex AI, with ADC authentication.

---

## Authentication

**Auth: ✅ ADC (Application Default Credentials) — no API key required.**

```bash
gcloud auth application-default login
```

### Required Environment Variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `GOOGLE_CLOUD_PROJECT` | Yes | — | Your GCP project ID |
| `GOOGLE_CLOUD_LOCATION` | No | `global` | Use `global` for Gemini image models |

### Getting a Token

```bash
gcloud auth print-access-token
```

---

## ⚠️ IMPORTANT: Two Different API Surfaces

Gemini image models and Imagen models use **completely different APIs**. Do not mix them up.

| Model Family | API Endpoint | Request Format |
| --- | --- | --- |
| **Gemini** (`gemini-*`) | `generateContent` | `contents[]` with `parts[]` |
| **Imagen** (`imagen-*`) | `predict` | `instances[]` with `prompt` |

**This skill uses the Gemini `generateContent` API.**

---

## Primary Endpoint

```
POST https://aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/global/publishers/google/models/{MODEL}:generateContent
```

> **Note:** Always use `global` as the location for Gemini image generation models.

---

## Models

| Model ID | Codename | Notes |
| --- | --- | --- |
| `gemini-3.1-flash-image-generation` | **Nano Banana 2** ⭐ | Latest, fastest, highest quality — **use this by default** |
| `gemini-3.0-pro-image-generation` | Nano Banana Pro | Slower, higher detail, 4K capable |
| `gemini-2.5-flash-preview-image-generation` | Nano Banana (v1) | Older generation |
| `gemini-2.0-flash-exp-image-generation` | — | Earlier experiment, broadly available |
| `imagen-3.0-generate-002` | Imagen 3 | Fallback — uses different `predict` API |

---

## Request Format

### Text-to-Image (Standard)

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "YOUR_ENHANCED_PROMPT_HERE"
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"]
  }
}
```

### Text-to-Image (With Aspect Ratio)

Gemini image models accept natural language aspect ratio guidance in the prompt itself:

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "YOUR_ENHANCED_PROMPT_HERE. Generate as a 16:9 widescreen landscape image."
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "temperature": 1.0
  }
}
```

### Image-to-Image (Editing / Style Transfer)

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "inlineData": {
            "mimeType": "image/jpeg",
            "data": "BASE64_ENCODED_REFERENCE_IMAGE"
          }
        },
        {
          "text": "Transform this image to: YOUR_PROMPT"
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"]
  }
}
```

### Multi-Turn / Conversational Editing

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [{ "text": "Generate an image of a forest at sunrise" }]
    },
    {
      "role": "model",
      "parts": [
        { "inlineData": { "mimeType": "image/png", "data": "PREVIOUS_IMAGE_BASE64" } }
      ]
    },
    {
      "role": "user",
      "parts": [{ "text": "Now add a deer in the foreground" }]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"]
  }
}
```

---

## Response Format

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "Here is the generated image..."
          },
          {
            "inlineData": {
              "mimeType": "image/png",
              "data": "iVBORw0KGgoAAAANSUhEUgAA..."
            }
          }
        ]
      }
    }
  ]
}
```

> **Image data** is in `candidates[0].content.parts[].inlineData.data` — base64-encoded PNG.
> Parts may contain both `text` and `inlineData` — iterate through all parts and extract `inlineData` ones.

---

## Output Structure

All generated assets **must** be saved under the `output/` directory of whichever project the skill is used in:

```
output/
├── images/
│   └── generated_image_{timestamp}_{index}.png
└── prompts/
    └── prompt_{timestamp}_{index}.json
```

### Prompt JSON Schema

Every generation must save a companion JSON file with the full prompt and parameters:

```json
{
  "id": "1740938400_1",
  "timestamp_utc": "2026-03-02T22:45:00Z",
  "model": "gemini-3.1-flash-image-generation",
  "skill": "image-generation",
  "style": "Fantasy Art",
  "aspect_ratio": "1:1",
  "raw_user_input": "a pomeranian warrior",
  "enhanced_prompt": "Epic fantasy illustration of a fierce but adorable Pomeranian dog...",
  "parameters": {
    "responseModalities": ["TEXT", "IMAGE"],
    "temperature": 1.0
  },
  "output_file": "output/images/generated_image_1740938400_1.png"
}
```

---

## Full cURL Example

```bash
PROJECT="anti-gravity-489010"
MODEL="gemini-3.1-flash-image-generation"
TOKEN=$(gcloud auth print-access-token)

curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://aiplatform.googleapis.com/v1/projects/${PROJECT}/locations/global/publishers/google/models/${MODEL}:generateContent" \
  -d '{
    "contents": [{
      "role": "user",
      "parts": [{
        "text": "Epic fantasy illustration of a fierce Pomeranian warrior in silver armor on a cliff, golden hour, low angle, 8K, highly detailed"
      }]
    }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"]
    }
  }'
```

---

## Complete PowerShell Generation Script

```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$RawPrompt,

    [string]$EnhancedPrompt = "",
    [string]$Style = "Photorealistic",
    [string]$AspectRatio = "1:1",
    [string]$Model = "gemini-3.1-flash-image-generation",
    [int]$Temperature = 1,
    [string]$OutputPrefix = "generated_image"
)

$PROJECT  = $env:GOOGLE_CLOUD_PROJECT
if (-not $PROJECT) { Write-Error "Set GOOGLE_CLOUD_PROJECT"; exit 1 }

$token    = (gcloud auth print-access-token).Trim()
$url      = "https://aiplatform.googleapis.com/v1/projects/${PROJECT}/locations/global/publishers/google/models/${Model}:generateContent"
$prompt   = if ($EnhancedPrompt) { "$EnhancedPrompt. Output as $AspectRatio aspect ratio." } else { "$RawPrompt. Output as $AspectRatio aspect ratio." }
$timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()

New-Item -ItemType Directory -Force -Path "output\images" | Out-Null
New-Item -ItemType Directory -Force -Path "output\prompts" | Out-Null

$body = @{
    contents = @(@{
        role  = "user"
        parts = @(@{ text = $prompt })
    })
    generationConfig = @{
        responseModalities = @("TEXT", "IMAGE")
        temperature        = $Temperature
    }
} | ConvertTo-Json -Depth 6

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type"  = "application/json"
}

Write-Host "⏳ Generating with $Model..."
$response = Invoke-RestMethod -Uri $url -Method POST -Headers $headers -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -TimeoutSec 120

$i = 1
foreach ($part in $response.candidates[0].content.parts) {
    if ($part.inlineData) {
        $bytes    = [Convert]::FromBase64String($part.inlineData.data)
        $imgFile  = "output\images\${OutputPrefix}_${timestamp}_${i}.png"
        [IO.File]::WriteAllBytes((Resolve-Path "." | Join-Path -ChildPath $imgFile), $bytes)

        $meta = @{
            id              = "${timestamp}_${i}"
            timestamp_utc   = [DateTimeOffset]::UtcNow.ToString("o")
            model           = $Model
            skill           = "image-generation"
            style           = $Style
            aspect_ratio    = $AspectRatio
            raw_user_input  = $RawPrompt
            enhanced_prompt = $prompt
            parameters      = @{
                responseModalities = @("TEXT","IMAGE")
                temperature        = $Temperature
            }
            output_file     = $imgFile
        }
        $metaFile = "output\prompts\prompt_${timestamp}_${i}.json"
        $meta | ConvertTo-Json -Depth 4 | Out-File -FilePath $metaFile -Encoding utf8

        Write-Host "✅ Image : $imgFile"
        Write-Host "✅ Prompt: $metaFile"
        $i++
    }
}
```

Usage:
```powershell
.\generate-image.ps1 -RawPrompt "a pomeranian warrior" -EnhancedPrompt "Epic fantasy illustration..." -Style "Fantasy Art" -AspectRatio "16:9"
```

---

## Error Codes & Recovery

| Code | Meaning | Recovery |
| --- | --- | --- |
| `200` | Success | Parse `candidates[0].content.parts` for `inlineData` |
| `400` | Bad request / safety filter | Simplify prompt |
| `401` | Unauthorized | `gcloud auth application-default login` |
| `403` | Forbidden / model not enabled | Enable API in Cloud Console; check allowlist |
| `404` | Model not found | Verify model ID; try `global` location |
| `429` | Rate limited | Wait 30 seconds, retry |
| `503` | Hanging / no response | Model may not be enabled — check Model Garden |

> **Hanging with no response** (no error, just waiting forever) = the model is not accessible on your project. Go to Vertex AI Model Garden and enable it, or use `imagen-3.0-generate-002` as a fallback.

---

## Fallback: Imagen 3 (Always Available)

If Gemini image models are inaccessible, use Imagen 3 which uses the `predict` API:

```
POST https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/us-central1/publishers/google/models/imagen-3.0-generate-002:predict
```

```json
{
  "instances": [{ "prompt": "YOUR_ENHANCED_PROMPT" }],
  "parameters": { "sampleCount": 1, "aspectRatio": "1:1" }
}
```

Response: `predictions[0].bytesBase64Encoded`
