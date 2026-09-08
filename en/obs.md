# OBS Live Streaming & Local Recording Setup · 1f6s

> 1帧6秒倡议 · https://brnme.github.io/1f6s/en/obs.html · 本文为 Markdown 镜像,[HTML 原版](obs.html)含交互组件。

---

## OBS Live Streaming & Local Recording Setup

This page applies the "1f6s" philosophy to two OBS Studio scenarios: **live streaming** and **local recording**. It covers only **"PPT + voiceover / screen-share" style lecture streams and screen recordings** — exactly the content the 1f6s initiative considers suitable.

How to use

First use the "suitability check" below to confirm your content is lecture-style; then pick one of the two paths: go live → see **streaming setup**; keep a recording → see **local recording setup**. The parameters are very different — don't mix them.

## Suitability Check: which type is your stream/recording?

The essence of 1f6s is "trade time for space" — it only fits content with low information density and slowly changing pictures. Before going live or recording, use the reverse-judgment test to sort yourself quickly:

| Your content's characteristics | Type | Applicable here? | What to do |
| --- | --- | --- | --- |
| PPT walkthroughs, desktop operation demos, screen-share lectures, code walkthroughs — picture mostly static/page-turning, core information carried by **speech** | Lecture-style | **Yes** | Keep reading this page |
| Real-time bullet comments, host facial close-ups, live physical demos, gesture/body-language-rich streams | Interactive demo | **No** | Use OBS's normal high frame rate; 1f6s destroys visual continuity — see [Red Lines](redlines.html) |

Red-line reminder

If your stream includes **live demonstration moves, host facial expressions, or body language while answering comments**, picture continuity is itself part of the value. Forcing 1 frame/6 seconds turns the stream into a "PPT pager" — **drop this standard** and use OBS's default 30fps streaming.

## I. Live Streaming Setup

Streaming is **real-time**: bounded by upload bandwidth, and platforms re-transcode your stream. A key insight here: **you cannot simply apply 1f6s frame sampling to a live stream**.

Core principle: stream at regular low bitrate; keep extreme compression for post-recording transcoding

Streaming protocols (RTMP/SRT/WebRTC) require **keyframe intervals and frame rates that match platform specs**. If you push the frame rate down to 1 frame/6 seconds and set a 6-second keyframe interval, viewers get severe buffering and artifacts — some platforms even refuse the stream. The right approach: **stream with OBS's regular low-bitrate settings (600–1200kbps is plenty clear for lecture-style content), and leave 1f6s's extreme compression to "post-recording transcoding" or "local recording at low bitrate"** (see section II).

### Scenario characteristics

- Real-time transport, bounded by upload bandwidth (home uploads are often only 1/5–1/10 of download)
- Platforms (Bilibili/Douyin/YouTube) **re-transcode** the stream; a poor source gets further degraded
- Lecture footage changes slowly — naturally suited to low bitrate, but not to low frame rate (streams require continuous frames)

### GUI steps (OBS Studio, Settings → Output)

Fill in via OBS "Settings → Output → Output Mode: Advanced". Recommended lecture-style streaming parameters:

| Setting | Recommended value | Notes |
| --- | --- | --- |
| Output mode | Advanced | Exposes full parameter control |
| Encoder (video) | x264 (no discrete GPU) / NVIDIA NVENC H.264 (NVIDIA GPU) | Prefer NVENC with a discrete GPU to save CPU; use x264 (software encoding) otherwise |
| Rate control | CBR | Streaming requires CBR (constant bitrate); platforms schedule on stable bitrate, VBR tends to stutter |
| Bitrate | 600–1200 kbps | Lecture footage is mostly static — far below platform caps (Bilibili ≤6000, Douyin ≤4000); 2Mbps upload pushes 1200kbps steadily |
| Keyframe interval | 2 seconds | **Universal platform requirement**; must match the platform (see notes below) |
| Preset (x264) | veryfast or fast | Streaming favors real-time; fast presets cut encode latency; NVENC: pick "Quality" or "Low Latency" |
| Resolution (Video → Output (Scaled) Resolution) | 1280×720 (720p) or 854×480 (480p) | Lecture 480p text is legible; drop to 480p when upload is tight; keep base resolution native |
| FPS (Video) | 30 FPS | Standard streaming frame rate — don't lower (streams cannot be frame-sampled) |
| Audio bitrate (Output → Audio) | 96–128 kbps | AAC; 96kbps keeps lecture voice clean |
| Audio sample rate | 48 kHz | Streaming standard; don't lower |

#### Settings → Stream (service and stream key)

- **Service**: pick the matching platform (Bilibili/Douyin/YouTube etc.) or "Custom"
- **Server**: enter the platform's ingest URL (e.g. `rtmp://live-push.example.com/app`)
- **Stream key**: your room's stream code (never leak it)

**Q:Advanced parameters (x264 tuning, bitrate math, why streaming can't be frame-sampled)**

x264 advanced options (Settings → Output → Streaming → Advanced) Paste the following into the "x264 Options" box (lecture-stream tuning): x264 options string keyint=60:min-keyint=60:scenecut=0:tune=zerolatency:profile=main keyint=60:min-keyint=60 : at 30fps, 2 seconds = 60 frames, aligned with the 2s keyframe interval; scenecut=0 disables scene-cut adaptive keyframes so keyframes stay strictly equidistant tune=zerolatency : low-latency tuning for streaming (note: this differs from recording's tune=stillimage — streaming prioritizes latency, recording prioritizes quality) profile=main : best compatibility — baseline lacks quality, high strains old-device decoding NVENC users: after selecting NVENC as encoder, independent "Preset", "Rate Control", and "Keyframe Interval" options appear below — no x264 string needed Bitrate and upload bandwidth math Stream bitrate + audio bitrate + protocol overhead ≈ actual upload usage. Rule of thumb: keep 30% headroom for network fluctuation. 1200kbps video + 96kbps audio ≈ 1.3Mbps; recommend upload ≥ 1.7Mbps 600kbps video + 96kbps audio ≈ 0.7Mbps; recommend upload ≥ 0.9Mbps (works on a 4G hotspot) Test upload: check speedtest.net ; 1MB/s = 8Mbps, plenty for 1200kbps streaming Why a stream cannot be frame-sampled (technical explanation) Platform transcoding servers assume the stream is continuous-frame-rate (usually 30/60fps). They slice HLS segments at a fixed keyframe interval (usually 2 seconds) and generate multiple bitrate ladders. If you push 1 frame/6 s: A 6s keyframe interval → the slicer, cutting at 2s, hits P-frames constantly → segment artifacts Frame rate 0.17fps → viewer players decode at 30fps and repeat each frame ~180 times, while buffers may judge the stream dead from the long frame gap and reconnect Some platforms outright refuse streams below 10fps Conclusion: keep 30fps + 2s keyframes + low bitrate on the stream side; hand the extreme compression to post-processing.

## II. Local Recording Setup

Recording has no real-time bandwidth pressure and can be transcoded offline — **this is where 1f6s's extreme compression is directly usable**. Two paths, choose by your workflow:

### Path comparison

| Path | Approach | Pros | Cons |
| --- | --- | --- | --- |
| **Path A (recommended)** Record high-quality source → transcode with 1f6s | OBS records a high-bitrate source; afterwards use ffmpeg/skill to transcode to L4 etc. | Source is reusable (editing/re-encoding/archiving); transcode parameters controllable; fully aligned with the initiative; supports 2-Pass size locking | One extra transcoding step; needs temporary disk space for the source |
| Path B OBS records straight to low bitrate | In OBS Output → Recording, set low bitrate/reduced resolution directly while recording | Saves a step; compressed result right after recording | Parameters less flexible than ffmpeg; no 2-Pass size locking; a botched recording can't be recovered from a source |

### Path A: record a high-quality source (OBS settings)

Goal: record a high-quality source file for later 1f6s transcoding. Settings → Output → Output Mode: Advanced → **Recording** tab:

| Setting | Recommended value | Notes |
| --- | --- | --- |
| Recording format | MKV | Fault-tolerant (an interrupted recording doesn't lose the whole file); can tick "Automatically remux to MP4" under Settings → Advanced → Recording afterwards |
| Video encoder | x264 or NVENC H.264 | Use H.264 for the source so later ffmpeg transcoding is smooth |
| Rate control | CRF (recommend CRF 18–23) or VBR | The source should be "near-lossless" with headroom: CRF 18 is nearly lossless, 23 visually lossless; if CBR, set 2500–4000kbps |
| Bitrate (if CBR) | 2500–4000 kbps | Leaves ample source quality for transcoding; 4000kbps is already very clear for lecture content |
| Keyframe interval | 2 seconds | Keep default, convenient for later editing |
| Preset (x264) | medium or slow | Recording is not real-time; slower presets trade time for quality |
| Resolution | Native (e.g. 1920×1080) | Keep full resolution in the source; scale to 480p/360p during transcoding |
| FPS | 30 FPS | Standard; keep normal frame rate in the source, sample it down during transcoding |
| Audio bitrate | 128–160 kbps / 48kHz | Keep audio headroom in the source; compress to 20k/8k during transcoding |

After recording, transcode with 1f6s (see [post-recording transcoding guide](#transcode)).

### Path B: OBS records directly at low bitrate (compress while recording)

Goal: compress while recording — the result is already in 1f6s style. Settings → Output → Output Mode: Advanced → **Recording** tab:

| Setting | Recommended value | Notes |
| --- | --- | --- |
| Recording format | MP4 or MKV | MP4 for direct delivery; MKV if you fear interruptions (then remux) |
| Video encoder | x264 | So you can directly apply `tune=stillimage` |
| Rate control | CRF 34 | Matches 1f6s L4/L5's CRF value; or CBR 300–500kbps (extreme low bitrate for lectures) |
| Bitrate (if CBR) | 300–500 kbps | At 480p B&W, 300kbps still keeps text legible for lectures |
| Keyframe interval | 2 seconds | Keep default |
| Preset (x264) | medium | Balance quality vs. encoding load |
| Resolution (Scaled Resolution) | 854×480 (480p) | Matches 1f6s L1–L5 resolution; drop to 640×360 (360p) on extremely low bandwidth |
| FPS | 30 FPS | OBS cannot frame-sample to 1 frame/6 s while recording (that's ffmpeg post-processing); keep 30fps and reduce size via CRF/bitrate + resolution |
| Audio bitrate | 48–96 kbps / 48kHz | OBS can't easily set 8kHz; 48kbps is a safe floor; leave extreme compression to post-processing |

Path B's limits

OBS recording **cannot do 1 frame/6 s sampling while recording** (fps=1/6 is an ffmpeg filter; OBS has no equivalent option), nor can it 2-Pass lock a size. Path B can only approach 1f6s on the "bitrate/resolution/CRF" axes — **true extreme compression still requires Path A's post-recording transcode**. If you want the initiative's full parameter set (sampling + 8k audio + 2-Pass), go with Path A.

**Q:Advanced parameters (custom FFmpeg output, MKV remux, grayscale filter)**

OBS custom FFmpeg output (Settings → Output → Output Mode: Advanced → Recording format: "Custom FFmpeg output") To apply tune=stillimage or a grayscale filter while recording, configure the "Custom FFmpeg Output": Video encoder : libx264 Video parameters (FFmpeg options box) : -preset slow -tune stillimage -crf 34 -pix\_fmt yuv420p Video filter (optional, to B&W) : format=gray (can be added for lectures to shrink size further) Audio encoder : aac , parameters: -ac 1 -ar 22050 -b:a 20k (aligns with L4 audio) Note: OBS custom FFmpeg output still cannot set fps=1/6 sampling (the recording source is a real-time stream) — sampling can only happen in post-processing. Remuxing an MKV recording to MP4 Path A records MKV for safety; before delivery you can remux losslessly (no re-encode, completes in seconds): bash · ffmpeg lossless remux ffmpeg -i recording.mkv -c copy -movflags +faststart recording.mp4 Grayscale filter (Path B advanced) In OBS's normal recording mode (non-custom FFmpeg), right-click the video/display capture in "Sources" → Filters → Add "Video Processing Filter" → pick "Grayscale" to get B&W, equivalent to format=gray .

## Streaming vs. Recording Parameter Quick Reference

See the differences at a glance and avoid mixing them up:

| Parameter | Streaming (live) | Recording Path A (high-quality source) | Recording Path B (compress while recording) |
| --- | --- | --- | --- |
| FPS | 30 FPS (can't lower) | 30 FPS | 30 FPS (OBS can't sample frames) |
| Keyframe interval | 2 s (platform requirement) | 2 s | 2 s |
| Rate control | CBR | CRF 18–23 | CRF 34 or CBR 300–500k |
| Video bitrate | 600–1200 kbps | 2500–4000 kbps | 300–500 kbps |
| Resolution | 720p / 480p | Native | 480p / 360p |
| Sampling (fps=1/6) | **No** | During transcoding | **No** (requires post-processing) |
| tune | zerolatency | — | stillimage |
| Audio bitrate | 96–128 kbps / 48kHz | 128–160 kbps / 48kHz | 48–96 kbps / 48kHz |
| 2-Pass size lock | No | During transcoding (L7) | No |
| Format | Platform ingest | MKV (source) | MP4 / MKV |

## Post-Recording Transcoding Guide (1f6s in practice)

After recording the source with Path A, transcode it with the 1f6s tool to get standard initiative output. Two ways:

### Way 1: the 1f6s script (recommended)

The repo ships `skill/1f6s-compress/1f6s.sh` — one command probes and transcodes:

bash · default L4 compression

```
# default: L4 (1 frame/6 s + 480p B&W + CRF 34 + stillimage)
./skill/1f6s-compress/1f6s.sh recording.mp4

# specify a level
./skill/1f6s-compress/1f6s.sh recording.mp4 L4 -y

# L7 locks the target size (e.g. 8MB)
./skill/1f6s-compress/1f6s.sh recording.mp4 L7 --target 8 -y
```

The output defaults to `recording_1f6s.mp4` and never overwrites the source. See the [1f6s tool README](../skill/1f6s-compress/README.md).

### Way 2: direct ffmpeg commands

The complete commands from the [8-level standard](levels.html); the most-used L4:

bash · ffmpeg L4

```
ffmpeg -i recording.mp4 -vf "fps=1/6,scale=-2:480,format=gray" -c:v libx264 -preset slow -tune stillimage -crf 34 -c:a aac -ac 1 -ar 22050 -b:a 20k -pix_fmt yuv420p recording_1f6s.mp4
```

Recommended workflow

**Stream live (low bitrate ~1200kbps) while recording locally (Path A, CRF 18 high-quality source)** — one live event yields three outputs: ① the stream viewers watch in real time; ② the finished source; ③ the source transcoded with 1f6s for archiving/distribution. The three parameter sets don't interfere — this is the optimal workflow for lecture-style live streaming.

## Frequently Asked Questions

**Q:Why can't a stream be sampled directly to 1 frame/6 s?**

Streaming protocols (RTMP/SRT) and platform transcoders assume continuous frame rates (30/60fps) and slice at fixed keyframe intervals (usually 2s). 1 frame/6 s makes the slicer hit non-keyframes constantly, causing artifacts; player buffers may also declare the stream dead from overlong frame gaps and reconnect; some platforms outright reject very low frame rates. Keep 30fps on the stream; do the sampling in post-processing .

**Q:Why is the keyframe interval 2 seconds instead of 6?**

2 seconds is a universal platform requirement (Bilibili, Douyin, YouTube all use it) — platforms slice HLS segments on it. A 6s keyframe interval makes segments too long: higher first-frame latency for viewers and sluggish seeking. 1f6s's "6 seconds" is the sampling interval (picture update frequency); a streaming keyframe interval is a different concept — don't mix them.

**Q:MKV or MP4 for recording?**

Prefer MKV while recording — if OBS crashes or power dies, the MKV is still recoverable; an MP4 damaged by a non-clean close loses the whole file. OBS can auto-remux to MP4 after recording (Settings → Advanced → Recording → tick "Automatically remux", format MP4). Use MP4 for delivery/distribution (best compatibility).

**Q:NVENC or x264?**

With an NVIDIA GPU use NVENC (hardware encoding) — saves CPU and keeps games/apps smooth while streaming; without one, or for maximum quality, use x264 (software encoding), which is slightly better at equal bitrate. For lecture streams the two are comparable — pick whichever lightens your system load. Note: when transcoding with 1f6s/ffmpeg, always use libx264 , regardless of the OBS choice.

**Q:Does the recorded source still need compressing?**

Depends on the use. Archive / distribute / send → transcode with 1f6s to L4/L7 (16–19MB / 8MB); later editing → keep the source untouched; platform upload → use the L1 color version (platforms re-transcode; don't start too low). Keep one source copy in cold storage and distribute the compressed version daily.

## Getting it

This page is an OBS setup guide — follow the GUI steps in OBS Studio directly, no extra files needed. The 1f6s tool used for post-recording transcoding comes from the repo:

| Way | How |
| --- | --- |
| Clone the repo | `git clone https://github.com/brnme/1f6s.git`; the transcoding tool lives in `skill/1f6s-compress/` |
| Use the script directly | After cloning, `chmod +x skill/1f6s-compress/1f6s.sh`, then `./skill/1f6s-compress/1f6s.sh recording.mp4 L4` compresses the recording to standard size |
| OBS itself | Download OBS Studio (free, open source) from [obsproject.com](https://obsproject.com); the steps here are based on OBS 30.x |

Dependencies

OBS Studio (free) + ffmpeg/ffprobe (needed for transcoding, ships with ffmpeg). The GUI steps here need no command line; only post-recording transcoding uses `skill/1f6s-compress/1f6s.sh`.

## Summary

OBS setup for lecture streams and screen recordings boils down to **knowing the real-time vs. offline boundary**: streaming wants stable continuity (30fps + low bitrate + 2s keyframes); extreme compression goes to post-recording transcoding (1f6s sampling + grayscale + stillimage). The parameter sets don't interfere — one live event can simultaneously produce a stream and an archivable source.

Core principle

No sampling on the stream; keep the source for recordings; transcode with 1f6s — real-time stays continuous, offline stays extreme.

---

[← Previous: nine work scenarios](scenarios.html)
[Next: prohibited red lines →](redlines.html)
