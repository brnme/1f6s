# 行业示例素材 · 教育（第一批）

这是 1f6s 课件起点素材库的第一批：教育行业 8 个学科各一个示例 deck。每个 deck 都是**自包含单文件 HTML**——零依赖、零外部引用，浏览器直接打开即可授课；拖入 [studio.html](../../studio.html) 可所见即所得编辑并跑「规范体检」；录课完成后按慕课场景推荐级别压缩（[spec/scenarios.json](../../spec/scenarios.json)：`mooc → L5`）。

## 清单

| 学科 | 课题 | 文件 | 页数 | 重点演示页型 |
|---|---|---|---|---|
| 数学 | 二次函数与抛物线 | [math-deck.html](math-deck.html) | 10 | 图表（柱状对比）、表格、左右对比 |
| 语文 | 水调歌头·明月几时有 | [chinese-deck.html](chinese-deck.html) | 11 | 大字引文、表格（名句品读）、清单 |
| 英语 | 四大核心时态 | [english-deck.html](english-deck.html) | 11 | 表格（标志词）、左右对比、清单 |
| 物理 | 牛顿运动三定律 | [physics-deck.html](physics-deck.html) | 11 | 表格、对比、深底例题页 |
| 化学 | 化学方程式与配平 | [chemistry-deck.html](chemistry-deck.html) | 11 | 深底代码页 ×2、表格（反应类型） |
| 生物 | 细胞的基本结构 | [biology-deck.html](biology-deck.html) | 10 | 表格（细胞器）、双对比页 |
| 历史 | 中国古代朝代大事速览 | [history-deck.html](history-deck.html) | 11 | 表格（时间线）、提示框口诀、清单 |
| 地理 | 世界气候类型判读 | [geography-deck.html](geography-deck.html) | 10 | 图表（降水柱状）、表格、左右对比 |

## 使用三步

1. **播放**：浏览器打开任一 deck 文件，`→ / Space` 翻页、`Home/End` 首末页、`F` 全屏；URL 加 `?s=3` 可直达第 3 页。
2. **改编**：把 deck 拖入 [studio.html](../../studio.html)（或粘贴源码），双击改字、用页型模板插页，点「体检」一键复查合规（三色 / ≥24pt / ≥3px 线宽 / 零阴影渐变 / 无衬线）。
3. **压片**：录屏 + 旁白得到课程视频后，用压缩脚本按慕课场景推荐级别输出：

   ```bash
   curl -fsSL -o 1f6s.sh https://raw.githubusercontent.com/brnme/1f6s/main/skill/1f6s-compress/1f6s.sh && chmod +x 1f6s.sh
   ./1f6s.sh 课程视频.mp4 L5   # 1帧/6秒 + 480p 黑白 + 8k 音频，产物为 *_1f6s.mp4
   ```

## 学科设计要点

- **理科（数学 / 物理 / 化学 / 生物）**：公式与方程式直接用文本排版（上标 ²、下标 ₂ 等 UTF-8 字符），不用图片；化学方程式、物理例题放深底代码页等宽展示；数值对比用黑白柱状图（实心 / 描边 / 斜纹三种填充）。
- **文科（语文 / 英语 / 历史 / 地理）**：诗词原文用大字号灰色引文整页展示；对照类知识（时态、朝代、气候）优先用表格与左右对比页；记忆线索做成提示框口诀或勾选清单。
- **通用**：一页只讲一件事（1 标题 + 3~5 要点，表格 ≤6 行），「宁可多一页，不要挤一页」；封面 badge 标注学科与「1f6s 教育示例」，末页附 Studio 与 L5 压缩提示。

## 合规与扩展约定

- 全部 deck 内嵌同一份规范样式（与 1f6s Studio 的 DECK_CSS 同源），通过 `python3 tools/check_decks.py` 静态校验与 Studio「规范体检」双重检查。
- 课题均为经典教学示例、不标学段，内容按 CC BY 4.0 授权，可自由改编。
- 新行业素材按 `examples/{行业}/{主题}-deck.html` 目录扩展（如 `examples/medical/`），从本目录任一 deck 复制骨架改内容即可，完成后跑 `python3 tools/check_decks.py` 验证。
