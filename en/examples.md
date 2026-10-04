# Industry Sample Decks · 1f6s

> 1帧6秒倡议 · https://brnme.github.io/1f6s/en/examples.html · 本文为 Markdown 镜像,[HTML 原版](examples.html)含交互组件。

---

## Industry Sample Decks

Starter material for making 1f6s courseware in each industry: every sample is a self-contained, single-file HTML slide deck — open it in a browser to present, drop it into Studio to edit and lint, then compress the recording at the scenario's recommended level. All topics are classic examples, not tied to a grade level, and freely adaptable under CC BY 4.0.

Three steps to use

**① Present**: open any deck in a browser, `→` to page, `F` for fullscreen; **② Adapt**: drop it into <studio.html>, double-click to edit text, run the lint check; **③ Compress**: after screen recording with narration, run `./1f6s.sh lecture.mp4 L5` (default for the MOOC scenario, see [Scenarios](scenarios.html)).

## Education Batch 1 · 8 subjects

[Edu · 01

📐 Math · Quadratic Functions

10 slides: definition and general form, a bar-chart comparison of |a| versus opening width, vertex and axis of symmetry, three forms and a 3-step method. (Chinese deck)

Open deck →](../examples/education/math-deck.html)
[Edu · 02

📖 Chinese · Su Shi's "Shui Diao Ge Tou"

11 slides: the poet's profile and background, the full lyric in large type, stanza-by-stanza analysis, a famous-lines table and a method checklist. (Chinese deck)

Open deck →](../examples/education/chinese-deck.html)
[Edu · 03

🔤 English · Four Core Tenses

11 slides: simple present, simple past, present continuous and present perfect, a side-by-side past-vs-perfect comparison and a signal-words table. (Chinese deck)

Open deck →](../examples/education/english-deck.html)
[Edu · 04

⚛️ Physics · Newton's Three Laws

11 slides: an overview table of the three laws, inertia and common pitfalls, balanced vs interacting forces, a 4-step method and a dark worked-example page. (Chinese deck)

Open deck →](../examples/education/physics-deck.html)
[Edu · 05

🧪 Chemistry · Equations & Balancing

11 slides: conservation of mass, common equations on dark code pages, a balancing walkthrough, a reaction-types table and a pitfall checklist. (Chinese deck)

Open deck →](../examples/education/chemistry-deck.html)
[Edu · 06

🧬 Biology · Cell Structure

10 slides: cell theory, animal vs plant cells, an organelle functions table, prokaryotic vs eukaryotic cells and a review checklist. (Chinese deck)

Open deck →](../examples/education/biology-deck.html)
[Edu · 07

🏛️ History · Imperial Dynasties at a Glance

11 slides: a dynasty timeline table, one landmark event per dynasty, a mnemonic callout and a review checklist. (Chinese deck)

Open deck →](../examples/education/history-deck.html)
[Edu · 08

🌍 Geography · Reading Climate Types

10 slides: how to read a climograph, an annual-precipitation bar chart in black and white, a climate traits table, a 3-step method and confusable pairs. (Chinese deck)

Open deck →](../examples/education/geography-deck.html)

## All Samples

| Subject | Topic | Deck file | Slides | Featured layouts |
| --- | --- | --- | --- | --- |
| Math | Quadratic functions | math-deck.html | 10 | Chart / Table / Compare |
| Chinese | Shui Diao Ge Tou | chinese-deck.html | 11 | Large-type quote / Table / Checklist |
| English | Four core tenses | english-deck.html | 11 | Table / Compare / Checklist |
| Physics | Newton's three laws | physics-deck.html | 11 | Table / Compare / Dark example |
| Chemistry | Equations & balancing | chemistry-deck.html | 11 | Dark code ×2 / Table |
| Biology | Cell structure | biology-deck.html | 10 | Table / Two compares |
| History | Dynasties at a glance | history-deck.html | 11 | Table / Mnemonic callout / Checklist |
| Geography | Reading climate types | geography-deck.html | 10 | Chart / Table / Compare |

## Conventions & Extending

- Location: `examples/{industry}/{topic}-deck.html`; this batch lives in `examples/education/` — see [examples/education/README.md](../examples/education/README.md) for the index and usage guide.
- Every deck embeds the same canonical style as 1f6s Studio: pure black/gray/white, body text ≥24pt, line width ≥3px, zero shadows and zero gradients — all verified by `tools/check_decks.py` and Studio's lint check.
- Formulas and equations are typeset as text (superscript ², subscript ₂), never screenshots; numeric comparisons use black-and-white bars (solid / outlined / hatched fills).
- New industries follow the same directory layout: copy any deck skeleton, replace the content, then run `python3 tools/check_decks.py` to verify.

---

[← Previous: Compress Skill](skill-compress.html)
[Next: Studio →](studio.html)
