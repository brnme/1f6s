# Nine Work Scenarios · 1f6s

> 1帧6秒倡议 · https://brnme.github.io/1f6s/en/scenarios.html · 本文为 Markdown 镜像,[HTML 原版](scenarios.html)含交互组件。

---

## Nine Work Scenarios

Playback environment, receiving devices, network conditions, and client expectations differ wildly across scenarios. One compression plan cannot fit everything — standardization is not one-size-fits-all, but a clear decision path.

How to use

Locate your scenario, look up the "primary/alternative" plan numbers, then get the matching ffmpeg command from the [8-level standard page](levels.html). Each section ends with "operational advice", covering delivery wording and cautions.

### 📧Scenario 1: Email attachment delivery

**Characteristics:**

- Mainstream mail providers cap attachments around 20–25 MB (see comparison table below); some domestic basic plans go as low as 15 MB
- Clients usually download and watch on a desktop with a high-resolution screen
- Email transfer speed is directly affected by attachment size

**📊 Mainstream email attachment limits** (taking each provider's smallest / basic limit, sorted from smallest to largest)

| Provider | Minimum attachment limit | Notes |
| --- | --- | --- |
| Wo Mail (China Unicom) | **15 MB** | Basic plan; premium plans reach 2 GB |
| NetEase Mail (163/126) | **20 MB** | Official help center says 20 MB; some versions allow 50 MB |
| 139 Mail (China Mobile) | **20 MB** | Low-tier plan 20 MB; high-tier up to 50 MB |
| Outlook.com / Hotmail | **20 MB** | Oversized files prompt sharing via OneDrive |
| iCloud Mail | **20 MB** | Mail Drop can send temporary links up to 5 GB |
| Zoho Mail | **20 MB** | Free tier; paid plans raise the limit |
| GMX (free) | **20 MB** | Some versions allow 50 MB |
| Gmail | **25 MB** | Larger files auto-convert to Google Drive links |
| Yahoo Mail | **25 MB** | Hard limit; no automatic cloud conversion |
| Proton Mail | **25 MB** | Known for encryption and privacy |
| AOL Mail | **25 MB** | — |
| Mail.com | **30 MB** | — |
| QQ Mail | **50 MB** | Single regular attachment ≤50 MB; whole email ≤55 MB |
| Sina Mail | **50 MB** | — |
| Sohu Mail | **50 MB** | — |
| Fastmail | **50 MB** | One of the mainstream providers with a higher bar |

Key takeaway

Among 16 mainstream providers, **11 have minimum attachment limits clustered at 15–25 MB** (Wo Mail's 15 MB is the lowest; Outlook / iCloud / NetEase / Zoho / GMX etc. at 20 MB; Gmail / Yahoo / Proton / AOL at 25 MB), and only QQ / Sina / Sohu / Fastmail allow 50 MB. Corporate mail (Microsoft 365 / Exchange Online) defaults are also commonly 25–35 MB. Compressing your video to **10–19 MB** (L4's 16–19 MB or L6's <10 MB) therefore ships reliably through almost any mailbox.

**Recommended plan:**L4 (1 frame/6 s + 480p B&W + CRF 34 + stillimage + 20k audio) — a 99-minute video ≈ 16–19 MB, fitting most attachment limits; B&W stays sharp on desktop screens, and 20k audio keeps the voice clean. To stay under 10 MB, step up to L6 (10 s/frame + 360p + 8k audio), trading some quality for deliverability.

**Operational advice:**

- When sending, note in the email body: "This video is heavily compressed; fullscreen is recommended on small screens"
- If the video exceeds the attachment limit, upload it to cloud storage and link it — after compression this rarely happens

### 📱Scenario 2: WeChat / WeCom / DingTalk instant transfer

**Characteristics:**

- WeChat single-file limit is 1 GB (stable transfer practically suggests <100 MB)
- But clients usually watch on a phone — small screen, insensitive to resolution
- WeChat's H.265 compatibility is poor (iPhones support it, most Androids do, older models don't)
- Transfer time scales directly with file size — smaller is faster

**Recommended plan:**L5 (1 frame/6 s + 480p B&W + CRF 34 + stillimage + 8k audio) or L6 (10 s/frame + 360p + 8k audio) — L5: 99 minutes ≈ 14–17 MB; 480p vs 360p barely matters on a phone screen; 8k audio is plenty clear on phone speakers; the file is small enough to send quickly over 4G/5G.

**Operational advice:**

- Add a text note when sending: "Video is maximally compressed; landscape fullscreen recommended"
- If the client explicitly plans to cast to a TV/projector, upgrade to L4
- Avoid H.265 (L8) — compatibility issues may leave the recipient unable to open it

### 🏢Scenario 3: Corporate training / knowledge-base recording

**Characteristics:**

- Usually archived long-term; storage cost is a real business consideration
- Audience is internal staff — demanding about content, tolerant of quality (they care about substance)
- Playback may happen on intranet platforms or an LMS with broad format support
- Videos may be downloaded and forwarded many times; small size helps distribution speed

**Recommended plan:**L3 (CRF 34 + B&W) or L4 (plus stillimage) as the standard; L5 can further cut costs when batch-transcoding legacy archives.

**Operational advice:**

- Establish an internal rule: all newly recorded training videos enter the archive using the L4 standard
- Keep one original file for the archive (cold storage); distribute the compressed version daily
- Pair with a batch script to automatically compress new videos and replace old versions weekly
- Expected storage cost reduction: 80%–90%

### 🌐Scenario 4: Public courses / open lectures / MOOCs

**Characteristics:**

- Audience may come from poorly connected regions (remote areas, low-bandwidth abroad)
- Videos must work across all kinds of devices (old phones, tablets, public computers)
- Usually uploaded to video platforms (Bilibili, YouTube, local MOOC platforms), which re-transcode
- Small size = faster upload + faster load + less platform traffic

**Recommended plan:**L5 (1 frame/6 s + 480p B&W + 8k audio) by default; for colorblind/weak-sighted audiences or courses explaining palettes, keep color with L1 and accept the larger size.

**Operational advice:**

- Add to the course description: "This video is an ultra-low-bandwidth optimized version, suitable for slow connections"
- If the platform supports adaptive bitrate (ABR), upload multiple levels simultaneously and let the platform adapt
- For pure-audio content (e.g. language courses), offer an additional MP3 version (80% smaller still) as a supplementary resource

### 💼Scenario 5: Sales demos / pre-sales walkthroughs (for client decision-makers)

**Characteristics:**

- Audience is executives (directors, VPs, CEOs) with expectations of "professionalism"
- Charts, data, and logos must be clearly legible; color is sometimes a brand requirement
- Decision-makers may use any device (quick phone preview, careful desktop study)
- Size can't be too big (they won't bother downloading) and quality can't be too low (it looks unprofessional)

**Recommended plan:**L1 (1 frame/6 s + 480p color + CRF 32 + 20k audio) — keeps color so brand hues and chart distinctions stand out; 480p remains crisp on big screens; 99 minutes ≈ 30–35 MB — neither embarrassing nor bulky.

**Operational advice:**

- If the client explicitly plans to project on a big screen, upgrade to 720p (scale=-2:720) + CRF 28 (≈60–80 MB)
- Name files with the company abbreviation and date to look professional
- Quickly preview the file yourself before sending to make sure compression left no obvious artifacts

### 📝Scenario 6: Regulatory / compliance / audit archival video

**Characteristics:**

- Core requirements: content must be tamper-proof, traceable, and preserved long-term
- Original quality is usually kept as evidence, but archival storage costs are high
- Playback is extremely rare (possibly once every few years)
- Format stability matters greatly (H.264 is the first choice; H.265 may not be supported by audit systems)

**Recommended plan:**

- Original: keep one full high-bitrate file for legal effect
- Daily review copy: L2 (grayscale standard) or L3 (CRF 34) for fast content retrieval

**Operational advice:**

- Store the original in compliance storage (e.g. WORM); the compressed copy for everyday review
- Preserve all metadata when compressing (recording time, recorder, device info, etc.)
- Consider overlaying a timestamp watermark on the video (drawtext filter) to reinforce legal effect
- L6/L8 are not recommended — heavy picture jumping may invite questions about content continuity

### 📱Scenario 7: Mobile / offline viewing (travel, commuting)

**Characteristics:**

- Users pre-download to a phone/tablet and watch with no network
- Device storage is limited (especially 64GB/128GB models)
- Usually many episodes are batch-downloaded at once

**Recommended plan:**L6 (1 frame/10 s + 360p + 8k audio) or L8 (H.265 extreme), provided the player supports it — 360p is plenty sharp on a phone screen; at under 10 MB per episode, 20 episodes download in less than 200 MB.

**Operational advice:**

- Offer an "offline (low-bitrate)" option on the download page so users choose as needed
- For Apple users (iOS natively supports H.265), prioritize the smallest L8 version
- Ship a short "viewing guide" explaining that picture jumps from long sampling intervals are by design

### 🖥️Scenario 8: Video platform upload (Bilibili / YouTube / Douyin, etc.)

**Characteristics:**

- Platforms re-transcode uploads themselves
- Platforms publish recommended specs for resolution, bitrate, and codec
- Video sharpness directly affects recommendation algorithms and user experience
- Upload speed is affected by file size

**Recommended plan:** upload L1 (color 480p), because platform transcoding only compresses 480p further — if the source starts too low, the final result is poor. If the platform allows, upload two versions: L1 as the main one, L6 as a low-bandwidth fallback.

**Operational advice:**

- Check the platform's officially recommended parameters and fine-tune from L1
- E.g. Bilibili recommends H.264 at ≤6000kbps; L1 is far below that ceiling, no extra adjustment needed
- Short-video platforms (Douyin/Kuaishou) recommend vertical 9:16 — change the command to `scale=-2:720,crop=ih*9/16:ih`

### 🗂️Scenario 9: Batch archiving of legacy material / storage cleanup

**Characteristics:**

- Deals with an existing library of hundreds of thousands of hours of video
- Goal: free up storage while losing as little core information as possible
- Long batch processing time is acceptable (runs in the background)

**Recommended plan:**L5 (1 frame/6 s + 480p B&W + 8k audio) — the optimal balance between compression ratio and content preservation.

**Operational advice:**

- Test-compress 100 sample files first and confirm content is still recognizable
- Use GNU Parallel or xargs for parallel compression and make full use of multi-core CPUs
- After compression, verify all outputs with FFmpeg's `-f null -`
- Once the compressed versions check out, move originals to cold storage (tape or archive cloud) rather than deleting them outright, in case of surprises

## Plan Selection Quick Reference

| Work scenario | Primary plan | Alternative plan | Key consideration |
| --- | --- | --- | --- |
| Email attachment | L4 | L6 | Attachment limits + desktop viewing |
| WeChat/DingTalk transfer | L5 | L6 | Phone screen + transfer speed |
| Corporate training / KB | L4 | L3 | Long-term archive + internal circulation |
| Public course / MOOC | L5 | L1 (platform version) | Low-bandwidth audience + platform compatibility |
| Sales demo / pre-sales | L1 | L1-720p | Professionalism + brand color |
| Compliance / audit archive | L2 (review copy) | Original file (archive) | Legal effect + storage cost |
| Mobile offline viewing | L6 | L8 (Apple users) | Storage + batch download |
| Video platform upload | L1 | Platform-native specs | Platform transcoding loss |
| Legacy batch archiving | L5 | L6 | Huge file volume + freeing space |

## Scenario Decision Flowchart

Start: you have a lecture-style video to compress

Must color be preserved?

Yes · brand/palette

Client projecting on a big screen?

Yes

L1-720p + CRF 28

No

L1 standard

No · B&W is fine

Channel and bandwidth?

Email / training

L4 smart tuning

WeChat / MOOC

L5 audio extreme

Offline / ultra-low bandwidth

L6 long interval

Hard size ceiling?

Yes

L7 2-Pass locked size

No · H.265 supported

L8 H.265 extreme

No · H.265 not supported

Use the result above

## Summary

"1 frame / 6 seconds" is a philosophy; the 8-level compression standard is the toolbox. What actually makes the system work is choosing correctly per scenario — using L6 where it doesn't belong makes clients think "this video is too rough", and using L1 where it doesn't belong lets storage costs spiral.

Core principle

Use the right plan at the right time — neither waste bandwidth nor shortchange the content.

---

[← Previous: 8-level compression standard](levels.html)
[Next: prohibited red lines →](redlines.html)
