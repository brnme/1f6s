# AGENTS.md — 「1帧6秒」规范仓库操作守则

本仓库是 1帧6秒(1 Frame / 6 Seconds)视频压缩规范倡议的静态站点 + 规范资产库,部署于 GitHub Pages(https://brnme.github.io/1f6s/,main 分支根目录,推送即发布)。

## 仓库结构

- 根目录 `*.html`:中文站 10 页;`en/*.html`:英文镜像 10 页 —— **两版必须同步修改**
- `{ja,ko,vi,th,id,ms,hi,bn,de,fr,es,pt,it,ru,nl,pl,tr,cs,el,hu,ro,sv,uk,fi,da,bg,no,ar,fa,he}/`:30 个语言目录(已建,待翻译页面落地)—— 全站共 32 语言,矩阵由 `tools/langs.py` 注册表驱动,工具链全部存在性驱动(页面存在才处理)
- `tools/langs.py`:**语言注册表唯一真相源**(code/endonym/hreflang/og_locale/rtl/subdir),新语言必须先在此注册
- `tools/i18n/`:各语言翻译片段目录(`{code}.json`,JS 字典结构 + `_banner`;由 `tools/merge_i18n.py` 合并进 main.js)
- 翻译文档命名约定:`skill/SKILL.{lang}.md`、`skill/1f6s-compress/SKILL.{lang}.md`、`spec/README.{lang}.md`
- `assets/`:共享样式 `css/style.css`(手写、零依赖,含 32 语言字体回退与 .lang-menu 下拉、RTL 适配)与 `js/main.js`(原生 JS,zh/en 内联字典 + 合并区多语言字典)
- `studio.html` + `en/studio.html`:1f6s Studio(幻灯片导入 / 所见即所得编辑 / 源码 / 规范体检 / 播放 / 白板)——单文件自包含工具页;**en 镜像由 `tools/mirror_studio.py` 从其内嵌 i18n 字典生成,禁止手改**;改 UI 文案一律改 `studio.html` 字典后重跑镜像
- `tools/mirror_studio.py` / `tools/serve_studio.py`:Studio 英文镜像生成器 / 本地一键启动(默认 8765 端口)
- `spec/`:机器可读规范资产(levels/scenarios/redlines .json)—— 稳定 URL 层,只加不改旧语义
- `skill/1f6s-compress/`:1f6s.sh 压缩脚本 + SKILL.md(agent 手册)+ levels.json 随包副本
- `slides/`:宣传 deck 源文件与配音脚本(二进制产物被 .gitignore 排除,不入库)
- `*.md` 与 `llms-full.txt`、`sitemap.xml`:**派生产物**,见下

## 构建管线(改完 HTML 必须跑)

```bash
python3 tools/mirror_studio.py             # studio.html → en/studio.html(改了 Studio 必跑,先于注入)
python3 tools/merge_i18n.py               # 翻译片段(tools/i18n/*.json)合并进 main.js 的 I18N
python3 tools/inject_langswitch.py        # 语言切换器(details 下拉)注入全部已存在页面
python3 tools/inject_meta.py              # og/canonical/hreflang 强制重写注入(先剥离旧块)
.venv-md/bin/python tools/build_md.py     # 重新生成 .md 镜像/llms-full.txt/sitemap.xml(存在性驱动)
.venv-md/bin/python tools/check_i18n.py   # 多语言一致性校验(表格行列数+数字一致,zh 为基准)
```

- 顺序固定:翻译交付 → mirror_studio(仅 Studio)→ merge_i18n → inject_langswitch → inject_meta → build_md → check_i18n
- `.md`/`llms-full.txt`/`sitemap.xml` 一律由 `tools/build_md.py` 从 HTML 生成,**禁止手改**(会漂移)
- `.venv-md` 不存在时:`python3 -m venv .venv-md && .venv-md/bin/pip install markdownify beautifulsoup4`

## 内容铁律

1. `spec/levels.json` 是八级参数的唯一真相源;改参数时同步 `skill/1f6s-compress/levels.json`,并在提交信息注明版本变化
2. 所有 ffmpeg 命令默认 H.264/AAC + `yuv420p`(L8 除外);页面里的体积数字改了,`index.html` 估算器基准和 levels.json 的 `expected_mb` 也要对齐
3. 页面新增时:zh/en 成对添加,并在 `tools/build_md.py` 与 `tools/inject_meta.py` 的 `PAGES` 列表登记;其余语言尽快补齐;**新语言必须先在 `tools/langs.py` 注册**(含目录、i18n 片段与 banner)
4. 设计规范(对 HTML/CSS 同样适用):无衬线、仅黑/灰/白正文 + 青 #22d3ee / 荧光绿 #a3e635 强调、无阴影渐变滥用、线宽 ≥2px(1f6s 自家的抗压缩设计标准)
5. 版权页作者署名格式不要动;内容统一 CC BY 4.0

## 提交与发布

- 直接提交 main 即发布(GitHub Pages legacy 构建);敏感信息不入库(本仓库无密钥)
- 提交信息中文,说明「改了什么内容/参数,为何改」;涉及参数变更须写明新旧值
