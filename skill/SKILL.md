---
name: ppt
description: 把内容转成 / 从零生成符合「1帧6秒」PPT 抗压缩规范的 HTML 幻灯片 deck 的 playbook。
---

# PPT 生成 Skill（1帧6秒 抗压缩幻灯片）

本 Skill 产出**自包含的 HTML 幻灯片 deck**：单个 `.html` 文件，内联 CSS + 极简翻页 JS，零外部依赖，浏览器直接打开即可键盘翻页 / 全屏演示。

它服务于「1帧6秒」视频压缩倡议的核心主张——**演示文稿必须从源头适配极限压缩**。一切生成的幻灯片都必须严格遵循 `design.html` 中的"PPT 抗压缩设计规范"。

## 两种工作模式

| 模式 | 触发 | 输入 | 产物 |
|---|---|---|---|
| **生成模式**（重点） | 用户给主题或大纲 | 主题 / 大纲要点 | 从零生成符合规范的 deck |
| **转换模式** | 用户给本站页面文件名或 `all` | `index.html` / `levels.html` / `scenarios.html` / `redlines.html` / `design.html` / `all` | 把该页内容转成符合规范的 deck |

**默认约定**：合并成单文件 deck；输出落盘到仓库 `slides/` 目录，文件名形如 `slides/<主题或页面名>-deck.html`。

---

## 一、设计规范（生成与转换的强制硬约束）

> 来源：仓库 `design.html`。生成与转换时**一律强制**，违反即不合格。先读 `design.html` 确认规范原文，再按下列条款逐条落实。

### A. 字体与字号（对抗模糊）

1. **字体类型**：强制无衬线字体（思源黑体、微软雅黑、Arial、Helvetica）。**严禁**宋体、楷体、Times New Roman 等衬线或手写字体。
2. **最小字号**：正文 ≥ **24pt**；标题建议 ≥ **36pt**。低于 24pt 的文字一律回退到 24pt。
3. **字体颜色**：正文纯黑 `#000000`；反白（深色背景）用纯白 `#FFFFFF`。**严禁**用深灰（如 `#333333`）替代黑色。
4. **字重**：常规展示用 Bold / Heavy；Light / Thin 仅限 **>48pt** 的超大标题使用。

### B. 色彩与灰度（仅三色）

5. **只允许 3 个灰度层级**：纯黑 `#000000`、中度灰 `#808080`、纯白 `#FFFFFF`。三者之外的颜色一律替换为这三者之一。
6. **禁用浅灰** `#CCCCCC` 及更浅（RGB ≥ 200）用作文字或图表线条。
7. **中度灰 `#808080` 的字号 ≥ 28pt**，否则易被压缩成空白。
8. **杜绝任何彩色**（红/绿/蓝/黄/紫）出现在最终交付版。原稿有彩色，导出前统一替换为上述灰度值。
9. 需要表达"区分"时，用**斜体 / 下划线 / 图案填充**，而非依赖灰度深浅或彩色。

### C. 版式与留白（为编码器减负）

10. **背景必须纯白 `#FFFFFF` 或纯黑 `#000000`**。**严禁**渐变背景、纹理填充、图片水印。
11. **彻底禁用阴影 / 三维**：文字阴影、形状阴影、映像、发光、三维旋转、棱台——全部禁用。
12. **图表填充**：纯黑实心填充与纯白空心（描边）交替；用图案（斜线 / 点阵）代替颜色区分图例。
13. **饼图相邻色块对比度 > 50%**（黑-白-灰交替）。
14. **线条 / 描边粗细 ≥ 2.25pt（约 3px）**。1pt 以下细线在 360p 会断裂，一律加粗。

### D. 特殊元素

15. **截图**：严禁直接粘贴全屏截图；裁剪多余 UI 边框，仅留核心区；设灰度模式 + 对比度 +30%；截图内代码字体 ≥ 14pt（物理尺寸），否则放大截图为整页。
16. **公式**：用矢量公式，**严禁**图片格式公式；分数线 / 根号线条加粗。

### E. 三步自检法（生成后必跑）

每生成完一个 deck，对末页（信息最密的一页）执行：

17. **缩小测试**：浏览器缩放至 50%，站 1 米外观看；看不清标题则字号太小，加大。
18. **去色测试**：确认页面已是纯黑白灰；若两个相邻元素看起来融为一体，对比度不足，改为纯黑 / 纯白。
19. **细线扫描**：检查所有表格、图表边框；任何 < 3px 的细线全部加粗至 ≥ 3px。

### 铁律

- **结构可借、样式必须新建**：可复用源页的 HTML 语义结构（`section` / `h2` / `h3` / `table` / `ul` / `li` / callout 结构），但**严禁直接引用 `assets/css/style.css` 或 `assets/js/main.js`**——它们含彩色、阴影、渐变、小字、细线，全面违反本规范。
- 幻灯片必须使用本 Skill 内嵌的**独立样式表**（见下方模板），强制三色、无衬线、≥24pt、≥3px 边框、纯色背景、零阴影零渐变。

---

## 二、生成模式 Playbook（重点：从零生成）

> 触发：用户给出主题或大纲（如 `主题: xxx` 或 `大纲: 要点1, 要点2, …`）。
> 目标：从零生成一套**逐页落实抗压缩规范**的 HTML 幻灯片 deck。

### 工作流（按顺序执行）

1. **拆解输入**：从用户输入中提炼出主题、目标受众、核心要点列表。若用户只给主题没给大纲，先根据主题规划 5～12 个要点（一个要点 ≈ 一页），必要时用 `ask` 与用户确认大纲。
2. **规划页面序列**：按「封面 → 目录 → 内容页（一个要点一页）→ 末页致谢」组织。控制信息密度——**一页一要点**，宁可多拆一页，不要把多要点挤一页。
3. **逐页生成**：对每一页，先选定「页型」（见下方页型清单），套用对应最小合规片段，填入内容。生成时严格执行「逐页强制动作」清单。
4. **自检**：全部页面生成后，对信息最密的一页跑「三步自检法」（缩小 / 去色 / 细线扫描），不合格则回退修正。
5. **落盘**：输出到 `slides/<主题>-deck.html`，告知用户文件路径与键盘操作说明。

### 逐页强制动作（生成每一页时逐条核对）

- [ ] **字号档位**：每个文本元素先定档——标题 36pt、正文 24pt、灰色辅助文字 28pt。任何低于 24pt 的一律回退到 24pt。
- [ ] **颜色三色化**：每个颜色值只允许 `#000000` / `#808080` / `#FFFFFF` 之一；出现任何彩色（含 `#0066cc`、`#c0392b`、`#2e7d32`、八级徽章配色等）立即替换为对应灰度。
- [ ] **线条加粗**：每条线 / 边框先确认 ≥ 3px；细线（1px / 2px）一律加粗到 3px。
- [ ] **禁用效果**：不写任何 `box-shadow` / `text-shadow` / `linear-gradient` / `radial-gradient` / `filter:blur`。
- [ ] **图表合规**：图表一律纯黑实心 + 纯白描边交替 + 图案（斜线 / 点阵）填充表达分类，**不得靠彩色区分**图例。
- [ ] **背景纯色**：`background` 只能是 `#FFFFFF` 或 `#000000`，不写渐变 / 纹理 / 图片。
- [ ] **无外部依赖**：不引入 `assets/css/style.css`、`assets/js/main.js` 或任何 CDN；样式与脚本全部内联。

### 页型清单（每种给出最小合规 HTML 片段）

以下片段都基于本 Skill 内嵌模板（见第四节）。`class="slide"` 是每页容器；`.deck-title` / `.deck-h2` / `.deck-body` / `.deck-muted` 等类已在模板 `<style>` 中定义好字号与颜色，直接复用即可保证合规。

**1. 封面页**
```html
<section class="slide slide-cover">
  <h1 class="deck-title">主题标题</h1>
  <p class="deck-muted">副标题 / 作者 / 日期</p>
</section>
```

**2. 目录页**
```html
<section class="slide">
  <h2 class="deck-h2">目录</h2>
  <ol class="deck-list">
    <li>要点一</li>
    <li>要点二</li>
    <li>要点三</li>
  </ol>
</section>
```

**3. 纯文字要点页**
```html
<section class="slide">
  <h2 class="deck-h2">本页标题</h2>
  <ul class="deck-list">
    <li>要点 A：一句话说清。</li>
    <li>要点 B：一句话说清。</li>
  </ul>
  <p class="deck-muted">辅助说明（中度灰，≥28pt）</p>
</section>
```

**4. 表格页**
```html
<section class="slide">
  <h2 class="deck-h2">本页标题</h2>
  <div class="deck-tbl-wrap">
    <table class="deck-tbl">
      <thead><tr><th>列名</th><th>列名</th></tr></thead>
      <tbody>
        <tr><td>值</td><td>值</td></tr>
      </tbody>
    </table>
  </div>
</section>
```

**5. 图表页（纯黑白 + 图案填充，无彩色）**
```html
<section class="slide">
  <h2 class="deck-h2">本页标题</h2>
  <div class="deck-chart">
    <!-- 柱状图：纯黑实心柱 与 纯白描边柱 交替 -->
    <div class="bar bar-solid" style="--h:60%"></div>
    <div class="bar bar-outline" style="--h:40%"></div>
    <div class="bar bar-hatch" style="--h:80%"></div>
  </div>
  <ul class="deck-legend">
    <li><span class="sw sw-solid"></span>系列 A</li>
    <li><span class="sw sw-outline"></span>系列 B</li>
    <li><span class="sw sw-hatch"></span>系列 C</li>
  </ul>
</section>
```

**6. 对比页（左右二分）**
```html
<section class="slide">
  <h2 class="deck-h2">本页标题</h2>
  <div class="deck-two">
    <div><h3 class="deck-h3">方案一</h3><p class="deck-body">说明</p></div>
    <div><h3 class="deck-h3">方案二</h3><p class="deck-body">说明</p></div>
  </div>
</section>
```

**7. 代码页（等宽，≥24pt 等效，深底白字）**
```html
<section class="slide slide-dark">
  <h2 class="deck-h2 deck-h2-light">本页标题</h2>
  <pre class="deck-code"><code>ffmpeg -i in.mp4 -an -vf fps=1/6 out.mp4</code></pre>
</section>
```

**8. 清单 / 自检页（可勾选，纯黑白勾选符号）**
```html
<section class="slide">
  <h2 class="deck-h2">自查清单</h2>
  <ul class="deck-checklist">
    <li>□ 缩小测试通过</li>
    <li>□ 去色测试通过</li>
    <li>□ 细线扫描通过</li>
  </ul>
</section>
```

**9. 末页致谢**
```html
<section class="slide slide-cover">
  <h1 class="deck-title">谢谢</h1>
  <p class="deck-muted">1帧6秒 · 视频压缩倡议</p>
</section>
```

### 信息密度控制

- 一页不超过 1 个标题 + 3～5 个要点 + 1 行辅助说明；超出就拆成两页。
- 表格一页不超过 6 行；超出拆页或只保留关键行。
- 代码一页不超过 8 行；超出拆页或只保留核心命令。
- **宁可多一页，不要挤一页**——这是抗压缩设计的延伸：画面越简单，编码器越省力，压缩后越清晰。

---

## 三、转换模式 Playbook（把已有页面转成 deck）

> 触发：用户给本站页面文件名（`index.html` / `levels.html` / `scenarios.html` / `redlines.html` / `design.html`）或 `all`（转全部 5 页）。
> 目标：把该页内容**结构保留、样式重做**，转成符合抗压缩规范的 deck。

### 切片规则（决定一页变几张幻灯片）

- **一级切片**：以源页 `<section id="…">` 为单位，一个 section → 一张幻灯片。
- **二级切片**（内容过密时下钻）：
  - `levels.html`：每个 `.lvl-section.l1`～`.l8` → 一张（L1～L8 共 8 张）
  - `scenarios.html`：每个 `.scene` → 一张（9 个场景共 9 张）
  - `redlines.html`：每个 `.redline-cat` → 一张或每类（`.redline-cat` 分组）→ 一张
  - `index.html`：`#why-6s` 的每个 `<h3>` → 可合一张或拆两张；`#entries` 的每个 `.entry-card` → 一张
- **全站预估**：约 44～52 张（见各页明细）：
  - index.html：9～11 张
  - levels.html：10～11 张
  - scenarios.html：12～13 张
  - redlines.html：6～10 张
  - design.html：7 张

### 剥离规则（这些元素一律去掉）

- `header.site-header`（sticky 导航）：去掉（幻灯片无需顶部导航；其半透明+模糊+边框违反规范）
- `footer.site-footer` + `ul.footer-nav` + `.footer-copy`：去掉（小字违反 ≥24pt）
- 页间 `<hr>` + `<nav>`（上一页/下一页）：去掉（幻灯片用键盘翻页取代）
- `a.brand` 文字"1帧6秒"：**仅**用于封面页标题与末页致谢，不保留为导航
- `ul.nav-links` 5 项：转为**目录页**的 5 个章节起点，不保留为顶部导航

### 转换时套用硬约束（与生成模式同规）

转换不是"原样搬运"，必须逐页套用「一、设计规范」全部 19 条 + 铁律：

- **表格**：去掉 `.tbl-wrap` 的 shadow；表头浅灰 `#f0f2f5` 改纯黑 `#000000`（白字）或纯白（黑字）；边框 `--line:#e4e4e4` 的 1px 细线加粗到 3px；改用模板的 `.deck-tbl` / `.deck-tbl-wrap`。
- **callout**：去掉 `.callout.danger` 的红色边、`.callout.ok` 的绿色边；统一改为模板的 `.deck-callout` / `.deck-callout-warn`（纯黑白边框、无彩色）；`.callout-title` 文字保留。
- **徽章**：`.lvl-badge.l1`～`.l8` 的八色全部去掉，改为模板的 `.deck-badge`（纯黑白文字徽章，用文字"L1"～"L8"区分，不靠颜色）。
- **checklist**：`.checklist` 的绿勾改为纯黑/纯白勾选符号；改用模板的 `.deck-checklist`。
- **代码块**：`.code-block` 的 shadow、`#f6f8fa` 浅灰底、13px 小字全部去掉；改用模板的 `.deck-code`（深底白字、≥24pt 等效、无 shadow）；`.copy-btn` 复制按钮可保留但改纯黑白样式。
- **流程图**：`.flowchart` / `.flow-node` 的 accent 蓝、shadow 去掉；改为纯黑白方框 + 3px 箭头线。
- **图表**：任何彩色填充改为纯黑实心 + 纯白描边 + 图案填充。
- **hero 渐变**：`index.html` 的 `.hero` linear-gradient 去掉，改纯白或纯黑背景 → 封面页。

### 交互组件处理

- `#calculator`（体积估算器）、`#selector`（方案选择器）：这两个是 JS 动态生成结果的交互组件。
  - 默认做法：**固化为静态默认输出**——取其推荐逻辑的默认结果，做成一张静态表格/要点页。
  - 可选做法：作为**独立交互演示页**保留（但必须用模板的合规样式重做，不得引入 `main.js`）。
- 自检清单 `#design-checklist`：保留为清单/自检页，用模板的 `.deck-checklist`。

### 各页转换要点

- **index.html**：hero → 封面；manifesto → 宣言页；why-6s → 1～2 张；compare-table → 表格页；calculator/selector → 静态化 1～2 张；entries → 4 张入口卡或合 1 张目录；glossary → 术语页；faq → 1～2 张。
- **levels.html**：top+overview → 总览页（含参数速览表）；L1～L8 → 8 张（每张含 badge+场景+参数表+ffmpeg 命令+预期效果）；conclusion → 末页。
- **scenarios.html**：top → 封面；9 个 scene → 9 张；quick-table → 速查表页；decision-flow → 流程图页；summary → 总结页。
- **redlines.html**：top → 封面（含 callout.danger 转 deck-callout-warn）；4 类 → 4～8 张；judge → 反向判断法页。
- **design.html**：top → 封面（核心原则）；fonts/grayscale/layout/special/checklist/bonus → 6 张内容页。

---

## 四、自包含幻灯片模板（两种模式共用，复制即用）

> 以下是一份**完整可用的 HTML deck 模板**。生成模式与转换模式都以此为基础：把 `<!-- SLIDES -->` 处替换为若干 `<section class="slide">` 页面即可。
> 模板自包含：内联 `<style>` + 内联 `<script>`，**零外部依赖**，不引用 `assets/css/style.css`、不引用 `assets/js/main.js`、不引用任何 CDN。
> 模板已落实全部 19 条硬约束：三色 `#000000`/`#808080`/`#FFFFFF`、无衬线字体栈、正文 24pt(32px)/标题 36pt(48px)/超大 56px、中度灰 28pt(约37px)、边框 ≥3px、纯色背景、零阴影零渐变。

**关键 CSS 变量与字号对应**（pt → px 按 96dpi 近似，幻灯片按 1280×720 投影缩放）：
- `--black: #000000`、`--gray: #808080`、`--white: #FFFFFF`（仅此三色）
- 正文 `.deck-body` = 32px (≈24pt)；标题 `.deck-h2` = 48px (≈36pt)；超大 `.deck-title` = 56px (>48pt)；中度灰 `.deck-muted` = 37px (≈28pt)
- 边框统一 3px 实线；零 `box-shadow`；零 `text-shadow`；零 `gradient`

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>幻灯片 Deck</title>
<style>
  /* ===== 抗压缩幻灯片样式（仅三色 / 无衬线 / ≥24pt / ≥3px边框 / 零阴影零渐变）===== */
  :root{
    --black:#000000; --gray:#808080; --white:#FFFFFF;
    --line:3px solid var(--black);          /* ≥2.25pt */
    --sans:"Source Han Sans SC","Microsoft YaHei","微软雅黑",Arial,Helvetica,sans-serif; /* 无衬线 */
    --mono:"Cascadia Code","Consolas","Courier New",monospace;
  }
  *{box-sizing:border-box; margin:0; padding:0;}
  html,body{height:100%;}
  body{
    font-family:var(--sans); background:var(--white); color:var(--black);
    overflow:hidden;                         /* 翻页模式，隐藏滚动 */
  }

  /* ===== 幻灯片容器 ===== */
  .deck{width:100vw; height:100vh; position:relative;}
  .slide{
    width:100vw; height:100vh; padding:64px 80px;
    display:none; flex-direction:column; justify-content:center;
    background:var(--white); color:var(--black);
  }
  .slide.active{display:flex;}

  /* 深色页（代码页等）：纯黑底 + 纯白字 */
  .slide-dark{background:var(--black); color:var(--white);}
  .slide-dark .deck-h2, .slide-dark .deck-h3{color:var(--white);}
  .deck-h2-light{color:var(--white) !important;}

  /* 封面页：居中大标题 */
  .slide-cover{align-items:center; text-align:center;}

  /* ===== 字号档位（≥24pt 硬约束）===== */
  .deck-title{font-size:56px; font-weight:700; line-height:1.2;}        /* 超大 >48pt */
  .deck-h2{font-size:48px; font-weight:700; line-height:1.25; margin-bottom:32px;}   /* 标题 ≈36pt */
  .deck-h3{font-size:40px; font-weight:700; line-height:1.3; margin-bottom:20px;}    /* 副标题 */
  .deck-body{font-size:32px; font-weight:700; line-height:1.5;}         /* 正文 ≈24pt，Bold */
  .deck-muted{font-size:37px; color:var(--gray); font-weight:700; line-height:1.4;}   /* 中度灰 ≈28pt */
  .slide-dark .deck-muted{color:var(--gray);}

  /* ===== 列表 ===== */
  .deck-list{list-style:none; padding:0;}
  .deck-list li{
    font-size:32px; font-weight:700; line-height:1.5; padding:10px 0;
    border-bottom:var(--line);               /* 3px 分隔线 */
  }
  .deck-list li:last-child{border-bottom:none;}
  ol.deck-list{counter-reset:deck;}
  ol.deck-list li{counter-increment:deck; padding-left:56px; position:relative;}
  ol.deck-list li::before{content:counter(deck)". "; position:absolute; left:0; font-weight:700;}

  /* ===== 表格（合规版：黑白表头、3px边框、无shadow）===== */
  .deck-tbl-wrap{overflow-x:auto;}
  .deck-tbl{width:100%; border-collapse:collapse; font-size:28px; font-weight:700;}
  .deck-tbl th,.deck-tbl td{border:var(--line); padding:14px 18px; text-align:left;}
  .deck-tbl thead th{background:var(--black); color:var(--white);}      /* 纯黑表头白字 */
  .deck-tbl tbody tr:nth-child(even){background:var(--white);}
  .deck-tbl tbody tr:nth-child(odd){background:var(--white);}

  /* ===== 提示框（合规版：纯黑白边框、无彩色）===== */
  .deck-callout{
    border:var(--line); padding:24px 28px; margin-top:24px; background:var(--white);
  }
  .deck-callout-title{font-size:36px; font-weight:700; margin-bottom:12px;}
  .deck-callout p{font-size:32px; font-weight:700; line-height:1.5;}
  /* 警告变体：用粗框 + 加粗"⚠"前缀区分，不靠红色 */
  .deck-callout-warn{border-width:5px;}
  .deck-callout-warn .deck-callout-title::before{content:"⚠ "; }

  /* ===== 徽章（合规版：纯黑白文字，不靠颜色）===== */
  .deck-badge{
    display:inline-block; border:var(--line); padding:4px 14px;
    font-size:28px; font-weight:700; margin-right:12px; background:var(--white);
  }

  /* ===== 清单 / 自检（纯黑白勾选符号）===== */
  .deck-checklist{list-style:none; padding:0;}
  .deck-checklist li{font-size:32px; font-weight:700; line-height:1.6; padding:8px 0;}

  /* ===== 代码块（合规版：深底白字、≥24pt等效、无shadow）===== */
  .deck-code{
    background:var(--black); color:var(--white); font-family:var(--mono);
    font-size:30px; line-height:1.5; padding:28px 32px; overflow-x:auto;
    white-space:pre; border:var(--line);
  }

  /* ===== 图表（纯黑白 + 图案填充）===== */
  .deck-chart{display:flex; align-items:flex-end; gap:32px; height:320px; border-bottom:var(--line); padding-bottom:0;}
  .bar{width:96px; background:var(--white); border:var(--line); height:var(--h);}
  .bar-solid{background:var(--black);}                       /* 纯黑实心 */
  .bar-outline{background:var(--white);}                     /* 纯白空心描边 */
  .bar-hatch{                                                   /* 斜线图案填充 */
    background:repeating-linear-gradient(45deg,var(--black) 0 8px,var(--white) 8px 16px);
  }
  .deck-legend{list-style:none; display:flex; gap:28px; margin-top:20px; padding:0;}
  .deck-legend li{font-size:28px; font-weight:700; display:flex; align-items:center; gap:10px;}
  .sw{display:inline-block; width:24px; height:24px; border:3px solid var(--black);}
  .sw-solid{background:var(--black);}
  .sw-outline{background:var(--white);}
  .sw-hatch{background:repeating-linear-gradient(45deg,var(--black) 0 4px,var(--white) 4px 8px);}

  /* ===== 对比页（左右二分，3px 分隔线）===== */
  .deck-two{display:flex; gap:0; margin-top:16px;}
  .deck-two>div{flex:1; padding:0 32px;}
  .deck-two>div+div{border-left:var(--line);}

  /* ===== 页码指示（纯黑白，≥24pt）===== */
  .pager{
    position:fixed; right:32px; bottom:24px; font-size:28px; font-weight:700;
    color:var(--gray); background:var(--white); padding:4px 12px; border:var(--line);
  }
  .slide-dark ~ .pager{color:var(--gray);}
</style>
</head>
<body>
<div class="deck">

  <!-- SLIDES：在此插入若干 <section class="slide"> 页面 -->
  <section class="slide slide-cover active">
    <h1 class="deck-title">标题</h1>
    <p class="deck-muted">副标题</p>
  </section>

  <section class="slide">
    <h2 class="deck-h2">第一页</h2>
    <ul class="deck-list">
      <li>要点 A</li>
      <li>要点 B</li>
    </ul>
  </section>

</div>

<div class="pager"><span id="cur">1</span> / <span id="total">2</span></div>

<script>
  /* ===== 极简翻页（←/→/Space/Home/End/F全屏），零依赖 ===== */
  (function(){
    var slides=document.querySelectorAll('.slide');
    var total=slides.length;
    document.getElementById('total').textContent=total;
    var cur=0;
    function show(i){
      cur=(i+total)%total;
      slides.forEach(function(s,idx){s.classList.toggle('active',idx===cur);});
      document.getElementById('cur').textContent=cur+1;
    }
    document.addEventListener('keydown',function(e){
      var k=e.key;
      if(k==='ArrowRight'||k===' '||k==='PageDown'){show(cur+1);e.preventDefault();}
      else if(k==='ArrowLeft'||k==='PageUp'){show(cur-1);e.preventDefault();}
      else if(k==='Home'){show(0);e.preventDefault();}
      else if(k==='End'){show(total-1);e.preventDefault();}
      else if(k==='f'||k==='F'){
        if(!document.fullscreenElement){document.documentElement.requestFullscreen();}
        else{document.exitFullscreen();}
      }
    });
    show(0);
  })();
</script>
</body>
</html>
```

### 模板使用说明

- **生成模式**：复制整个模板，把 `<!-- SLIDES -->` 区的两个示例页替换为你按「二、生成模式」页型清单产出的若干 `<section class="slide">`。
- **转换模式**：复制整个模板，把示例页替换为你按「三、转换模式」切片规则从源页提取并重做样式的若干 `<section class="slide">`。
- **第一张** slide 加 `active` 类（模板已示范）；翻页 JS 会自动管理其余页的显示。
- **页码** 由 JS 自动计算，无需手填 `total`。
- **深色页**（代码页）加 `slide-dark` 类；其标题加 `deck-h2-light`。
- 所有字号、颜色、边框都由模板 CSS 锁死合规——**只要用模板提供的类名（`deck-*`），就不可能违反规范**。切勿内联覆盖字号 / 颜色 / 边框 / 阴影。

---

## 五、调用约定、示例与验证

### arguments 约定

调用本 Skill 时，`arguments` 按下列格式传：

- **生成模式**：
  - `主题: <主题>` —— 只给主题，由 Skill 规划大纲（5～12 个要点）
  - `主题: <主题>; 大纲: 要点1, 要点2, 要点3` —— 给定大纲，按大纲逐页生成
  - `主题: <主题>; 受众: <受众>; 页数: <约N页>` —— 可选附加约束
- **转换模式**：
  - `转换: <页面名>` —— 如 `转换: levels.html`
  - `转换: all` —— 转全部 5 个内容页，每页一个 deck

### 最小调用示例

```
# 生成模式
run_skill ppt "主题: 团队周报规范; 大纲: 本周进展, 风险与阻塞, 下周计划, 数据看板"
# 产物：slides/团队周报规范-deck.html

# 转换模式
run_skill ppt "转换: levels.html"
# 产物：slides/levels-deck.html
```

### 输出落盘约定

- 目录：仓库 `slides/`（不存在则创建）
- 文件名：`<主题或页面名>-deck.html`，小写、空格用连字符
- 单文件 deck（内联 CSS + JS），可直接双击在浏览器打开

### 交付时告知用户

生成 / 转换完成后，向用户报告：
1. 输出文件路径（如 `slides/levels-deck.html`）
2. 键盘操作：`←/→` 或 `Space` 翻页、`Home/End` 首末页、`F` 全屏
3. 幻灯片总张数
4. 自检结果（三步自检法是否通过）

### 验证（自测样本）

每完成一个 deck，按「三步自检法」自检（见一、E）。作为 Skill 自身可用性的验证，需能跑通以下两个样本：

**样本 A — 生成模式自测**：对 `design.html` 的"PPT 抗压缩设计规范"内容，用生成模式产出一个 deck。
- 输入理解为：`主题: PPT抗压缩设计规范; 大纲: 字体字号, 色彩灰度, 版式留白, 特殊元素, 三步自检`
- 预期产物：`slides/design-deck.html`，约 7 张
- 核验项：纯黑白灰、无阴影渐变、字号 ≥24pt、线条 ≥3px、键盘可翻页、可全屏

**样本 B — 转换模式自测**：对 `levels.html` 用转换模式产出一个 deck。
- 输入：`转换: levels.html`
- 预期产物：`slides/levels-deck.html`，约 10～11 张
- 核验项：L1～L8 各一张、表格去 shadow 表头改黑白、徽章去彩色改文字、ffmpeg 命令在深底代码页、剥离 header/footer

若自测发现问题，回补 Skill 正文的约束或模板，直到两份样本均通过自检。

---

## 附：与「1帧6秒」倡议的关系

本 Skill 是 `design.html`「PPT 抗压缩设计规范」的**可执行落地**：规范告诉人"该怎么做"，本 Skill 让 Agent "直接做出来"。遵循本 Skill 产出的幻灯片，在 L4/L5 级别（CRF 34 + stillimage）下的清晰度将等同于普通文稿在 CRF 28 下的效果，可在不牺牲阅读体验的前提下将视频体积再降低约 40%——这正是"源头适配"的复利效应。
