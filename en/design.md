# Compression-Resistant PPT Design · 1f6s

> 1帧6秒倡议 · https://brnme.github.io/1f6s/en/design.html · 本文为 Markdown 镜像,[HTML 原版](design.html)含交互组件。

---

## Compression-Resistant PPT Design

To pair with the extreme "B&W + low resolution (480p/360p) + high compression (CRF 34+)" plans, we design presentations (PPT/Keynote) to be "compression-resistant" at the source.

Core principle

At low bitrates, encoders prioritize high-contrast edges and large color patches, sacrificing gradients, thin lines, and similar hues. The core principle is therefore: **"Black is black, white is white: no grayscale gradients, no reliance on thin lines."**

## I. Font & Size Guidelines (fighting blur)

At low resolutions, complex-stroke fonts blur into mush and small sizes simply disappear.

| Design element | Mandatory rule | Reason & notes |
| --- | --- | --- |
| **Font family** | Mandatory **sans-serif** (e.g. Source Han Sans, Microsoft YaHei, Arial, Helvetica). Strictly forbidden: serif or script fonts like SimSun, KaiTi, Times New Roman. | Sans-serif strokes are uniform and evenly weighted; after pixelated compression the outline stays crisp. The "flared mouths" and "triangular serifs" of serif faces become mosaic noise at 360p. |
| **Minimum size (body)** | ≥ **24pt** (titles recommended ≥ 36pt). | Field-tested: 24pt at 480p scaling (854×480) reads comfortably in landscape on a small phone; text below 20pt loses its strokes entirely at 360p. |
| **Font color (B&W)** | Pure black (`#000000`) for body text, pure white (`#FFFFFF`) for reversed-out text (dark backgrounds). Strictly forbidden to substitute dark gray (e.g. `#333333`) for black. | The x264 encoder detects pure-black edges most reliably and preferentially preserves sharp edges when compressing; dark gray gets mistaken for "noise" or "shadow" and blurred away, making text look soft. |
| **Font weight** | Use **Bold or Heavy** for regular display. Light/Thin only for oversized titles (>48pt). | Bold strokes have greater pixel coverage and resist H.264 detail smearing at CRF 34. |

## II. Color & Grayscale Contrast (working in black, white, gray)

Once compressed to B&W, visual hierarchy relies entirely on "luminance differences". We use only **3 grayscale levels**.

| Grayscale level | Hex value | RGB | Use for | Compression performance |
| --- | --- | --- | --- | --- |
| **Pure black (foreground)** | `#000000` | (0,0,0) | Body text, primary lines, chart borders, titles on dark backgrounds. | Excellent. Sharp edges, lowest bitrate. |
| **Mid gray (emphasis)** | `#808080` | (128,128,128) | Supplementary text, minor table cells, helper arrows, watermarks. | Usable. Requires ≥ 28pt or gray areas may compress to "blank". |
| **Pure white (background)** | `#FFFFFF` | (255,255,255) | Page background, text on light backgrounds (reversed), highlight areas. | Excellent. More whitespace → the encoder more easily classifies the area as "static" → smaller files. |
| **❌ Light gray forbidden** | `#CCCCCC` and lighter | (200+) | Strictly forbidden for text or chart lines. | Very poor. Nearly invisible after compression, or appears as "dirty" blotches. |

🔴 Red-line rule

**Eliminate all color** (red, green, blue, yellow, purple) from the final deliverable. If the source has color, select all with Ctrl+A in PPT before export, force font color to "Automatic (black)", and replace colored shape fills with the grayscale values above.

To express "distinction" without gray levels, use **italics** or **underlines** instead of relying on gray shades.

## III. Layout & Whitespace (lightening the encoder's load)

At high compression, complex textures (grids, shadows, gradients) are "size killers" — they bloat files and dirty the picture.

| Design element | Mandatory rule | Reason |
| --- | --- | --- |
| **Background** | Pure white (`#FFFFFF`) or pure black (`#000000`) only. Strictly forbidden: PPT's built-in "gradient backgrounds", "texture fills", or "image watermarks". | Solid backgrounds have near-zero DCT (discrete cosine transform) coefficients — the encoder restores them with almost no bits, leaving bitrate for the text. |
| **Shadows / 3D effects** | Completely disabled: text shadows, shape shadows, reflections, glows, 3D rotation, bevel effects. | Shadows become ugly "ghost" mosaics at low bitrates, eating into the sharpness of text edges. |
| **Charts (bars/pies)** | Alternate **solid black fills** with **hollow white outlines (strokes)**. Distinguish legends with **patterns (hatching/dots)** instead of colors. | Adjacent pie slices (gray vs black) need contrast above 50% (e.g. black–white–gray alternation), or they become indistinguishable after compression. |
| **Line weight** | Strokes/lines ≥ **2.25pt** (~3px). Lines under 1pt break at 360p. | Keeps divider and table borders continuous under extreme compression. |

## IV. Special Element Adaptation

### Embedding screenshots (code / UI)

- Strictly forbidden to paste full-screen screenshots directly (they carry tons of irrelevant pixels).
- Procedure: crop away the extra UI frame in PPT, keep only the core code/operation area; set the screenshot to "grayscale mode" and raise contrast ~+30%.
- Size: ensure code inside the screenshot is ≥ 14pt (physical size), otherwise enlarge the screenshot to a full page.

### Formulas / math symbols

- Use PPT's built-in equation editor for **vector formulas**; strictly forbidden to use image-format formulas.
- Thicken fraction bars and radical strokes in formulas so they don't fracture under compression.

## V. Final Self-Check (3-Step Method)

Before exporting the MP4, run this "3-step self-check" on the last slide (click to check off; state is saved locally):

- **Shrink test:** zoom the PPT to 50% and view from 1 meter away. If the title is unreadable, the size is too small — enlarge it.
- **Decolor test:** switch the page to "grayscale/B&W" preview in PPT. If two adjacent elements blend together, contrast is insufficient — change them to pure black/white.
- **Thin-line scan:** check all table and chart borders. Anything that shows "a single dot" instead of "a wide line" when you click it (i.e. thin lines) must be set to ≥ 2.25pt.

Reset checks

## Additional Advice

The compound effect of source adaptation

If your deck follows the rules above, its sharpness at L4/L5 (CRF 34 + stillimage) equals what an ordinary deck gets at CRF 28. That means you can **cut video size by another 40%** without **sacrificing reading experience**.

That's the compound effect of "source adaptation" — compression is not a post-production fixup; it's a collaboration that starts at the design stage.

---

[← Previous: red lines](redlines.html)
[Back to home →](index.html)
