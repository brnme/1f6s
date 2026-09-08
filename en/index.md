# 1 Frame / 6 Seconds · Video Compression Initiative for Lectures

> 1帧6秒倡议 · https://brnme.github.io/1f6s/en/index.html · 本文为 Markdown 镜像,[HTML 原版](index.html)含交互组件。

---

FRAME EXTRACTION STANDARD · FPS 1/6

## 1 Frame Every 6 Seconds as the Standard Sampling Rate for Compressing Lecture Videos

Finding the golden balance between how often the picture updates and how much you compress: stretch the interval further and the picture drifts far from the audio; shorten it and you can no longer compress aggressively. 6 seconds is the sweet spot of perception, speech pace, and time-keeping convenience.

v1.0 · Initiative
H.264 / AAC
8 compression levels
9 work scenarios

600*fr*

Total frames per hour

≈17.5*MB*

99-min size · L4 recommended

8*lvl*

Compression levels L1 → L8

9*scn*

Work scenarios covered

## Manifesto

The core value of lecture-style videos (PPT walkthroughs, code demos, desktop operations) lies in the **content**, not **visual fluidity**. When viewers only need to "see what's on this page and hear what's being said", the traditional 30fps high frame rate is pure waste — it re-encodes thousands of nearly identical frames, spending precious bandwidth and storage on pixels with *zero information gain*.

The core claim of the "1 frame / 6 seconds" initiative: **sample one frame every 6 seconds, so the picture only updates when the information actually changes**. This is not cutting corners — it is making encoding resources match the real information density of the content. The companion 8-level compression standard, scenario recommendations, and compression-resistant PPT design guidelines make this idea implementable, reproducible, and consistently executable across a team.

In one sentence

Trade time for space — it only works on content that is "mostly static, delivered by speech"; the moment content depends on continuous motion, emotional delivery, or precise timing, drop this guideline immediately.

## Why 6 Seconds?

While exploring the ultimate compression for lecture videos, we hit a core contradiction: the trade-off between picture update frequency and compression efficiency. After rounds of testing and reasoning, "1 frame / 6 seconds" is the optimal solution.

### 1. Matches human perception

Visual memory of a static picture lasts roughly **4–8 seconds**, and 6 seconds lands right in the middle of that range. Any shorter (e.g. 3–5 s) and the audience is forced to update before they have finished digesting the current slide, adding needless cognitive load; any longer (e.g. 8–10 s), and when the narration has moved to the next point, the picture still shows the previous slide, sharply amplifying the audio-visual mismatch.

6 seconds also matches the natural rhythm of speech. At a normal Mandarin pace (about 150–180 characters/minute), 6 seconds equals roughly **15–18 characters** — just the amount of time needed to read a slide's core title or a key set of figures.

### 2. Advantage over 5 seconds

**Bigger compression gain:** 5 s/frame means 12 frames per minute; 6 s/frame means only 10 — 2 fewer frames per minute, 120 fewer per hour. For a 1-hour video, that reduces the video data by another ~**16.7%**.

**Time-keeping convenience:** 6 is a divisor of both 60 (seconds per minute) and 3600 (seconds per hour). While watching, you only need the seconds digits of the timestamp to quickly figure out which frame you're on — second 6, 12, 18… aligned to the whole second, no mental math. 5 also divides 60, but being odd, 5 is less intuitive in minute–second conversions than the even 6.

### 3. Advantage over 8 seconds and beyond

Past 6 seconds, each extra second brings **diminishing returns** (from 6 s to 8 s, the frame rate only drops from 10 to 7.5 frames/minute — a 25% reduction — yet complaints about audio-video desync rise sharply). 6 seconds is "the longest interval that is still acceptable" — the golden balance between compression efficiency and viewing experience.

### 4. A divisor of 60: low-effort time positioning

Because 6 divides 60, every 10 frames correspond to exactly 1 minute and every 600 frames to 100 minutes. Viewers and editors **only need to look at the seconds digits** to tell "which frame we should be on" — no division required. This is the hidden advantage of 6 over non-divisible intervals like 7 or 9 seconds: in your mental model, time progress is an integer multiple relationship, not decimal arithmetic.

## Measured Compression Comparison

Frame counts and subjective experience at different sampling intervals (based on a 1-hour video):

| Sampling interval | Frames / hour | Compression vs. 6 s | Subjective experience |
| --- | --- | --- | --- |
| 2 s | 1800 | Baseline (smoothest) | Large files; compression pointless |
| 5 s | 720 | ~16.7% smaller | Good experience, awkward arithmetic |
| **6 s** | **600** | **Baseline (recommended)** | **Best balance of experience and compression** |
| 8 s | 450 | 25% smaller still | Noticeable audio-visual gap; not recommended |
| 10 s | 360 | 40% smaller still | Only for very slow speech / purely static PPTs |

## Size Estimator

Enter the video duration (minutes); it is scaled linearly from the 99-minute baseline to estimate size and total frame count for each level. Figures are midpoints of empirical ranges; actual results depend on content complexity.

## Plan Selector

Answer three questions to get a recommended level instantly. The mapping logic follows the scenario quick-reference table.

## Dive Into Each Topic

[Page · 01

8-Level Compression Standard

From the standard level to the extreme H.265 level: L1–L8 parameters, complete ffmpeg commands, expected sizes, and the 2-Pass formula for exact size control.

View the 8 levels →](levels.html)
[Page · 02

Nine Work Scenarios

Email, WeChat, corporate training, public MOOCs, sales demos, compliance audits, offline viewing, platform uploads, batch archiving — a primary and an alternative plan for each.

View scenario matching →](scenarios.html)
[Page · 03

Prohibited Red Lines

Surveillance, film & TV, surgery, sign language, ASMR… explicitly what content must never use 1f6s, plus a one-question "reverse judgment" test.

View the red lines →](redlines.html)
[Page · 04

Compression-Resistant PPT Design

Making slides "survive" black-and-white + low resolution + high CRF at the source: fonts and sizes, a 3-level grayscale palette, layout whitespace, line weights, and a 3-step self-check.

View the PPT guidelines →](design.html)
[Page · 05

OBS Live Streaming & Local Recording Setup

OBS streaming parameters and local recording settings for lecture-style live streams (PPT + voiceover), with GUI steps and advanced settings, plus a post-recording 1f6s transcoding guide.

View the OBS setup →](obs.html)

## Toolbox · Skills

Executable tools shipped with the initiative — standardizing everything from source slides to finished video, plus a streaming configuration guide.

[Skill · 01

🎬 PPT Generation Skill

Generate slides from a topic/outline from scratch, or convert any site page into a compression-compliant HTML slide deck. Self-contained single file, keyboard paging, zero external dependencies.

`run_skill ppt "topic: weekly report"` →](skill-ppt.html)
[Skill · 02

🎞️ Video-to-1f6s Skill

Uses ffmpeg to convert a given video into an 8-level-compliant output. Probes the source first, shows the command, executes after confirmation, and never overwrites the original by default.

`./1f6s.sh lecture.mp4 L4` →](skill-compress.html)
[Related page · 05

📺 OBS Streaming & Recording Setup

OBS streaming parameters and local recording settings for lecture-style streams, with GUI steps and advanced settings, plus a post-recording 1f6s transcoding guide. Same page as "Topics · 05".

Stream 1200kbps + record CRF 18 →](obs.html)

## Ecosystem · Official Implementations

The initiative goes beyond documentation — official services and tooling are being built around the spec, all consuming the single parameter source of truth `spec/levels.json`.

Online service · in development

⚙️ 1f6s Online Conversion Service

Upload a video, the server compresses it per the 8-level spec, and a time-limited download link is delivered by email. Works without an account; built for low-bandwidth regions, with multi-node worker scheduling, credit-based billing, and shared org credit pools.

Publishing platform · in development

📺 1f6s Lecture-Video Hosting

A publishing and distribution platform for videos compressed per the spec: browser-side pre-check + server-side re-verification + manual review, with zero transcode load on the server — a small VPS suffices. Bilingual (EN/中文), aimed at overseas audiences.

[Open-source repository

🧩 GitHub · brnme/1f6s

This site's source and all spec assets: the levels.json parameter source of truth, the 1f6s.sh compression script, and the SKILL.md agent playbook.

One-line install: `curl -fsSL -o 1f6s.sh https://raw.githubusercontent.com/brnme/1f6s/main/skill/1f6s-compress/1f6s.sh` →](https://github.com/brnme/1f6s)

## Terminology Quick Reference

**fps=1/6** — The FFmpeg filter parameter that outputs 1 frame every 6 seconds — i.e. the technical spelling of "1 frame / 6 seconds".

**CRF** — Constant Rate Factor. Higher values mean lower quality and smaller files; 28 is the visually-lossless baseline, anything above 34 counts as heavy compression.

**tune=stillimage** — x264's dedicated tuning for still images/slides: lowers inter-frame prediction weight and strengthens per-frame detail retention — ideal for post-sampling video.

**2-Pass** — Two-pass encoding: the first pass analyzes the whole file's bitrate distribution, the second allocates bits precisely to hit a target — used to "lock in" an exact file size.

**HEVC / H.265** — The next-generation codec: roughly half the size of H.264 at equal quality, but with worse compatibility — confirm player support first.

**480p / 360p** — Vertical pixel count. 480p ≈ 854×480, 360p ≈ 640×360; for lecture content the two are barely distinguishable on a phone screen.

**yuv420p** — Pixel format that guarantees maximum playback compatibility (supported by old devices/browsers) — a required parameter for delivered files.

**scale=-2:480** — Scales proportionally to 480px height; width is computed automatically and forced to an even number (a codec requirement). -2 means "automatic and even".

## Frequently Asked Questions

**Q:Why recommend H.264 by default instead of H.265?**

Compatibility. H.264 plays directly on virtually every device, browser, and player, while H.265 may fail to decode on older Android phones, corporate audit systems, and some web players. The default plan L4 prioritizes "opens wherever it's sent"; H.265 (L8) is only an extreme option once player support is explicitly confirmed.

**Q:Can 8kHz audio really be understood?**

You can clearly hear "what is being said", with a slight metallic tint. 8kHz sampling is telephone-grade: the speech band (300Hz–3.4kHz) is largely preserved, which is enough for phone speakers and noisy environments. If content involves music, tonal nuance, or foreign-language listening practice, fall back to 22.05kHz (L1–L4).

**Q:Why not just send a GIF or plain images?**

GIFs have no audio and a limited palette, so they cannot carry the narration; plain images lose the "watch while listening" time synchronization. The essence of 1f6s is keeping audio's time stream while compressing the picture's time stream — extremely low frame rate for size, while preserving the sense that "when you hear this sentence, you should be looking at that frame".

**Q:Won't the "jumping" picture after sampling be jarring?**

Not for lecture content. Adjacent frames are usually different parts of the same PPT page, or page turns — the audience already expects "look at a page, listen for a while, turn the page". What really feels jarring is audio-video misalignment (picture lagging behind the narration), which is exactly why 6 seconds was chosen over 8 or 10.

**Q:Does this standard suit live-stream recordings?**

Depends on the content. For "PPT + voiceover" style live lectures, yes (just process with L4). For live streams with real-time bullet comments, host facial expressions, or live demonstrations, visual continuity matters — don't. See the "reverse judgment" test on the Red Lines page.

**Q:Some teammates use Mac, some Windows — do parameters change?**

No. The FFmpeg commands are identical on both platforms as long as the FFmpeg versions are close (4.x+ recommended). The only difference is path syntax (Windows replaces /dev/null with NUL ), which matters in L7's 2-Pass first pass.
