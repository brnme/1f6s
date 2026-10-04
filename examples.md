# 行业示例素材 · 1帧6秒

> 1帧6秒倡议 · https://brnme.github.io/1f6s/examples.html · 本文为 Markdown 镜像,[HTML 原版](examples.html)含交互组件。

---

## 行业示例素材

为各行业制作的 1f6s 课件起点素材：每个示例都是自包含单文件 HTML 幻灯片 deck——浏览器直接打开即可播放，拖入工作台可编辑并自动体检，录课后按场景推荐级别压缩。课题均为经典示例，不标学段，按 CC BY 4.0 可自由改编。

使用三步

**① 播放**：浏览器打开任一 deck，`→` 翻页、`F` 全屏；**② 改编**：拖入 <studio.html> 双击改字，「体检」一键复查合规；**③ 压片**：录屏 + 旁白后 `./1f6s.sh 课程.mp4 L5`（慕课场景默认级，见[场景适配](scenarios.html)）。

## 教育行业 第一批 · 8 学科

[教育 · 01

📐 数学 · 二次函数与抛物线

10 页：定义与一般式、|a| 与开口大小的柱状图对比、顶点与对称轴、三种表达式与解题三步法。

打开 deck →](examples/education/math-deck.html)
[教育 · 02

📖 语文 · 水调歌头·明月几时有

11 页：苏轼名片与写作背景、上下阕大字原文、逐阕赏析、名句品读表与赏析方法清单。

打开 deck →](examples/education/chinese-deck.html)
[教育 · 03

🔤 英语 · 四大核心时态

11 页：一般现在 / 过去 / 现在进行 / 现在完成时逐页精讲，过去时与完成时左右对比、标志词表。

打开 deck →](examples/education/english-deck.html)
[教育 · 04

⚛️ 物理 · 牛顿运动三定律

11 页：三定律总览表、惯性与易错提示、平衡力与相互作用力对比、解题四步与深底例题页。

打开 deck →](examples/education/physics-deck.html)
[教育 · 05

🧪 化学 · 化学方程式与配平

11 页：质量守恒、常见方程式深底代码页、配平演示、四种反应类型表与易错清单。

打开 deck →](examples/education/chemistry-deck.html)
[教育 · 06

🧬 生物 · 细胞的基本结构

10 页：细胞学说、动植物细胞对比、细胞器分工表、原核与真核对比、复习清单。

打开 deck →](examples/education/biology-deck.html)
[教育 · 07

🏛️ 历史 · 朝代大事速览

11 页：朝代时间线表，秦汉隋唐宋元明清逐页一件大事，口诀提示框与复习清单。

打开 deck →](examples/education/history-deck.html)
[教育 · 08

🌍 地理 · 世界气候类型判读

10 页：判读依据、年降水量黑白柱状图、气候特征表、判读三步与易混辨析。

打开 deck →](examples/education/geography-deck.html)

## 全部示例一览

| 学科 | 课题 | deck 文件 | 页数 | 重点演示页型 |
| --- | --- | --- | --- | --- |
| 数学 | 二次函数与抛物线 | math-deck.html | 10 | 图表 / 表格 / 左右对比 |
| 语文 | 水调歌头·明月几时有 | chinese-deck.html | 11 | 大字引文 / 表格 / 清单 |
| 英语 | 四大核心时态 | english-deck.html | 11 | 表格 / 左右对比 / 清单 |
| 物理 | 牛顿运动三定律 | physics-deck.html | 11 | 表格 / 对比 / 深底例题 |
| 化学 | 化学方程式与配平 | chemistry-deck.html | 11 | 深底代码页 ×2 / 表格 |
| 生物 | 细胞的基本结构 | biology-deck.html | 10 | 表格 / 双对比页 |
| 历史 | 朝代大事速览 | history-deck.html | 11 | 表格 / 提示框口诀 / 清单 |
| 地理 | 世界气候类型判读 | geography-deck.html | 10 | 图表 / 表格 / 左右对比 |

## 素材约定与扩展

- 存放位置：`examples/{行业}/{主题}-deck.html`，本批为 `examples/education/`，索引与使用说明见 <examples/education/README.md>。
- 每个 deck 内嵌与 1f6s Studio 同源的规范样式：纯黑白灰三色、正文 ≥24pt、线宽 ≥3px、零阴影零渐变，全部通过 `tools/check_decks.py` 静态校验与工作台「体检」双重检查。
- 公式与方程式用文本排版（上标 ²、下标 ₂），不用截图；数值对比用黑白柱状图（实心 / 描边 / 斜纹三种填充）。
- 新行业按同样目录结构扩展：复制任一 deck 骨架改内容，完成后运行 `python3 tools/check_decks.py` 验证即可。

---

[← 上一页：压缩 Skill](skill-compress.html)
[下一页：工作台 Studio →](studio.html)
