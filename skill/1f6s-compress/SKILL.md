---
name: 1f6s-compress
description: 用 ffmpeg 把给定视频转成符合「1帧6秒」八级压缩规范的输出。给定视频路径与级别(默认 L4),先探测源、展示将执行的命令,确认后执行压缩,产物默认 <basename>_1f6s.mp4,不覆盖原视频。
---

# 1f6s 视频压缩 Skill(1帧6秒 · ffmpeg 八级压缩)

本 Skill 是「1帧6秒」视频压缩倡议的**可执行落地**:给定一个视频,用 ffmpeg 把它转成符合八级压缩规范之一的输出。规范原文见仓库 `levels.html`;机器可读参数表见同目录 `levels.json`(脚本与 agent 共用,唯一真相源)。

它服务于「1帧6秒」倡议的核心主张——**讲解类视频的标准抽帧频率为 1帧/6秒**,在此之上叠加灰度、降分辨率、stillimage 调优、2-Pass 精确体积、H.265 等手段,把 99 分钟视频压到 6~35 MB 不等,且文字依然清晰。

## 两种使用路径

| 路径 | 适用 | 做法 |
|---|---|---|
| **脚本路径**(推荐) | 人类或 agent 直接压缩 | 调 `1f6s.sh <视频> [级别] [选项]`,脚本自动探测、展示、执行 |
| **纯 agent 路径** | agent 无法执行脚本时 | agent 读 `levels.json` 取参数,自行构造 ffmpeg 命令,按下方执行流程跑 |

**默认约定**:级别默认 **L4**(倡议默认推荐);输出默认 `<basename>_1f6s.mp4`,与源同目录,**不覆盖原视频,也不覆盖已存在输出**。

---

## 一、规范摘要(强制)

> 来源:`levels.html`。一切压缩参数以 `levels.json` 为准。

1. **抽帧**:讲解类视频统一抽帧到 `1帧/6秒`(L1~L5)或 `1帧/10秒`(L6~L8),用 `-vf "fps=1/6"` 或 `fps=1/10` 实现。
2. **灰度优先**:除 L1 外,全部级别加 `format=gray` 转黑白——讲解类画面颜色信息对理解无帮助,黑白可显著降体积。
3. **降分辨率**:480p(`scale=-2:480`)为默认;L6~L8 降到 360p(`scale=-2:360`)。
4. **编码器**:H.264(`libx264`)保证最大兼容性,除 L8 用 H.265(`libx265`,需确认客户端播放器支持)。
5. **音频**:AAC 单声道;L1~L4 用 20k/22050Hz,L5~L8 压到 8k/8000Hz(电话音质)。
6. **调优**:L4~L7 加 `-tune stillimage`(幻灯片静态画面专用优化,提升锐度);L8 加 `keyint=1:min-keyint=1`(每帧均为关键帧)。
7. **像素格式**:统一 `-pix_fmt yuv420p`(最大兼容)。
8. **2-Pass**:仅 L7,用于锁死目标体积;按公式算视频码率,跑两遍 pass。

---

## 二、八级参数表

| 级别 | 名称 | 抽帧 | 分辨率 | 色彩 | 视频 | 音频 | 调优 | 99分钟体积 |
|---|---|---|---|---|---|---|---|---|
| L1 | 标准级 | 1帧/6秒 | 480p | 彩色 | CRF 32 | 20k/22050 | — | ≈30~35 MB |
| L2 | 黑白级 | 1帧/6秒 | 480p | 黑白 | CRF 32 | 20k/22050 | — | ≈24~28 MB |
| L3 | 高压缩级 | 1帧/6秒 | 480p | 黑白 | CRF 34 | 20k/22050 | — | ≈18~22 MB |
| **L4** | **智能调优级 ★默认** | 1帧/6秒 | 480p | 黑白 | CRF 34 | 20k/22050 | stillimage | ≈16~19 MB |
| L5 | 音频极限级 | 1帧/6秒 | 480p | 黑白 | CRF 34 | 8k/8000 | stillimage | ≈14~17 MB |
| L6 | 长间隔级 | 1帧/10秒 | 360p | 黑白 | CRF 36 | 8k/8000 | stillimage | ≈10~12 MB |
| L7 | 2-Pass 级 | 1帧/10秒 | 360p | 黑白 | 2-Pass 动态 | 8k/8000 | stillimage | 按目标锁定 |
| L8 | H.265 极限级 | 1帧/10秒 | 360p | 黑白 | CRF 38 (x265) | 8k/8000 | keyint=1 | ≈6~8 MB |

### 各级完整 ffmpeg 命令(源自 levels.html / levels.json)

```bash
# L1 标准级(彩色)
ffmpeg -i input.mp4 -vf "fps=1/6,scale=-2:480" -c:v libx264 -preset slow -crf 32 -c:a aac -ac 1 -ar 22050 -b:a 20k -pix_fmt yuv420p output_L1.mp4

# L2 黑白级
ffmpeg -i input.mp4 -vf "fps=1/6,scale=-2:480,format=gray" -c:v libx264 -preset slow -crf 32 -c:a aac -ac 1 -ar 22050 -b:a 20k -pix_fmt yuv420p output_L2.mp4

# L3 高压缩级
ffmpeg -i input.mp4 -vf "fps=1/6,scale=-2:480,format=gray" -c:v libx264 -preset slow -crf 34 -c:a aac -ac 1 -ar 22050 -b:a 20k -pix_fmt yuv420p output_L3.mp4

# L4 智能调优级(★默认推荐)
ffmpeg -i input.mp4 -vf "fps=1/6,scale=-2:480,format=gray" -c:v libx264 -preset slow -tune stillimage -crf 34 -c:a aac -ac 1 -ar 22050 -b:a 20k -pix_fmt yuv420p output_L4.mp4

# L5 音频极限级
ffmpeg -i input.mp4 -vf "fps=1/6,scale=-2:480,format=gray" -c:v libx264 -preset slow -tune stillimage -crf 34 -c:a aac -ac 1 -ar 8000 -b:a 8k -pix_fmt yuv420p output_L5.mp4

# L6 长间隔级
ffmpeg -i input.mp4 -vf "fps=1/10,scale=-2:360,format=gray" -c:v libx264 -preset slow -tune stillimage -crf 36 -c:a aac -ac 1 -ar 8000 -b:a 8k -pix_fmt yuv420p output_L6.mp4

# L7 2-Pass 精确控制级(以 99 分钟压至 8MB 为例,视频码率约 3k)
# 第一遍分析
ffmpeg -i input.mp4 -vf "fps=1/10,scale=-2:360,format=gray" -c:v libx264 -preset slow -tune stillimage -b:v 3k -pass 1 -an -f mp4 /dev/null
# 第二遍输出
ffmpeg -i input.mp4 -vf "fps=1/10,scale=-2:360,format=gray" -c:v libx264 -preset slow -tune stillimage -b:v 3k -pass 2 -c:a aac -ac 1 -ar 8000 -b:a 8k -pix_fmt yuv420p output_L7.mp4

# L8 H.265 极限级(需播放器支持 H.265)
ffmpeg -i input.mp4 -vf "fps=1/10,scale=-2:360,format=gray" -c:v libx265 -preset slow -crf 38 -x265-params "keyint=1:min-keyint=1" -c:a aac -ac 1 -ar 8000 -b:a 8k -pix_fmt yuv420p output_L8.mp4
```

> Windows 平台:L7 第一遍命令中的 `/dev/null` 需替换为 `NUL`。脚本 `1f6s.sh` 已自动适配。

### L7 目标体积换算公式

```
总比特率(kbps) = 目标体积(MB) × 8192 / 总时长(秒)
视频码率(kbps) = 总比特率 − 音频码率(kbps,L7 为 8)
```

例:99 分钟(5940 秒)压至 8MB → 总比特率 = 8×8192/5940 ≈ 11 kbps → 视频码率 ≈ 3k。

---

## 三、执行流程(agent 逐条执行)

无论走脚本路径还是纯 agent 路径,都按下列流程:

1. **校验输入**:确认给定的视频文件存在;确认环境有 `ffmpeg` 与 `ffprobe`(脚本路径会自动检查)。
2. **确定级别**:从 `arguments` 解析级别(默认 L4)、目标体积(仅 L7,可选)、输出路径(可选)。
3. **探测源视频**:用 `ffprobe` 取时长、分辨率、编码、体积(脚本路径自动完成)。
4. **取参数**:从 `levels.json` 读取该级别全部参数(脚本路径自动完成;纯 agent 路径必须解析 `levels.json`,不得凭记忆写参数)。
5. **构造命令**:按参数拼装 ffmpeg 命令;L7 按公式算视频码率并生成两遍 pass 命令。
6. **展示**:向用户打印源信息 + 选定级别参数 + 即将执行的完整命令 + 预期输出文件名(`<basename>_1f6s.mp4`)。
7. **输出存在性检查**:若输出已存在且用户未明确允许覆盖(`--force`),中止并提示;若输出路径等于源视频,一律拒绝。
8. **确认后执行**:默认等用户确认 `y` 后执行;若 `arguments` 含 `--yes`/`-y` 或用户已明确同意,直接执行。
9. **校验并报告**:执行后用 ffprobe 校验产物可识别,打印输出体积并与该级 `expected_size` 对比,向用户报告路径/体积/级别/预期。

---

## 四、调用约定(arguments 格式)

调用本 Skill 时,`arguments` 按下列格式传:

- **默认压缩**:`视频: <路径>` —— 用默认 L4 压缩
- **指定级别**:`视频: <路径>; 级别: L4`(L1~L8)
- **L7 锁定体积**:`视频: <路径>; 级别: L7; 目标: 8MB`
- **自定义输出**:`视频: <路径>; 级别: L4; 输出: out.mp4`
- **仅生成命令不执行**:`视频: <路径>; 级别: L4; dry-run`
- **跳过确认直接执行**:`视频: <路径>; 级别: L4; yes`
- **覆盖已存在输出**:`视频: <路径>; 级别: L4; force`

### 最小调用示例

```
# 默认 L4 压缩(先展示后执行)
run_skill 1f6s-compress "视频: lecture.mp4"
# 产物: lecture_1f6s.mp4

# 指定 L7 锁定 8MB
run_skill 1f6s-compress "视频: lecture.mp4; 级别: L7; 目标: 8MB; yes"
# 产物: lecture_1f6s.mp4

# 只看命令不执行
run_skill 1f6s-compress "视频: lecture.mp4; 级别: L6; dry-run"
```

### 脚本路径直接调用

```bash
# 默认 L4
./skill/1f6s-compress/1f6s.sh lecture.mp4
# 指定级别
./skill/1f6s-compress/1f6s.sh lecture.mp4 L4 -y
# L7 锁定 8MB
./skill/1f6s-compress/1f6s.sh lecture.mp4 L7 --target 8 -y
# 只看命令
./skill/1f6s-compress/1f6s.sh lecture.mp4 L4 --dry-run
# 速查表
./skill/1f6s-compress/1f6s.sh --list
```

---

## 五、agent 强制约束

执行本 Skill 时,agent 必须遵守:

- **以 `levels.json` 为唯一参数源**:构造 ffmpeg 命令的参数(抽帧、分辨率、CRF、音频、tune、extra、twopass)必须从 `levels.json` 读取,不得凭记忆或猜测写参数,避免参数漂移。
- **默认先展示后执行**:展示将执行的完整命令与预期输出,用户确认后再执行;除非 `arguments` 明确含 `yes`/`-y` 或用户已事先同意。
- **默认不覆盖原视频**:输出命名 `<basename>_1f6s.mp4`;若输出已存在,中止并提示用 `--force` 覆盖或 `-o` 改名;若输出路径等于源视频,一律拒绝。
- **L7 必须跑两遍 pass**:第一遍 `-pass 1 -an -f mp4 /dev/null`(Windows 用 `NUL`)分析,第二遍 `-pass 2` 输出;按公式算视频码率;执行后清理 `ffmpeg2pass-*.log*` 残留日志。
- **L8 提示兼容性风险**:执行 L8 前必须向用户提示"输出为 H.265,必须确认客户端播放器支持,否则无法播放"。
- **失败保留诊断**:压缩失败时保留 ffmpeg 的 stderr 输出供诊断,不要吞掉错误。
- **校验产物**:执行后用 ffprobe 校验产物可识别,打印体积并与 `expected_size` 对比。

---

## 六、自测样本

作为 Skill 可用性验证,需能跑通以下样本(用 `ffmpeg -f lavfi` 造一段 12s 测试视频):

**样本 A — L4 默认压缩**:
```bash
ffmpeg -f lavfi -i testsrc=duration=12:size=640x480:rate=25 -f lavfi -i sine -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest test.mp4
./1f6s.sh test.mp4 L4 -y
```
核验:产物 `test_1f6s.mp4` 存在、可被 ffprobe 识别、未覆盖 `test.mp4`、命令含 `fps=1/6,scale=-2:480,format=gray -tune stillimage -crf 34`。

**样本 B — L7 两遍 pass**:
```bash
./1f6s.sh test.mp4 L7 --target 1 -y
```
核验:打印"目标体积 1MB → 视频码率约 XXXk";两遍 pass 均执行;产物可识别;`ffmpeg2pass-*.log*` 已清理。

**样本 C — 速查表与 dry-run**:
```bash
./1f6s.sh --list
./1f6s.sh test.mp4 L8 --dry-run
```
核验:`--list` 输出 L1~L8 八行;`L8 --dry-run` 命令含 `libx265 -crf 38 -x265-params "keyint=1:min-keyint=1"`,且未实际执行。

若自测发现问题,回补 `levels.json` / `1f6s.sh` / 本 SKILL.md,直到三份样本均通过。

---

## 附:文件清单与关系

```
skill/1f6s-compress/
├── SKILL.md      ← 本文件:agent playbook(规范摘要 + 参数表 + 执行流程 + 约束 + 自测)
├── 1f6s.sh       ← 配套封装脚本:人类与 agent 共用的执行入口
├── levels.json   ← 机器可读八级参数表(脚本与 agent 的唯一真相源)
└── README.md     ← 面向人的快速上手
```

本 Skill 与仓库现有 `skill/SKILL.md`(ppt skill)互补:ppt skill 让"源头"的幻灯片适配极限压缩,本 skill 把"成品"的视频压到规范体积。两者共同构成「1帧6秒」倡议从源头到成片的完整闭环。
