# 八级压缩规范 · 1帧6秒

> 1帧6秒倡议 · https://brnme.github.io/1f6s/levels.html · 本文为 Markdown 镜像,[HTML 原版](levels.html)含交互组件。

---

## 八级压缩规范

以下方案按压缩强度从低到高排列，适用于不同场景（微信发送、邮件附件、超低带宽传输、存档备份等）。所有方案均基于 **H.264（libx264）**编码 + **AAC 音频**，确保最大兼容性——除 L8（H.265）外。

默认推荐

我们推荐将 **L4**（1帧/6秒 + 480p 黑白 + CRF 34 + stillimage + 20k 音频）作为默认标准方案，它在体积（99 分钟约 16～19 MB）和观看体验之间取得最佳平衡。

## 八级参数速览

| 级别 | 抽帧间隔 | 分辨率 | 色彩 | 视频质量 | 音频 | 额外调优 | 99分钟体积 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L1 标准级 | 1帧/6秒 | 480p | 彩色 | CRF 32 | 20k / 22.05kHz | — | ≈30～35 MB |
| L2 黑白级 | 1帧/6秒 | 480p | 黑白 | CRF 32 | 20k / 22.05kHz | — | ≈24～28 MB |
| L3 高压缩级 | 1帧/6秒 | 480p | 黑白 | CRF 34 | 20k / 22.05kHz | — | ≈18～22 MB |
| L4 智能调优级 | 1帧/6秒 | 480p | 黑白 | CRF 34 | 20k / 22.05kHz | tune=stillimage | ≈16～19 MB |
| L5 音频极限级 | 1帧/6秒 | 480p | 黑白 | CRF 34 | 8k / 8kHz | tune=stillimage | ≈14～17 MB |
| L6 长间隔级 | 1帧/10秒 | 360p | 黑白 | CRF 36 | 8k / 8kHz | tune=stillimage | ≈10～12 MB |
| L7 2-Pass级 | 1帧/10秒 | 360p | 黑白 | 2-Pass 动态 | 8k / 8kHz | tune=stillimage | 按目标锁定 |
| L8 H.265极限级 | 1帧/10秒 | 360p | 黑白 | CRF 38 (x265) | 8k / 8kHz | keyint=1 | ≈6～8 MB |

🟢 L1 标准级

### 快速压缩，保留画质与色彩

彩色兼容性最佳

**适用场景：**客户对画质有基本要求，需要保留彩色画面（如图表配色、UI 界面区分）。

|  |  |
| --- | --- |
| 画面刷新间隔 | 1帧/6秒 |
| 分辨率 | 480p（scale=-2:480） |
| 色彩 | 彩色 |
| 视频质量 | CRF 32（H.264） |
| 音频码率/采样率 | 20 kbps / 22.05 kHz / 单声道 |
| 额外调优 | 无 |

bash · ffmpeg

```
ffmpeg -i input.mp4 -vf "fps=1/6,scale=-2:480" -c:v libx264 -preset slow -crf 32 -c:a aac -ac 1 -ar 22050 -b:a 20k -pix_fmt yuv420p output_L1.mp4
```

**预期效果：**99 分钟视频 ≈ 30～35 MB。文字清晰，色彩完整，人声干净。

⚫ L2 黑白级

### 放弃色彩，换取体积

黑白体积降20%

**适用场景：**画面主要是黑白 PPT、代码、文字，颜色信息对理解内容无帮助。

|  |  |
| --- | --- |
| 画面刷新间隔 | 1帧/6秒 |
| 分辨率 | 480p（scale=-2:480） |
| 色彩 | 黑白（format=gray） |
| 视频质量 | CRF 32 |
| 音频码率/采样率 | 20 kbps / 22.05 kHz / 单声道 |
| 额外调优 | 无 |

bash · ffmpeg

```
ffmpeg -i input.mp4 -vf "fps=1/6,scale=-2:480,format=gray" -c:v libx264 -preset slow -crf 32 -c:a aac -ac 1 -ar 22050 -b:a 20k -pix_fmt yuv420p output_L2.mp4
```

**预期效果：**99 分钟视频 ≈ 24～28 MB。文字清晰度不变，体积再降约 20%。

🟠 L3 高压缩级

### CRF 34 + 黑白

CRF 34略有颗粒感

**适用场景：**需要进一步压缩，且客户接受画质有一定颗粒感。

|  |  |
| --- | --- |
| 画面刷新间隔 | 1帧/6秒 |
| 分辨率 | 480p |
| 色彩 | 黑白 |
| 视频质量 | CRF 34 |
| 音频码率/采样率 | 20 kbps / 22.05 kHz / 单声道 |
| 额外调优 | 无 |

bash · ffmpeg

```
ffmpeg -i input.mp4 -vf "fps=1/6,scale=-2:480,format=gray" -c:v libx264 -preset slow -crf 34 -c:a aac -ac 1 -ar 22050 -b:a 20k -pix_fmt yuv420p output_L3.mp4
```

**预期效果：**99 分钟视频 ≈ 18～22 MB。大号文字依然清晰，小号字体边缘略有模糊。

🔵 L4 智能调优级

### CRF 34 + 黑白 + tune=stillimage ★ 默认推荐

stillimage锐度最佳

**适用场景：**画面以幻灯片/静态图表为主，需要尽量保留锐度，同时压到最小。

|  |  |
| --- | --- |
| 画面刷新间隔 | 1帧/6秒 |
| 分辨率 | 480p |
| 色彩 | 黑白 |
| 视频质量 | CRF 34 |
| 音频码率/采样率 | 20 kbps / 22.05 kHz / 单声道 |
| 额外调优 | -tune stillimage（启用幻灯片专用优化） |

bash · ffmpeg

```
ffmpeg -i input.mp4 -vf "fps=1/6,scale=-2:480,format=gray" -c:v libx264 -preset slow -tune stillimage -crf 34 -c:a aac -ac 1 -ar 22050 -b:a 20k -pix_fmt yuv420p output_L4.mp4
```

**预期效果：**99 分钟视频 ≈ 16～19 MB。在同等体积下，文字锐度比 L3 更高。

🟣 L5 音频极限级

### CRF 34 + 黑白 + stillimage + 8kHz 音频

8k音频电话音质

**适用场景：**传输带宽极低（如 2G/3G 网络），只要求"能听清讲的是什么"。

|  |  |
| --- | --- |
| 画面刷新间隔 | 1帧/6秒 |
| 分辨率 | 480p |
| 色彩 | 黑白 |
| 视频质量 | CRF 34 |
| 音频码率/采样率 | 8 kbps / 8 kHz / 单声道（电话音质） |
| 额外调优 | -tune stillimage |

bash · ffmpeg

```
ffmpeg -i input.mp4 -vf "fps=1/6,scale=-2:480,format=gray" -c:v libx264 -preset slow -tune stillimage -crf 34 -c:a aac -ac 1 -ar 8000 -b:a 8k -pix_fmt yuv420p output_L5.mp4
```

**预期效果：**99 分钟视频 ≈ 14～17 MB。音频有轻微金属感，但人声可辨。

🔴 L6 长间隔级

### 10秒/帧 + 360p + 8kHz

10秒间隔360p

**适用场景：**极端压缩需求，语速较慢，且客户接受画面跳跃感较强。

|  |  |
| --- | --- |
| 画面刷新间隔 | 1帧/10秒 |
| 分辨率 | 360p（scale=-2:360） |
| 色彩 | 黑白 |
| 视频质量 | CRF 36 |
| 音频码率/采样率 | 8 kbps / 8 kHz |
| 额外调优 | -tune stillimage |

bash · ffmpeg

```
ffmpeg -i input.mp4 -vf "fps=1/10,scale=-2:360,format=gray" -c:v libx264 -preset slow -tune stillimage -crf 36 -c:a aac -ac 1 -ar 8000 -b:a 8k -pix_fmt yuv420p output_L6.mp4
```

**预期效果：**99 分钟视频 ≈ 10～12 MB。仅适合手机小屏观看，大字号标题可辨。

⚪ L7 2-Pass 精确控制级

### 锁死目标体积

2-Pass精确体积

**适用场景：**客户明确要求"文件必须小于 XX MB"，需要精确控制输出体积。

|  |  |
| --- | --- |
| 画面刷新间隔 | 1帧/10秒 |
| 分辨率 | 360p |
| 色彩 | 黑白 |
| 编码模式 | 2-Pass（二次编码） |
| 视频码率 | 根据目标体积动态计算 |
| 音频码率/采样率 | 8 kbps / 8 kHz |
| 额外调优 | -tune stillimage |

#### 计算方式

1. 目标体积（MB）→ 总比特率（kbps）= 目标体积(MB) × 8192 / 总时长(秒)
2. 视频码率 = 总比特率 − 音频码率（8 kbps）
3. 第一遍分析 + 第二遍输出

以下以 99 分钟压至 8MB 为例（视频码率约 3k）：

bash · pass 1 分析

```
# 第一遍
ffmpeg -i input.mp4 -vf "fps=1/10,scale=-2:360,format=gray" -c:v libx264 -preset slow -tune stillimage -b:v 3k -pass 1 -f mp4 /dev/null
```

bash · pass 2 输出

```
# 第二遍
ffmpeg -i input.mp4 -vf "fps=1/10,scale=-2:360,format=gray" -c:v libx264 -preset slow -tune stillimage -b:v 3k -pass 2 -c:a aac -ac 1 -ar 8000 -b:a 8k -pix_fmt yuv420p output_L7.mp4
```

Windows 平台注意

第一遍命令中的 `/dev/null` 在 Windows 上需替换为 `NUL`。

⚫ L8 H.265 极限级

### 兼容性牺牲换取极限体积

libx265需确认兼容

**适用场景：**客户使用 VLC/PotPlayer 等现代播放器，不依赖系统原生解码。

|  |  |
| --- | --- |
| 编码器 | libx265（H.265/HEVC） |
| 画面刷新间隔 | 1帧/10秒 |
| 分辨率 | 360p |
| 色彩 | 黑白 |
| 视频质量 | CRF 38 |
| 音频码率/采样率 | 8 kbps / 8 kHz |
| 额外调优 | keyint=1（每帧均为关键帧） |

bash · ffmpeg

```
ffmpeg -i input.mp4 -vf "fps=1/10,scale=-2:360,format=gray" -c:v libx265 -preset slow -crf 38 -x265-params "keyint=1:min-keyint=1" -c:a aac -ac 1 -ar 8000 -b:a 8k -pix_fmt yuv420p output_L8.mp4
```

兼容性警告

预期效果：99 分钟视频 ≈ 6～8 MB，画质接近 L6，体积仅为一半。**必须确认客户端播放器支持 H.265**，否则对方将无法播放。

## 倡议结语

这套规范的价值在于**标准化**——团队内统一标准，无需每次重新讨论参数，且任何成员都能快速生成质量一致、大小可控的输出文件。

最终建议

将本倡议作为团队内部的操作规范存档，新人入职时按此培训，确保视频输出的一致性。如有新的场景需求，可在此基础上扩展新的方案级别。

以上方案已全部经过实测验证，可直接投入生产使用。

---

[← 返回首页](index.html)
[下一页：九大工作场景适配 →](scenarios.html)
