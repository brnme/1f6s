# PPT Generation Skill · 1f6s

> 1帧6秒倡议 · https://brnme.github.io/1f6s/en/skill-ppt.html · 本文为 Markdown 镜像,[HTML 原版](skill-ppt.html)含交互组件。

---

## PPT Generation Skill

Generates a deck **from scratch** from a topic or outline, or **converts** a given web-PPT into an HTML slide deck conforming to the "1f6s" compression-resistant PPT guidelines. The output is a **self-contained single .html file** — inline CSS + minimal paging JS, zero external dependencies; double-click in a browser for keyboard paging / fullscreen presenting.

What it is

A shareable playbook any agent can read and follow (`skill/SKILL.md`). An agent reading it produces, from a given topic or page, a slide deck that implements the compression-resistant guidelines slide by slide. It serves the initiative's core claim — **presentations must be adapted for extreme compression at the source**.

## Two Working Modes

| Mode | Trigger | Input | Output |
| --- | --- | --- | --- |
| **Generate mode** (main) | User gives a topic or outline | Topic / outline points | A guideline-compliant deck generated from scratch |
| **Convert mode** | User gives a web-PPT file path (HTML) | Any HTML slide/page file path (e.g. `my-deck.html`, `slides/intro.html`, or a site page like `levels.html`) | That web-PPT's content turned into a compliant deck |

**Default convention**: output merges into a single-file deck, written to the repo `slides/` directory, named like `slides/<topic-or-page>-deck.html`.

## Compression-Resistant Guidelines Summary

Every generated page must strictly follow the "Compression-Resistant PPT Design" rules in <design.html>. Key points:

- **Only three colors**: pure black `#000000`, mid gray `#808080`, pure white `#FFFFFF` — no color whatsoever
- **Sans-serif only**: Source Han Sans / Microsoft YaHei / Arial; serif fonts like SimSun, KaiTi strictly forbidden
- **Minimum sizes**: body ≥ 24pt, titles recommended ≥ 36pt, mid-gray text ≥ 28pt
- **Lines ≥ 3px**: borders, table rules, chart lines all ≥ 3px; thin lines fracture at 360p
- **Solid backgrounds**: pure white or pure black; gradients, textures, and image watermarks strictly forbidden
- **Zero shadows, zero gradients**: no box-shadow / text-shadow / gradient / 3D effects
- **Charts don't rely on color**: solid black fill + white outline + hatching/dot patterns alternate

Iron rule

Structure may be borrowed; styles must be rebuilt. You may reuse the source page's HTML semantics, but **strictly forbidden to reference** `assets/css/style.css` or `assets/js/main.js` directly — they contain color, shadows, gradients, small text, and thin lines, all violating this standard. Slides must use the skill's embedded standalone stylesheet.

## Call Convention & Examples

When invoking this Skill, pass `arguments` in the following format:

### Generate mode

call examples

```
# topic only; the skill plans the outline
run_skill ppt "topic: team weekly report"

# given an outline, generate page by page per outline point
run_skill ppt "topic: team weekly report; outline: this week's progress, risks and blockers, next week's plan, data dashboard"

# optional extra constraints
run_skill ppt "topic: team weekly report; audience: everyone; pages: about 8"
```

Output: `slides/team-weekly-report-deck.html`

### Convert mode

call examples

```
# convert a given web-PPT
run_skill ppt "convert: my-deck.html"
# output: slides/my-deck-deck.html

# convert a site page as an example (site pages are valid web-PPT inputs too)
run_skill ppt "convert: levels.html"
# output: slides/levels-deck.html
```

## Workflow Essentials

### Generate mode in 5 steps

1. **Break down the input**: distill topic, audience, and key points; with only a topic, plan 5–12 key points (one point ≈ one page)
2. **Plan the page sequence**: cover → table of contents → content pages (one point per page) → closing thanks; rather split one more page than cram one
3. **Generate page by page**: pick a page type (cover/toc/keypoint/table/chart/compare/code/checklist/thanks), apply minimal compliant snippets, and implement each mandatory action (size tiers / three-color / line thickening / no effects / chart compliance / solid backgrounds / no external deps)
4. **Self-check**: run the "3-step self-check" (shrink test / decolor test / thin-line scan) on the most info-dense page
5. **Write out**: save to `slides/<topic>-deck.html`

### Convert mode slicing rules

- **Level-1 slicing**: use the source web-PPT's `<section id="…">` as the unit — one section → one slide
- **Level-2 slicing** (drill down when content is too dense): e.g. a page with L1–L8 gets one slide each, a page with 9 scenarios gets one slide each
- **Stripping**: remove header nav, footer, and inter-page hr/nav (keyboard paging replaces them in slides)
- **Style rebuild**: tables lose shadows, headers go B&W, badges lose color and use text, callouts lose colored borders, code blocks get dark backgrounds with white text

## Self-Test Samples

Sample A — generate mode

On the "Compression-Resistant PPT Design" content of <design.html>, produce a deck in generate mode. Input understood as: `topic: compression-resistant PPT design; outline: fonts and sizes, color and grayscale, layout and whitespace, special elements, three-step self-check`. Expected output `slides/design-deck.html`, about 7 slides. Verify: pure B&W/gray, no shadow or gradient, text ≥ 24pt, lines ≥ 3px, keyboard paging works, fullscreen works.

Sample B — convert mode

Use this site's <levels.html> as the given web-PPT and produce a deck in convert mode. Input: `convert: levels.html`. Expected output `slides/levels-deck.html`, about 10–11 slides. Verify: one slide per L1–L8, tables without shadows and with B&W headers, badges without color and with text, ffmpeg commands on dark code pages, header/footer stripped. Any other web-PPT file works the same way.

## Frequently Asked Questions

**Q:How does this skill relate to design.html?**

design.html is the standard itself — it tells people "how it should be done"; this skill is the standard made executable — it lets an agent "just build it". The standard is the constraint, the skill is the execution. Slides produced by following this skill, at L4/L5 (CRF 34 + stillimage), are as sharp as ordinary decks at CRF 28, with size cut roughly another 40%.

**Q:Can generated slides use color?**

No. The compression-resistant standard mandates exactly three colors (pure black / mid gray / pure white) and forbids all color. To express "distinction", use italics / underlines / pattern fills instead of gray shades or color. This is what keeps slides readable after being compressed to a B&W low-resolution video.

**Q:Can I add animations / transitions?**

No. Slides are static, paged by keyboard (←/→/Space/Home/End/F for fullscreen). After compression, animations and transitions are either lost or become blurry remnants, and they add encoding load. The simpler the picture, the easier the encoder's job and the sharper the result after compression.

**Q:Where do output files go?**

Default output goes to the repo's slides/ directory, named -deck.html — lowercase, spaces as hyphens. Single-file decks (inline CSS + JS) open directly in a browser by double-click.

**Q:How do I use it if my agent has no run\_skill?**

The skill's skill/SKILL.md is a plain-Markdown playbook; any agent can read it and follow along — no specific framework needed. The agent uses its page-type list, templates, and mandatory constraints to generate compliant HTML directly.

## Getting It

This Skill is a pure-Markdown playbook with no runtime dependencies — grab it and go.

| Way | How |
| --- | --- |
| Clone the repo | `git clone https://github.com/brnme/1f6s.git`; the file lives at `skill/SKILL.md` |
| Download directly | On GitHub open `skill/SKILL.md` → Raw → Save As |
| Feed an agent | Paste the `skill/SKILL.md` content into any agent's conversation or system prompt; the agent follows its page-type list and templates to generate a deck |

File location

Repo `skill/SKILL.md` (single file). No installation, no extra dependencies — it's a playbook; an agent that reads it can follow it.

## Summary

The PPT Generation Skill turns "source-side adaptation for extreme compression" from a slogan into a reproducible output: give a topic or a page, get a set of self-contained, presentable slides in pure B&W/gray, big text, thick lines, zero shadows, zero gradients. It complements the [Video Compression Skill](skill-compress.html) — the former makes source slides survive compression, the latter compresses finished video to standard size; together they close the loop from source to finished piece.

Core principle

The simpler the picture, the easier the encoder's job and the sharper the compressed result — an extension of compression-resistant design, and 1f6s's handle at the source.

---

[← Previous: compression-resistant PPT design](design.html)
[Next: video compression skill →](skill-compress.html)
