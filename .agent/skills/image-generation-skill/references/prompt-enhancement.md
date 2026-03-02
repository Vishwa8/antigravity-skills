# Prompt Enhancement Engine

This document contains the full prompt enhancement system. Read it before every image generation to ensure maximum quality output.

---

## The Enhancement Philosophy

A prompt like *"a cat on a windowsill"* produces something generic. But with style prefixes, lighting cues, composition direction, and quality tags, the same idea becomes a professional image:

> *"A photorealistic close-up of a ginger tabby cat lounging on a sunlit windowsill, soft golden hour light streaming through sheer curtains, shallow depth of field, warm amber tones, dust motes floating in light beams, shot on 85mm f/1.4 lens, 8K resolution"*

The difference is specificity. Generation models fill in gaps randomly — your job is to close those gaps intentionally.

---

## Style Categories

Each style has a **prefix** (placed before the subject) and a **suffix** (placed after). Apply the style that best matches the user's intent.

### 1. Photorealistic
- **Prefix:** `A photorealistic photograph of`
- **Suffix:** `shot on Canon EOS R5, 85mm lens, natural lighting, 8K resolution, hyper-detailed`
- **Best for:** Portraits, product shots, nature, architecture

### 2. Cinematic
- **Prefix:** `A cinematic film still of`
- **Suffix:** `dramatic lighting, anamorphic lens flare, color graded, 35mm film grain, wide aspect ratio, movie scene`
- **Best for:** Thumbnails, hero images, dramatic scenes

### 3. Digital Art
- **Prefix:** `Digital art illustration of`
- **Suffix:** `vibrant colors, clean lines, trending on ArtStation, highly detailed, professional digital painting`
- **Best for:** Editorial, social media, marketing

### 4. Concept Art
- **Prefix:** `Professional concept art of`
- **Suffix:** `atmospheric perspective, dynamic composition, matte painting style, cinematic lighting, detailed environment`
- **Best for:** Game art, worldbuilding, environments

### 5. Anime / Manga
- **Prefix:** `Anime-style illustration of`
- **Suffix:** `cel-shaded, detailed eyes, dynamic pose, vibrant palette, studio quality animation, clean linework`
- **Best for:** Character art, fan art, stylized content

### 6. Oil Painting
- **Prefix:** `Oil painting of`
- **Suffix:** `visible brushstrokes, rich color palette, chiaroscuro lighting, museum quality, gallery piece, impasto texture`
- **Best for:** Fine art, classical subjects, decorative prints

### 7. Watercolor
- **Prefix:** `Watercolor painting of`
- **Suffix:** `soft washes, transparent layers, paper texture visible, gentle blending, luminous quality, artistic`
- **Best for:** Invitations, greeting cards, soft/organic subjects

### 8. 3D Render
- **Prefix:** `3D rendered scene of`
- **Suffix:** `Octane render, volumetric lighting, subsurface scattering, global illumination, physically based rendering, 8K`
- **Best for:** Product visualization, abstract, tech

### 9. Flat Design / Vector
- **Prefix:** `Flat design illustration of`
- **Suffix:** `clean vector style, bold colors, minimal shadows, geometric shapes, scalable design, modern graphic`
- **Best for:** Icons, logos, UI elements, infographics

### 10. Logo Design
- **Prefix:** `Professional logo design of`
- **Suffix:** `clean vector, minimal, scalable, balanced composition, negative space, brand identity, iconic`
- **Best for:** Branding, identity design

### 11. Product Shot
- **Prefix:** `Professional product photograph of`
- **Suffix:** `studio lighting, clean white background, commercial quality, sharp focus, lifestyle context, premium finish`
- **Best for:** E-commerce, marketing, catalogs

### 12. Fantasy Art
- **Prefix:** `Epic fantasy illustration of`
- **Suffix:** `magical atmosphere, ethereal glow, intricate details, dynamic composition, rich color palette, mythical`
- **Best for:** Book covers, game art, worldbuilding

### 13. Isometric
- **Prefix:** `Isometric view of`
- **Suffix:** `30-degree angle, clean geometry, pastel colors, detailed miniature, no perspective distortion, diorama style`
- **Best for:** Icons, infographics, game assets, tech illustrations

### 14. Vintage / Retro
- **Prefix:** `Vintage-style photograph of`
- **Suffix:** `faded colors, film grain, nostalgic mood, warm tones, vignette, retro aesthetic, analog feel`
- **Best for:** Branding, editorial, nostalgic themes

---

## Six Enhancement Rules

Apply these in order to transform any raw prompt into a professional one:

### Rule 1: Add Subject Specificity
Replace vague nouns with precise descriptions.

| Before | After |
| --- | --- |
| a dog | a golden retriever with a damp coat |
| a woman | a young woman with windswept auburn hair |
| a city | a rain-slicked Tokyo alleyway at midnight |
| a car | a matte black 1967 Mustang Fastback |

### Rule 2: Define the Lighting
Lighting transforms the mood entirely. Always specify at least one lighting descriptor.

- **Natural:** golden hour, blue hour, overcast, dappled sunlight, harsh noon sun
- **Studio:** Rembrandt lighting, butterfly lighting, rim light, three-point setup, softbox
- **Dramatic:** chiaroscuro, backlit silhouette, neon glow, candlelight, bioluminescent
- **Ambient:** foggy, misty, hazy, atmospheric, diffused

### Rule 3: Specify Composition
Tell the model *how* to frame the shot.

- **Distance:** extreme close-up, close-up, medium shot, full body, wide shot, aerial view
- **Angle:** eye level, low angle (heroic), high angle (vulnerable), bird's eye, worm's eye, Dutch angle
- **Rule of thirds:** off-center subject, lead room, negative space

### Rule 4: Set the Mood / Atmosphere
One or two mood words dramatically shift the output.

- **Warm:** cozy, nostalgic, intimate, inviting, golden
- **Cool:** serene, ethereal, mystical, melancholic, icy
- **Intense:** dramatic, electric, visceral, powerful, epic
- **Dark:** moody, noir, ominous, brooding, mysterious

### Rule 5: Add Material & Texture Cues
Physical details make images feel tangible.

- Weathered leather, brushed steel, frosted glass, rough concrete
- Velvet, silk, linen, denim, polished marble, aged wood
- Wet surfaces, dust particles, smoke wisps, lens condensation

### Rule 6: Include Technical Quality Tags
These push the model toward higher fidelity output.

- `8K resolution`, `ultra-detailed`, `sharp focus`
- `professional photography`, `award-winning`
- `masterpiece`, `best quality`, `highly detailed`
- `ray tracing`, `global illumination` (for 3D styles)

---

## Prompt Assembly Template

Combine the parts in this order:

```
[STYLE PREFIX] [SPECIFIC SUBJECT] [IN SETTING/CONTEXT], [LIGHTING], [COMPOSITION], [MOOD/ATMOSPHERE], [MATERIAL DETAILS], [STYLE SUFFIX], [QUALITY TAGS]
```

### Example Assembly

**User input:** *"a knight in a forest"*

**Enhanced:**
> *Professional concept art of a battle-scarred knight in ornate silver armor standing at the edge of an ancient moss-covered forest, volumetric god rays filtering through the canopy, low angle heroic composition, epic and mystical atmosphere, weathered metal textures with emerald reflections, atmospheric perspective, dynamic composition, matte painting style, cinematic lighting, ultra-detailed, 8K resolution*

---

## Camera & Lens Language

Use these when the style calls for photorealism:

| Lens | Effect | Use When |
| --- | --- | --- |
| 24mm wide angle | Expansive, environmental | Landscapes, architecture, establishing shots |
| 35mm | Natural perspective | Street photography, environmental portraits |
| 50mm | Human eye perspective | General-purpose, natural feeling |
| 85mm | Compressed, flattering | Portraits, headshots, beauty |
| 135mm | Strong compression, dreamy bokeh | Fashion, beauty, character close-ups |
| 200mm+ telephoto | Extreme compression | Wildlife, sports, dramatic isolation |
| Macro lens | Extreme close-up detail | Small objects, textures, insects |
| Tilt-shift | Miniature effect | Cityscapes, creative perspectives |
| Fisheye | Extreme distortion | Action sports, creative, abstract |

---

## Art Direction Keywords

Use these to dial in specific visual qualities:

**Color Palettes:**
- Monochromatic, complementary, analogous, triadic
- Earth tones, jewel tones, pastel, neon, muted
- Specific: "cyan and magenta palette", "amber and navy"

**Rendering Styles:**
- Photorealistic, hyperrealistic, stylized, abstract, minimalist
- Painterly, sketchy, geometric, organic, surreal

**Time Periods (for setting/costume):**
- Victorian, Art Deco, 1970s retro, futuristic, cyberpunk, steampunk
- Medieval, Renaissance, Baroque, Modern, Post-apocalyptic

**Cultural References:**
- Studio Ghibli style, Blade Runner aesthetic, Wes Anderson palette
- Ukiyo-e inspired, Art Nouveau, Bauhaus, Memphis design

---

## Negative Prompt Guidance

While Vertex AI Imagen doesn't use explicit negative prompts in the same way as Stable Diffusion, you can steer away from unwanted elements by being more specific about what you DO want. Instead of saying "no blur", say "tack-sharp focus". Instead of "no distortion", say "anatomically correct proportions."

**Common quality steering phrases:**
- `well-proportioned`, `anatomically correct`
- `sharp focus`, `tack-sharp`
- `clean composition`, `balanced framing`
- `professional quality`, `polished finish`
