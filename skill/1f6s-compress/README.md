# 1f6s-compress · 1帧6秒 视频压缩工具

用 ffmpeg 把视频压成符合「1帧6秒」八级压缩规范的输出。讲解类视频的标准抽帧频率是 **1帧/6秒**,在此之上叠加灰度、降分辨率、stillimage 调优等手段,把 99 分钟视频压到 6~35 MB,文字依然清晰。

> 规范原文:仓库 `levels.html` · 参数真相源:`levels.json` · agent playbook:`SKILL.md`

## 依赖

| 依赖 | 是否必需 | 说明 |
|---|---|---|
| `ffmpeg` | 必需 | 4.x 及以上;需含 `libx264`。L8 还需 `libx265`。 |
| `ffprobe` | 必需 | 通常随 ffmpeg 一起安装。 |
| `jq` | 可选 | 解析 `levels.json`;未装时脚本自动降级用 `python3`。 |
| `python3` | 可选 | `jq` 缺失时作为 JSON 解析降级方案。 |

安装示例:

```bash
# Ubuntu / Debian
sudo apt install ffmpeg jq
# macOS
brew install ffmpeg jq
```

## 快速上手

```bash
# 给脚本可执行权限(首次)
chmod +x skill/1f6s-compress/1f6s.sh

# 默认用 L4 压缩(先展示命令,确认后执行)
./skill/1f6s-compress/1f6s.sh lecture.mp4

# 指定级别
./skill/1f6s-compress/1f6s.sh lecture.mp4 L4 -y

# L7 锁定目标体积(8MB)
./skill/1f6s-compress/1f6s.sh lecture.mp4 L7 --target 8 -y

# 只看将执行的命令,不实际压缩
./skill/1f6s-compress/1f6s.sh lecture.mp4 L4 --dry-run

# 打印八级速查表
./skill/1f6s-compress/1f6s.sh --list
```

**默认输出**:与源视频同目录,命名 `<原名>_1f6s.mp4`,**不覆盖原视频,也不覆盖已存在的输出**。需要覆盖加 `--force`;需要改名加 `-o <路径>`。

## 命令行选项

```
1f6s.sh <输入视频> [级别] [选项]

级别: L1 ~ L8(默认 L4)

选项:
  -o, --output <路径>   自定义输出文件名/路径
  -y, --yes             跳过确认,直接执行
  -n, --dry-run         只打印将执行的命令,不执行
  -l, --list            打印八级参数速查表后退出
  --target <MB>         L7 目标体积(MB),自动算视频码率
  --force               允许覆盖已存在的输出文件
  -h, --help            显示帮助
```

## 八级速查表

| 级别 | 名称 | 抽帧 | 分辨率 | 色彩 | 视频 | 音频 | 调优 | 99分钟体积 | 适用场景 |
|---|---|---|---|---|---|---|---|---|---|
| L1 | 标准级 | 1帧/6秒 | 480p | 彩色 | CRF 32 | 20k/22050 | — | ≈30~35 MB | 需保留彩色(图表/UI) |
| L2 | 黑白级 | 1帧/6秒 | 480p | 黑白 | CRF 32 | 20k/22050 | — | ≈24~28 MB | 黑白 PPT/代码/文字 |
| L3 | 高压缩级 | 1帧/6秒 | 480p | 黑白 | CRF 34 | 20k/22050 | — | ≈18~22 MB | 接受一定颗粒感 |
| **L4** | **智能调优级 ★默认** | 1帧/6秒 | 480p | 黑白 | CRF 34 | 20k/22050 | stillimage | ≈16~19 MB | 幻灯片/静态图表,体积与锐度最佳平衡 |
| L5 | 音频极限级 | 1帧/6秒 | 480p | 黑白 | CRF 34 | 8k/8000 | stillimage | ≈14~17 MB | 极低带宽(2G/3G),能听清即可 |
| L6 | 长间隔级 | 1帧/10秒 | 360p | 黑白 | CRF 36 | 8k/8000 | stillimage | ≈10~12 MB | 语速慢,接受画面跳跃 |
| L7 | 2-Pass 级 | 1帧/10秒 | 360p | 黑白 | 2-Pass | 8k/8000 | stillimage | 按目标锁定 | 必须"小于 XX MB" |
| L8 | H.265 极限级 | 1帧/10秒 | 360p | 黑白 | CRF 38 | 8k/8000 | keyint=1 | ≈6~8 MB | VLC/PotPlayer 等现代播放器 |

> **为什么默认 L4?** 它在体积(99 分钟约 16~19 MB)和观看体验之间取得最佳平衡:`-tune stillimage` 让静态幻灯片文字更锐利,同时 20k/22050 音频保证人声干净。除非有特殊需求,直接用 L4 即可。

## L7:精确锁定体积

L7 用 2-Pass 二次编码锁死目标体积。公式:

```
总比特率(kbps) = 目标体积(MB) × 8192 / 总时长(秒)
视频码率(kbps) = 总比特率 − 音频码率(8)
```

```bash
# 把 99 分钟视频压到 8MB
./1f6s.sh lecture.mp4 L7 --target 8 -y

# 脚本会自动算出视频码率,跑两遍 pass,并清理 pass 日志
```

## FAQ

**Q: 为什么默认转黑白?**
讲解类视频(教学、讲座、PPT 录屏)的颜色信息对理解内容几乎没有帮助,转黑白(`format=gray`)可让体积再降约 20%。若必须保留彩色(如图表配色、UI 区分),用 L1。

**Q: 为什么抽到 1帧/6秒?**
这是「1帧6秒」倡议的标准抽帧频率——讲解类画面变化慢,每 6 秒取一帧足够跟上换页节奏,又极大降低码率。语速慢、画面变化更少的场景可用 L6/L7/L8 的 1帧/10秒。

**Q: Windows 上 L7 报错?**
L7 第一遍输出到 `/dev/null`,Windows 需替换为 `NUL`。脚本 `1f6s.sh` 已自动检测平台适配;若你手工拼命令,记得替换。

**Q: L8 压出来对方打不开?**
L8 用 H.265(HEVC)编码,系统原生解码器(尤其旧版 Windows Media Player、部分手机)可能不支持。需确认对方用 VLC、PotPlayer 等支持 H.265 的播放器。否则用 L6。

**Q: 会覆盖我的原视频吗?**
不会。默认输出 `<原名>_1f6s.mp4`,与源同目录。即使同名输出已存在,脚本也会拒绝并提示用 `--force` 覆盖或 `-o` 改名。

**Q: 没有 jq 能用吗?**
能。脚本会自动降级用 `python3` 解析 `levels.json`。两者都没有才报错。

## 给 agent 用

把整个 `skill/1f6s-compress/` 文件夹交给任意 agent,让它读 `SKILL.md` 即可照做:给定视频路径与级别,agent 按 playbook 探测源、从 `levels.json` 取参、构造并展示命令、确认后执行(或直接调 `1f6s.sh` 完成)。`SKILL.md` 含完整的执行流程、调用约定与强制约束。

## 许可

随仓库统一许可。
