# Copyright & License · 1f6s

> 1帧6秒倡议 · https://brnme.github.io/1f6s/en/license.html · 本文为 Markdown 镜像,[HTML 原版](license.html)含交互组件。

---

## Copyright & License

The content of this site (all pages — the standard, scenarios, red lines, PPT design, OBS setup, Skills — and companion files) is released under the **Creative Commons Attribution 4.0 International license** (**CC BY 4.0**).

In one sentence

You are free to **share** (copy, distribute, transmit) and **adapt** (remix, transform, build upon) any content on this site for any purpose — including commercial use — **with the only condition of crediting the authors and linking the license**.

## License

| Item | Content |
| --- | --- |
| License name | Creative Commons Attribution 4.0 International |
| Abbreviation | CC BY 4.0 |
| License icon | 🌐 ✍️ 📌 — Attribution |
| Full text | [creativecommons.org/licenses/by/4.0/legalcode](https://creativecommons.org/licenses/by/4.0/legalcode) |
| Human-readable deed | [creativecommons.org/licenses/by/4.0/deed.en](https://creativecommons.org/licenses/by/4.0/deed.en) |

## What You Can Do

Provided you follow the attribution condition, the license grants you these rights:

- **Share** — copy, distribute, and transmit this site's content in any medium
- **Adapt** — remix, transform, or build new works on top of this site's content
- **Use commercially** — for commercial purposes, without asking for further permission
- **No extra permission needed** — the license pre-grants these rights; just honor the attribution condition

Attribution condition (the only requirement)

You must:

- **Credit the authors** — attribute this site's authors: `Han Lie, GLM, DeepSeek, Kimi, Hermes Agent & Reasonix`
- **Provide the license link** — point to [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.en), and indicate whether changes were made
- **Indicate changes** — if you modified, transformed, or built upon the original, note that the original work has been changed

Attribution should be reasonable and must not imply that the author or the licensor endorses you or your use.

## Authors

| Role | Credit | Notes |
| --- | --- | --- |
| Author | **Han Lie** | Originator and principal writer of the "1f6s" video compression initiative |
| Collaborator | **GLM, DeepSeek, Kimi, Hermes Agent & Reasonix** | AI collaboration partners (GLM, DeepSeek, Kimi, Hermes Agent, Reasonix); contributed to writing, code, and site building |

When citing this site, the recommended attribution format is:

recommended attribution format

```
Han Lie, GLM, DeepSeek, Kimi, Hermes Agent & Reasonix, the "1f6s" video compression initiative,
CC BY 4.0, https://github.com/brnme/1f6s
```

About attribution

This site's content was produced jointly by the human author **Han Lie** and the AI collaboration partners **GLM, DeepSeek, Kimi, Hermes Agent & Reasonix**. When attributing, list them all to reflect the human–AI collaborative creation process. The AI-generated portions were integrated into the whole under the human author's direction and review.

## Scope & Exceptions

- **Coverage**: this license covers the text and design of all site pages (`index` / `levels` / `scenarios` / `redlines` / `design` / `obs` / `skill-ppt` / `skill-compress` / `license`) and their companion files (SKILL.md, 1f6s.sh, levels.json, README.md under `skill/`)
- **Trademark**: "1帧6秒" is used as the initiative's name; CC BY 4.0 does not license trademark rights. Referring to the initiative's name is fair reference and not trademark infringement; but please do not publish content contrary to the initiative's intent under the "1帧6秒" name
- **Third-party content**: where pages reference third-party content (e.g. OBS Studio links, platform names), its copyright belongs to the original owners and is outside this license
- **Public domain**: any content already in the public domain before publication on this site remains in the public domain and is not bound by this license

## FFmpeg's Open-Source License

The initiative's 8-level parameters, compression commands, and both Skills are built on **FFmpeg**. FFmpeg is free and open-source software, but its licensing structure is more layered than this site's CC BY 4.0: which "build" you have determines your obligations. Luckily, nearly all "just compress videos with it" scenarios carry near-zero obligations; what needs care is "bundling it into your own product and redistributing".

- **LGPL core, optional GPL components**: the FFmpeg codebase is licensed under **LGPL-2.1-or-later**; some popular components (e.g. the x264 and x265 encoders) are under **GPL-2.0-or-later** and enabled at compile time. Whether a given ffmpeg binary is an LGPL or a GPL build therefore depends on compile options, not how new the version is.
- **Check your build with `-version`**: run `ffmpeg -version` and read the configuration line — `--enable-gpl` means a GPL build (most distro and Homebrew packages fall here because they bundle x264/x265); `--enable-nonfree` (typically with libfdk-aac enabled) means a non-free build that **may not be redistributed**.
- **Command-line use is near-zero obligation**: invoking ffmpeg from a terminal or script — as the initiative's `1f6s.sh` does — producing only video files and never handing ffmpeg itself to anyone, does not trigger the copyleft terms. Personal study, corporate training, and commercial transcoding services can all use it with confidence; the compressed video is not a derivative work of FFmpeg.
- **Patents are a separate matter**: an open-source license grants copyright permission, not a patent license. H.264 and AAC are patent-covered standard codecs; the pools have been reshuffled and consolidated over the years, and most early core patents have expired. Personal use, internal teaching, and distributing the compressed video files are generally fine; for large-scale commercial encoding services or hardware embedding, assess patent licensing yourself — independent of which open-source build you choose.

Obligations at a glance, by how you use it:

| How you use it | License obligations |
| --- | --- |
| Invoke only from a terminal/script; never distribute ffmpeg itself | No extra obligations; the output video is not a derivative work |
| Distribute an LGPL build with your product (separate process or dynamic linking) | Include FFmpeg's copyright notice and the LGPL text, point to where the source can be obtained; if you modified FFmpeg's source, publish the modifications |
| Distribute a GPL build with your product (static linking or bundling) | The derivative work must be opened under GPL as a whole — closed-source commercial products should usually avoid this |
| Distribute a `--enable-nonfree` build | May not be redistributed, period |

One red line

A `--enable-nonfree` build must not be redistributed under any circumstances — if you want to bundle it into your product (even an internal system), stop and check the license first. When a closed-source commercial product needs to integrate FFmpeg, pick an LGPL build and invoke it as a separate process or via dynamic linking; that carries the lightest obligations.

Further reading

FFmpeg's official legal notes on licenses and builds are at [ffmpeg.org/legal](https://ffmpeg.org/legal.html); installation steps are in [the compression Skill · install FFmpeg](skill-compress.html#install). This section is general education, not legal advice; consult a qualified lawyer for major commercial decisions.

## Frequently Asked Questions

**Q:May I move this site's content to my own website / blog / course?**

Yes. Just credit "Authors: Han Lie, GLM, DeepSeek, Kimi, Hermes Agent & Reasonix, License: CC BY 4.0", provide the license link, and note whether changes were made. Commercial use (paid courses, corporate training) is also allowed.

**Q:I modified the content — how should I attribute?**

Credit the original authors "Han Lie, GLM, DeepSeek, Kimi, Hermes Agent & Reasonix" + the CC BY 4.0 link, and add "adapted from the original work". For example: Han Lie, GLM, DeepSeek, Kimi, Hermes Agent & Reasonix, CC BY 4.0, adapted .

**Q:Why CC BY instead of CC BY-NC (non-commercial)?**

The initiative's goal is to be adopted as widely as possible — teams, companies, and platforms can use it directly. A "non-commercial" restriction would make corporate training and paid courses non-compliant, which hurts adoption. CC BY only requires attribution, maximizing spread.

**Q:Are the Skill scripts (1f6s.sh etc.) also under CC BY?**

Yes. SKILL.md, 1f6s.sh, levels.json, and README.md under skill/ are all licensed under CC BY 4.0. You may freely use, modify, and distribute them, as long as you credit the authors and the license. Scripts are literary works, so CC BY applies.

**Q:How should the AI models' output be credited?**

This site is a collaboration between a human author (Han Lie) and AI models (GLM, DeepSeek, Kimi, Hermes Agent, Reasonix). Credit "Han Lie, GLM, DeepSeek, Kimi, Hermes Agent & Reasonix" and you're done. The AI-generated content was integrated into the whole under the human author's direction and review; copyright is uniformly licensed by the authors under CC BY 4.0.

**Q:I compress videos with the initiative's commands — do I need to worry about FFmpeg's GPL?**

No. GPL/LGPL obligations arise only when you "distribute FFmpeg itself, or a program linked to it"; running a command and receiving a video file does not make the output a derivative work of FFmpeg. Most distro builds are indeed GPL builds, but for people who "only use, never redistribute", a GPL build can likewise be used freely for any purpose (including commercial). See FFmpeg's open-source license above for the essentials.

## Summary

"1f6s" is an open initiative — **take it and use it; just credit who made it**. CC BY 4.0 lets the standard, code, and design be freely transmitted and re-created; the only requirement is attributing "Han Lie, GLM, DeepSeek, Kimi, Hermes Agent & Reasonix" and keeping the license link. We hope this standard leaves the repo and enters more teams' workflows.

Core principle

Open, attributed, commercially usable — so the standard gets adopted as widely as possible.

---

[← Previous: video compression skill](skill-compress.html)
[Back to home →](index.html)
