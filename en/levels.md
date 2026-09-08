# 8-Level Compression Standard · 1f6s

> 1帧6秒倡议 · https://brnme.github.io/1f6s/en/levels.html · 本文为 Markdown 镜像,[HTML 原版](levels.html)含交互组件。

---

## The 8-Level Compression Standard

The plans below are ordered from least to most aggressive compression, suited to different scenarios (WeChat sending, email attachments, ultra-low-bandwidth transfer, archival backup, etc.). All plans use **H.264 (libx264)** encoding + **AAC audio** for maximum compatibility — except L8 (H.265).

Default recommendation

We recommend **L4** (1 frame/6 s + 480p B&W + CRF 34 + stillimage + 20k audio) as the default standard plan: it strikes the best balance between size (~16–19 MB for 99 minutes) and viewing experience.

## 8-Level Parameter Overview

| Level | Sampling interval | Resolution | Color | Video quality | Audio | Extra tuning | Size for 99 min |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L1 Standard | 1 f / 6 s | 480p | Color | CRF 32 | 20k / 22.05kHz | — | ≈30–35 MB |
| L2 Grayscale | 1 f / 6 s | 480p | B&W | CRF 32 | 20k / 22.05kHz | — | ≈24–28 MB |
| L3 High compression | 1 f / 6 s | 480p | B&W | CRF 34 | 20k / 22.05kHz | — | ≈18–22 MB |
| L4 Smart tuning | 1 f / 6 s | 480p | B&W | CRF 34 | 20k / 22.05kHz | tune=stillimage | ≈16–19 MB |
| L5 Audio extreme | 1 f / 6 s | 480p | B&W | CRF 34 | 8k / 8kHz | tune=stillimage | ≈14–17 MB |
| L6 Long interval | 1 f / 10 s | 360p | B&W | CRF 36 | 8k / 8kHz | tune=stillimage | ≈10–12 MB |
| L7 2-Pass | 1 f / 10 s | 360p | B&W | 2-Pass dynamic | 8k / 8kHz | tune=stillimage | Locked to target |
| L8 H.265 extreme | 1 f / 10 s | 360p | B&W | CRF 38 (x265) | 8k / 8kHz | keyint=1 | ≈6–8 MB |

🟢 L1 Standard

### Quick compression, keeping quality and color

ColorBest compatibility

**Use when:** the client has basic quality requirements and color must be preserved (e.g. chart palettes, UI distinctions).

|  |  |
| --- | --- |
| Picture refresh interval | 1 frame / 6 seconds |
| Resolution | 480p (scale=-2:480) |
| Color | Color |
| Video quality | CRF 32 (H.264) |
| Audio bitrate / sample rate | 20 kbps / 22.05 kHz / mono |
| Extra tuning | None |

bash · ffmpegCopy

```
ffmpeg -i input.mp4 -vf "fps=1/6,scale=-2:480" -c:v libx264 -preset slow -crf 32 -c:a aac -ac 1 -ar 22050 -b:a 20k -pix_fmt yuv420p output_L1.mp4
```

**Expected result:** a 99-minute video ≈ 30–35 MB. Crisp text, complete color, clean voice.

⚫ L2 Grayscale

### Give up color to gain size

B&W20% smaller

**Use when:** the picture is mostly B&W PPTs, code, and text, where color carries no meaning.

|  |  |
| --- | --- |
| Picture refresh interval | 1 frame / 6 seconds |
| Resolution | 480p (scale=-2:480) |
| Color | B&W (format=gray) |
| Video quality | CRF 32 |
| Audio bitrate / sample rate | 20 kbps / 22.05 kHz / mono |
| Extra tuning | None |

bash · ffmpegCopy

```
ffmpeg -i input.mp4 -vf "fps=1/6,scale=-2:480,format=gray" -c:v libx264 -preset slow -crf 32 -c:a aac -ac 1 -ar 22050 -b:a 20k -pix_fmt yuv420p output_L2.mp4
```

**Expected result:** a 99-minute video ≈ 24–28 MB. Text sharpness unchanged; size drops another ~20%.

🟠 L3 High compression

### CRF 34 + B&W

CRF 34Slight grain

**Use when:** you need to compress further and the client accepts some grain in the picture.

|  |  |
| --- | --- |
| Picture refresh interval | 1 frame / 6 seconds |
| Resolution | 480p |
| Color | B&W |
| Video quality | CRF 34 |
| Audio bitrate / sample rate | 20 kbps / 22.05 kHz / mono |
| Extra tuning | None |

bash · ffmpegCopy

```
ffmpeg -i input.mp4 -vf "fps=1/6,scale=-2:480,format=gray" -c:v libx264 -preset slow -crf 34 -c:a aac -ac 1 -ar 22050 -b:a 20k -pix_fmt yuv420p output_L3.mp4
```

**Expected result:** a 99-minute video ≈ 18–22 MB. Large text stays readable; small font edges get slightly blurry.

🔵 L4 Smart tuning

### CRF 34 + B&W + tune=stillimage ★ Default recommended

stillimageBest sharpness

**Use when:** the picture is mostly slides/static charts and you need maximum sharpness at minimum size.

|  |  |
| --- | --- |
| Picture refresh interval | 1 frame / 6 seconds |
| Resolution | 480p |
| Color | B&W |
| Video quality | CRF 34 |
| Audio bitrate / sample rate | 20 kbps / 22.05 kHz / mono |
| Extra tuning | -tune stillimage (slide-specific optimization) |

bash · ffmpegCopy

```
ffmpeg -i input.mp4 -vf "fps=1/6,scale=-2:480,format=gray" -c:v libx264 -preset slow -tune stillimage -crf 34 -c:a aac -ac 1 -ar 22050 -b:a 20k -pix_fmt yuv420p output_L4.mp4
```

**Expected result:** a 99-minute video ≈ 16–19 MB. Sharper text than L3 at the same size.

🟣 L5 Audio extreme

### CRF 34 + B&W + stillimage + 8kHz audio

8k audioPhone-grade sound

**Use when:** bandwidth is extremely low (e.g. 2G/3G networks) and you only need "to hear clearly what is being said".

|  |  |
| --- | --- |
| Picture refresh interval | 1 frame / 6 seconds |
| Resolution | 480p |
| Color | B&W |
| Video quality | CRF 34 |
| Audio bitrate / sample rate | 8 kbps / 8 kHz / mono (phone-grade) |
| Extra tuning | -tune stillimage |

bash · ffmpegCopy

```
ffmpeg -i input.mp4 -vf "fps=1/6,scale=-2:480,format=gray" -c:v libx264 -preset slow -tune stillimage -crf 34 -c:a aac -ac 1 -ar 8000 -b:a 8k -pix_fmt yuv420p output_L5.mp4
```

**Expected result:** a 99-minute video ≈ 14–17 MB. Audio has a slight metallic tint but speech stays intelligible.

🔴 L6 Long interval

### 10 s/frame + 360p + 8kHz

10 s interval360p

**Use when:** you need extreme compression, speech is slow, and the client accepts visible picture jumps.

|  |  |
| --- | --- |
| Picture refresh interval | 1 frame / 10 seconds |
| Resolution | 360p (scale=-2:360) |
| Color | B&W |
| Video quality | CRF 36 |
| Audio bitrate / sample rate | 8 kbps / 8 kHz |
| Extra tuning | -tune stillimage |

bash · ffmpegCopy

```
ffmpeg -i input.mp4 -vf "fps=1/10,scale=-2:360,format=gray" -c:v libx264 -preset slow -tune stillimage -crf 36 -c:a aac -ac 1 -ar 8000 -b:a 8k -pix_fmt yuv420p output_L6.mp4
```

**Expected result:** a 99-minute video ≈ 10–12 MB. Only suitable for small phone screens; large headings remain legible.

⚪ L7 2-Pass precise control

### Lock in the exact target size

2-PassExact size

**Use when:** the client explicitly demands "the file must be under XX MB" and you need precise output-size control.

|  |  |
| --- | --- |
| Picture refresh interval | 1 frame / 10 seconds |
| Resolution | 360p |
| Color | B&W |
| Encoding mode | 2-Pass (two-pass encoding) |
| Video bitrate | Computed from the target size |
| Audio bitrate / sample rate | 8 kbps / 8 kHz |
| Extra tuning | -tune stillimage |

#### How to compute it

1. Target size (MB) → total bitrate (kbps) = target (MB) × 8192 / duration (seconds)
2. Video bitrate = total bitrate − audio bitrate (8 kbps)
3. Pass 1 analyzes, Pass 2 outputs

Example below: 99 minutes into 8MB (video bitrate ≈ 3k):

bash · pass 1 analyzeCopy

```
# pass 1
ffmpeg -i input.mp4 -vf "fps=1/10,scale=-2:360,format=gray" -c:v libx264 -preset slow -tune stillimage -b:v 3k -pass 1 -f mp4 /dev/null
```

bash · pass 2 outputCopy

```
# pass 2
ffmpeg -i input.mp4 -vf "fps=1/10,scale=-2:360,format=gray" -c:v libx264 -preset slow -tune stillimage -b:v 3k -pass 2 -c:a aac -ac 1 -ar 8000 -b:a 8k -pix_fmt yuv420p output_L7.mp4
```

Windows note

In pass 1, replace `/dev/null` with `NUL` on Windows.

⚫ L8 H.265 extreme

### Trading compatibility for extreme size

libx265Confirm support

**Use when:** the client uses modern players (VLC, PotPlayer, etc.) and does not rely on the OS's native decoding.

|  |  |
| --- | --- |
| Encoder | libx265 (H.265/HEVC) |
| Picture refresh interval | 1 frame / 10 seconds |
| Resolution | 360p |
| Color | B&W |
| Video quality | CRF 38 |
| Audio bitrate / sample rate | 8 kbps / 8 kHz |
| Extra tuning | keyint=1 (every frame is a keyframe) |

bash · ffmpegCopy

```
ffmpeg -i input.mp4 -vf "fps=1/10,scale=-2:360,format=gray" -c:v libx265 -preset slow -crf 38 -x265-params "keyint=1:min-keyint=1" -c:a aac -ac 1 -ar 8000 -b:a 8k -pix_fmt yuv420p output_L8.mp4
```

Compatibility warning

Expected result: a 99-minute video ≈ 6–8 MB, quality close to L6 at half the size. **You must confirm the client player supports H.265**, otherwise they won't be able to play it.

## Closing Words

The value of this standard is **standardization** — a consistent team-wide baseline so parameters are not renegotiated every time, and any member can quickly produce outputs with consistent quality and controlled size.

Final advice

Adopt this initiative as a team operating standard, train new hires on it, and keep video output consistent. As new scenarios arise, extend with additional levels built on this foundation.

All plans above have been tested and verified; they are ready for production use.

---

[← Back to home](index.html)
[Next: nine work scenarios →](scenarios.html)
