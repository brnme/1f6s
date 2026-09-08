# Video-to-1f6s Skill · 1f6s

> 1帧6秒倡议 · https://brnme.github.io/1f6s/en/skill-compress.html · 本文为 Markdown 镜像,[HTML 原版](skill-compress.html)含交互组件。

---

## Video-to-1f6s Skill

Given a video, use **ffmpeg** to convert it into an output matching one of the "1f6s" 8-level compression standards. Given a video path and level (default L4), it **probes the source first, shows the command that will run, and only executes after confirmation**; the output defaults to `<basename>_1f6s.mp4` and **never overwrites the original**.

What it is

A shareable toolkit for any agent and humans (`skill/1f6s-compress/`): a playbook for agents (`SKILL.md`) plus a shell wrapper for direct execution (`1f6s.sh`). It encodes the initiative's 8-level parameters into a machine-readable `levels.json` shared by the script and the agent, keeping parameters from drifting.

## 8-Level Parameter Quick Reference

Full parameters and ffmpeg commands are on the [8-level standard page](levels.html). This skill treats `levels.json` as the single source of truth:

| Level | Name | Sampling | Resolution | Color | Video | Audio | Tuning | Size for 99 min |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L1 | Standard | 1 f/6 s | 480p | Color | CRF 32 | 20k/22050 | — | ≈30–35 MB |
| L2 | Grayscale | 1 f/6 s | 480p | B&W | CRF 32 | 20k/22050 | — | ≈24–28 MB |
| L3 | High compression | 1 f/6 s | 480p | B&W | CRF 34 | 20k/22050 | — | ≈18–22 MB |
| **L4** | **Smart tuning ★default** | 1 f/6 s | 480p | B&W | CRF 34 | 20k/22050 | stillimage | ≈16–19 MB |
| L5 | Audio extreme | 1 f/6 s | 480p | B&W | CRF 34 | 8k/8000 | stillimage | ≈14–17 MB |
| L6 | Long interval | 1 f/10 s | 360p | B&W | CRF 36 | 8k/8000 | stillimage | ≈10–12 MB |
| L7 | 2-Pass | 1 f/10 s | 360p | B&W | 2-Pass | 8k/8000 | stillimage | Locked to target |
| L8 | H.265 extreme | 1 f/10 s | 360p | B&W | CRF 38 | 8k/8000 | keyint=1 | ≈6–8 MB |

## How to Use

### Script path (humans or agents executing directly)

bash · 1f6s.sh

```
# default L4 compression (shows the command first, runs after confirmation)
./skill/1f6s-compress/1f6s.sh lecture.mp4

# specify a level + skip confirmation
./skill/1f6s-compress/1f6s.sh lecture.mp4 L4 -y

# L7 locks the target size (8MB)
./skill/1f6s-compress/1f6s.sh lecture.mp4 L7 --target 8 -y

# show the command that would run, without actually compressing
./skill/1f6s-compress/1f6s.sh lecture.mp4 L6 --dry-run

# print the 8-level quick reference
./skill/1f6s-compress/1f6s.sh --list
```

### Agent path (read the playbook)

An agent reads `skill/1f6s-compress/SKILL.md` and executes per the `arguments` convention:

call examples

```
# default L4
run_skill 1f6s-compress "video: lecture.mp4"

# L7 locking 8MB
run_skill 1f6s-compress "video: lecture.mp4; level: L7; target: 8MB; yes"

# generate the command only, don't execute
run_skill 1f6s-compress "video: lecture.mp4; level: L6; dry-run"
```

### Command-line options

| Option | Description |
| --- | --- |
| `-o, --output <path>` | Custom output filename/path |
| `-y, --yes` | Skip confirmation and execute directly |
| `-n, --dry-run` | Only print the command that would run, don't execute |
| `-l, --list` | Print the 8-level parameter table and exit |
| `--target <MB>` | L7 target size (MB); the video bitrate is computed automatically |
| `--force` | Allow overwriting an existing output file |
| `-h, --help` | Show help |

## Core Features

- **Show first, then execute**: ffprobe probes the source (duration/resolution/codec/size) → prints the selected level's parameters + the full command + expected output → runs after the user confirms `y` (`-y` skips)
- **Never overwrites the original by default**: output named `<basename>_1f6s.mp4` in the source's directory; refuses if the output already exists (needs `--force`); refuses whenever the output path equals the source video
- **Full 8-level coverage**: all L1–L8 parameters come from `levels.json` (matching <levels.html>); L4 is the default recommendation
- **L7 two-pass**: computes the video bitrate automatically via `target size × 8192 / duration − audio bitrate`, runs both passes, and cleans up `ffmpeg2pass-*.log*` automatically
- **L8 H.265**: includes `keyint=1:min-keyint=1`; warns about compatibility risk before running
- **Platform adaptation**: `/dev/null` → `NUL` detected automatically (Windows)
- **Dependency fallback**: parses JSON with `python3` when `jq` is missing; only errors out when neither is available

## Execution Flow

1. **Validate input**: confirm the video file exists and ffmpeg + ffprobe are available
2. **Determine level**: parse the level from arguments (default L4), target size (L7 only), and output path (optional)
3. **Probe the source**: ffprobe fetches duration, resolution, codec, and size
4. **Fetch parameters**: read all parameters for the level from `levels.json`
5. **Build the command**: assemble the ffmpeg command; for L7 compute the video bitrate from the formula and generate both pass commands
6. **Show**: print source info + level parameters + full command + expected output filename
7. **Execute after confirmation**: waits for the user by default; runs directly when `yes` is passed
8. **Verify and report**: ffprobe confirms the output is recognizable; print the output size and compare to the level's expectation

## File List

| File | Purpose |
| --- | --- |
| `skill/1f6s-compress/SKILL.md` | Agent playbook: guidelines summary + parameter table + execution flow + call convention + mandatory constraints + self-test samples |
| `skill/1f6s-compress/1f6s.sh` | Companion wrapper script: the execution entry point shared by humans and agents (executable) |
| `skill/1f6s-compress/levels.json` | Machine-readable 8-level parameter table (single source of truth for script and agent) |
| `skill/1f6s-compress/README.md` | Human-oriented quick start: dependencies/examples/quick reference/FAQ |

## Frequently Asked Questions

**Q:Why L4 by default?**

It strikes the best balance between size (~16–19 MB for 99 minutes) and viewing experience: -tune stillimage keeps static slide text sharper, and 20k/22050 audio keeps the voice clean. Unless you have a special need (color → L1, locked size → L7, extreme size → L8), just use L4.

**Q:Why convert to B&W by default?**

Color in lecture videos adds almost no understanding value; converting to B&W ( format=gray ) cuts size by roughly another 20%. If color must be preserved (chart palettes, UI distinctions), use L1.

**Q:Why 6 seconds?**

It's the standard sampling rate of the "1f6s" initiative — lecture footage changes slowly; one frame every 6 seconds is enough to keep pace with page turns while massively cutting bitrate. For slower speech and even less change, use L6/L7/L8's 1 frame/10 s. See Why 6 seconds .

**Q:How does L7 lock the size?**

2-Pass encoding. Formula: total bitrate = target size (MB) × 8192 / duration (seconds) , video bitrate = total bitrate − audio bitrate (8) . Pass 1 analyzes ( -pass 1 -an -f mp4 /dev/null , NUL on Windows), pass 2 outputs ( -pass 2 ). The script computes the bitrate, runs both passes, and cleans up the logs automatically.

**Q:Will it overwrite my original video?**

No. Output defaults to \_1f6s.mp4 in the same directory as the source. Even if an output with the same name exists, the script refuses and suggests --force to overwrite or -o to rename.

## Getting It

This Skill is a toolkit folder — an agent playbook plus an executable shell script; grab it and go.

| Way | How |
| --- | --- |
| Clone the repo | `git clone https://github.com/brnme/1f6s.git`; files live in `skill/1f6s-compress/` |
| Use the script directly | After cloning, `chmod +x skill/1f6s-compress/1f6s.sh`, then `./skill/1f6s-compress/1f6s.sh video.mp4 L4` compresses in one line |
| Feed an agent | Hand `skill/1f6s-compress/SKILL.md` to any agent; the agent executes per the call convention, or directly invokes `1f6s.sh` |

Files & dependencies

Repo `skill/1f6s-compress/` (contains `SKILL.md` / `1f6s.sh` / `levels.json` / `README.md`). Running the script needs ffmpeg + ffprobe; parsing `levels.json` needs jq or python3 (either works; the script degrades automatically when one is missing).

## Summary

The Video-to-1f6s Skill is the initiative's **executable landing**: give a video path and level, get an 8-level-compliant compressed output. It complements the [PPT Generation Skill](skill-ppt.html) — the former compresses finished video to standard size, the latter makes source slides survive compression. Together they close the loop from source to finished piece.

Core principle

levels.json as the single parameter source; show first, execute after confirmation; never overwrite the original — making the initiative's 8-level standard usable by everyone and executable by agents.

---

[← Previous: PPT generation skill](skill-ppt.html)
[Next: OBS setup →](obs.html)
