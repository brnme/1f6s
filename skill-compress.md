# 视频转 1f6s Skill · 1帧6秒

> 1帧6秒倡议 · https://brnme.github.io/1f6s/skill-compress.html · 本文为 Markdown 镜像,[HTML 原版](skill-compress.html)含交互组件。

---

## 视频转 1f6s Skill

给定一个视频，用 **ffmpeg** 把它转成符合「1帧6秒」八级压缩规范之一的输出。给定视频路径与级别（默认 L4），**先探测源、展示将执行的命令，确认后再执行**，产物默认 `<basename>_1f6s.mp4`，**不覆盖原视频**。

这是什么

一个可分享、供任意 agent 及人类使用的工具包（`skill/1f6s-compress/`）。既有供 agent 读取的 playbook（`SKILL.md`），也有供直接执行的 shell 封装（`1f6s.sh`）。它把倡议的八级参数落成机器可读的 `levels.json`，脚本与 agent 共用，避免参数漂移。

## 八级参数速查表

完整参数与 ffmpeg 命令见 [八级规范页](levels.html)。本 skill 以 `levels.json` 为唯一真相源：

| 级别 | 名称 | 抽帧 | 分辨率 | 色彩 | 视频 | 音频 | 调优 | 99分钟体积 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L1 | 标准级 | 1帧/6秒 | 480p | 彩色 | CRF 32 | 20k/22050 | — | ≈30~35 MB |
| L2 | 黑白级 | 1帧/6秒 | 480p | 黑白 | CRF 32 | 20k/22050 | — | ≈24~28 MB |
| L3 | 高压缩级 | 1帧/6秒 | 480p | 黑白 | CRF 34 | 20k/22050 | — | ≈18~22 MB |
| **L4** | **智能调优级 ★默认** | 1帧/6秒 | 480p | 黑白 | CRF 34 | 20k/22050 | stillimage | ≈16~19 MB |
| L5 | 音频极限级 | 1帧/6秒 | 480p | 黑白 | CRF 34 | 8k/8000 | stillimage | ≈14~17 MB |
| L6 | 长间隔级 | 1帧/10秒 | 360p | 黑白 | CRF 36 | 8k/8000 | stillimage | ≈10~12 MB |
| L7 | 2-Pass 级 | 1帧/10秒 | 360p | 黑白 | 2-Pass | 8k/8000 | stillimage | 按目标锁定 |
| L8 | H.265 极限级 | 1帧/10秒 | 360p | 黑白 | CRF 38 | 8k/8000 | keyint=1 | ≈6~8 MB |

## 怎么用

### 脚本路径（人类或 agent 直接执行）

bash · 1f6s.sh

```
# 默认用 L4 压缩(先展示命令,确认后执行)
./skill/1f6s-compress/1f6s.sh lecture.mp4

# 指定级别 + 跳过确认
./skill/1f6s-compress/1f6s.sh lecture.mp4 L4 -y

# L7 锁定目标体积(8MB)
./skill/1f6s-compress/1f6s.sh lecture.mp4 L7 --target 8 -y

# 只看将执行的命令,不实际压缩
./skill/1f6s-compress/1f6s.sh lecture.mp4 L6 --dry-run

# 打印八级速查表
./skill/1f6s-compress/1f6s.sh --list
```

### agent 路径（读取 playbook）

agent 读 `skill/1f6s-compress/SKILL.md` 后，按 `arguments` 约定执行：

调用示例

```
# 默认 L4
run_skill 1f6s-compress "视频: lecture.mp4"

# 指定 L7 锁定 8MB
run_skill 1f6s-compress "视频: lecture.mp4; 级别: L7; 目标: 8MB; yes"

# 只生成命令不执行
run_skill 1f6s-compress "视频: lecture.mp4; 级别: L6; dry-run"
```

### 命令行选项

| 选项 | 说明 |
| --- | --- |
| `-o, --output <路径>` | 自定义输出文件名/路径 |
| `-y, --yes` | 跳过确认，直接执行 |
| `-n, --dry-run` | 只打印将执行的命令，不执行 |
| `-l, --list` | 打印八级参数速查表后退出 |
| `--target <MB>` | L7 目标体积（MB），自动算视频码率 |
| `--force` | 允许覆盖已存在的输出文件 |
| `-h, --help` | 显示帮助 |

## 核心特性

- **先展示后执行**：ffprobe 探测源（时长/分辨率/编码/体积）→ 打印选定级别参数 + 完整命令 + 预期输出 → 用户确认 `y` 后执行（`-y` 跳过）
- **默认不覆盖原视频**：产物命名 `<basename>_1f6s.mp4`，与源同目录；输出已存在则拒绝（需 `--force` 才覆盖）；输出路径等于源视频则一律拒绝
- **八级全覆盖**：L1~L8 参数全部源自 `levels.json`（与 <levels.html> 一致），默认推荐 L4
- **L7 两遍 pass**：按公式 `目标体积×8192/时长 − 音频码率` 自动算视频码率，跑两遍 pass，自动清理 `ffmpeg2pass-*.log*`
- **L8 H.265**：含 `keyint=1:min-keyint=1`，执行前提示兼容性风险
- **平台适配**：`/dev/null` → `NUL` 自动检测（Windows）
- **依赖降级**：无 `jq` 时用 `python3` 解析 JSON；两者都没有才报错

## 执行流程

1. **校验输入**：确认视频文件存在、环境有 ffmpeg 与 ffprobe
2. **确定级别**：从 arguments 解析级别（默认 L4）、目标体积（仅 L7）、输出路径（可选）
3. **探测源视频**：ffprobe 取时长、分辨率、编码、体积
4. **取参数**：从 `levels.json` 读取该级别全部参数
5. **构造命令**：拼装 ffmpeg 命令；L7 按公式算视频码率并生成两遍 pass 命令
6. **展示**：打印源信息 + 级别参数 + 完整命令 + 预期输出文件名
7. **确认后执行**：默认等用户确认；含 `yes` 时直接执行
8. **校验并报告**：ffprobe 校验产物可识别，打印输出体积并与该级预期对比

## 文件清单

| 文件 | 作用 |
| --- | --- |
| `skill/1f6s-compress/SKILL.md` | agent playbook：规范摘要 + 参数表 + 执行流程 + 调用约定 + 强制约束 + 自测样本 |
| `skill/1f6s-compress/1f6s.sh` | 配套封装脚本：人类与 agent 共用的执行入口（已可执行） |
| `skill/1f6s-compress/levels.json` | 机器可读八级参数表（脚本与 agent 的唯一真相源） |
| `skill/1f6s-compress/README.md` | 面向人的快速上手：依赖/示例/速查表/FAQ |

## 常见问题

**Q:为什么默认 L4？**

它在体积（99 分钟约 16~19 MB）和观看体验之间取得最佳平衡： -tune stillimage 让静态幻灯片文字更锐利，20k/22050 音频保证人声干净。除非有特殊需求（需彩色用 L1、需锁体积用 L7、需极限体积用 L8），直接用 L4 即可。

**Q:为什么默认转黑白？**

讲解类视频的颜色信息对理解内容几乎没有帮助，转黑白（ format=gray ）可让体积再降约 20%。若必须保留彩色（图表配色、UI 区分），用 L1。

**Q:为什么是 6 秒？**

这是「1帧6秒」倡议的标准抽帧频率——讲解类画面变化慢，每 6 秒取一帧足够跟上换页节奏，又极大降低码率。语速慢、画面变化更少的场景可用 L6/L7/L8 的 1帧/10秒。详见 为什么是 6 秒 。

**Q:L7 怎么锁定体积？**

2-Pass 二次编码。公式： 总比特率 = 目标体积(MB) × 8192 / 总时长(秒) ， 视频码率 = 总比特率 − 音频码率(8) 。第一遍分析（ -pass 1 -an -f mp4 /dev/null ，Windows 用 NUL ），第二遍输出（ -pass 2 ）。脚本自动算码率、跑两遍、清理日志。

**Q:会覆盖我的原视频吗？**

不会。默认输出 <原名>\_1f6s.mp4 ，与源同目录。即使同名输出已存在，脚本也会拒绝并提示用 --force 覆盖或 -o 改名。

## 获取方式

本 Skill 是一个工具包文件夹，含 agent playbook 与可执行 shell 脚本，拿到即可用。

| 方式 | 做法 |
| --- | --- |
| 克隆仓库 | `git clone https://github.com/brnme/1f6s.git`，文件位于 `skill/1f6s-compress/` 目录 |
| 直接使用脚本 | 克隆后 `chmod +x skill/1f6s-compress/1f6s.sh`，即可 `./skill/1f6s-compress/1f6s.sh video.mp4 L4` 一行压缩 |
| 喂给 agent | 把 `skill/1f6s-compress/SKILL.md` 交给任意 agent，agent 读后按调用约定执行；或让 agent 直接调 `1f6s.sh` |

文件清单与依赖

仓库 `skill/1f6s-compress/`（含 `SKILL.md` / `1f6s.sh` / `levels.json` / `README.md`）。运行脚本需 ffmpeg + ffprobe；解析 `levels.json` 需 jq 或 python3（二选一即可，缺失时脚本自动降级）。

## 总结

视频转 1f6s Skill 是倡议的**可执行落地**：给视频路径与级别，得到符合八级规范的压缩输出。它与 [PPT 生成 Skill](skill-ppt.html) 互补——前者让成品视频压到规范体积，后者让源头幻灯片扛得住压缩。两者共同构成从源头到成片的完整闭环。

核心原则

以 levels.json 为唯一参数源，先展示后执行，默认不覆盖原视频——让倡议的八级规范人人可用、agent 可执行。

---

[← 上一页：PPT 生成 Skill](skill-ppt.html)
[下一页：OBS 配置 →](obs.html)
