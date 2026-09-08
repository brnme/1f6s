# AGENTS.md — 「1帧6秒」规范仓库操作守则

本仓库是 1帧6秒(1 Frame / 6 Seconds)视频压缩规范倡议的静态站点 + 规范资产库,部署于 GitHub Pages(https://brnme.github.io/1f6s/,main 分支根目录,推送即发布)。

## 仓库结构

- 根目录 `*.html`:中文站 9 页;`en/*.html`:英文镜像 9 页 —— **两版必须同步修改**
- `assets/`:共享样式 `css/style.css`(963 行手写、零依赖)与 `js/main.js`(原生 JS,内置 zh/en 双语文案字典)
- `spec/`:机器可读规范资产(levels/scenarios/redlines .json)—— 稳定 URL 层,只加不改旧语义
- `skill/1f6s-compress/`:1f6s.sh 压缩脚本 + SKILL.md(agent 手册)+ levels.json 随包副本
- `slides/`:宣传 deck 源文件与配音脚本(二进制产物被 .gitignore 排除,不入库)
- `*.md` 与 `llms-full.txt`、`sitemap.xml`:**派生产物**,见下

## 构建管线(改完 HTML 必须跑)

```bash
.venv-md/bin/python tools/build_md.py     # 重新生成 .md 镜像/llms-full.txt/sitemap.xml
python3 tools/inject_meta.py              # 新页面注入 og/canonical/hreflang(幂等,已注入则跳过)
.venv-md/bin/python tools/check_i18n.py   # 中英一致性校验(表格行列数+数字一致)
```

- `.md`/`llms-full.txt`/`sitemap.xml` 一律由 `tools/build_md.py` 从 HTML 生成,**禁止手改**(会漂移)
- `.venv-md` 不存在时:`python3 -m venv .venv-md && .venv-md/bin/pip install markdownify beautifulsoup4`

## 内容铁律

1. `spec/levels.json` 是八级参数的唯一真相源;改参数时同步 `skill/1f6s-compress/levels.json`,并在提交信息注明版本变化
2. 所有 ffmpeg 命令默认 H.264/AAC + `yuv420p`(L8 除外);页面里的体积数字改了,`index.html` 估算器基准和 levels.json 的 `expected_mb` 也要对齐
3. 页面新增时:zh/en 成对添加,并在 `tools/build_md.py` 与 `tools/inject_meta.py` 的 `PAGES` 列表登记
4. 设计规范(对 HTML/CSS 同样适用):无衬线、仅黑/灰/白正文 + 青 #22d3ee / 荧光绿 #a3e635 强调、无阴影渐变滥用、线宽 ≥2px(1f6s 自家的抗压缩设计标准)
5. 版权页作者署名格式不要动;内容统一 CC BY 4.0

## 提交与发布

- 直接提交 main 即发布(GitHub Pages legacy 构建);敏感信息不入库(本仓库无密钥)
- 提交信息中文,说明「改了什么内容/参数,为何改」;涉及参数变更须写明新旧值
