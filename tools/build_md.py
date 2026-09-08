#!/usr/bin/env python3
"""规范站的 agent 内容层构建管线。

HTML 是唯一内容源,本脚本派生:
- 每页 {page}.md / en/{page}.md(agent 友好的 Markdown 镜像)
- llms-full.txt / en/llms-full.txt(全站合并单文件)
- sitemap.xml(18 URL + hreflang)

幂等:每次从 HTML 全量重新生成,重复运行零 diff(HTML 不变则产物不变)。
用法:.venv-md/bin/python tools/build_md.py(需 markdownify + beautifulsoup4)
"""
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://brnme.github.io/1f6s"
PAGES = [
    "index", "levels", "scenarios", "redlines", "design",
    "obs", "skill-ppt", "skill-compress", "license",
]
PAGE_TITLES = {}  # name -> (zh_title, en_title),sitemap 与 md 头部共用

# 移除:导航/页脚/交互控件/画布——对 agent 无信息量,保留会稀释正文
STRIP_SELECTORS = [
    "header.site-header", "footer.site-footer", "script", "noscript",
    "canvas", ".tool-panel", ".lang-switch", "#hero-canvas",
]


def to_markdown(page: Path, name: str, lang: str) -> str:
    html = page.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    for sel in STRIP_SELECTORS:
        for el in soup.select(sel):
            el.decompose()
    # 术语表 dl → 强调词条段落(markdownify 对 dl 支持弱)
    for item in soup.select(".glossary-item"):
        term = item.dt.get_text(" ", strip=True) if item.dt else ""
        defn = item.dd.get_text(" ", strip=True) if item.dd else ""
        item.replace_with(
            BeautifulSoup(f"<p><strong>{term}</strong> — {defn}</p>", "html.parser")
        )
    # FAQ details/summary → 加粗问题 + 回答段落
    for det in soup.select("details.faq-item"):
        q = det.summary.get_text(" ", strip=True) if det.summary else ""
        det.summary.decompose()
        a = det.get_text(" ", strip=True)
        det.replace_with(
            BeautifulSoup(f"<p><strong>Q:{q}</strong></p><p>{a}</p>", "html.parser")
        )
    main = soup.main if soup.main else soup.body
    # 正文 h1 降为 h2:文档头已提供唯一 H1(llms-full.txt 合并时每页一个 H1)
    for h in main.find_all("h1"):
        h.name = "h2"
    md = markdownify(str(main), heading_style="ATX", bullets="-")
    # 去掉代码块语言标签上的"复制"按钮残字(如「bash · ffmpeg复制」)
    md = "\n".join(
        ln[:-2].rstrip(" ·") if ln.endswith("复制") else ln
        for ln in md.splitlines()
    )
    # 压缩 3+ 连续空行;去掉每行尾随空格
    lines = [ln.rstrip() for ln in md.splitlines()]
    out, blank = [], 0
    for ln in lines:
        blank = blank + 1 if not ln.strip() else 0
        if blank <= 1:
            out.append(ln)
    title = soup.title.get_text(strip=True) if soup.title else name
    PAGE_TITLES.setdefault(name, {})[lang] = title
    prefix = "en/" if lang == "en" else ""
    header = (
        f"# {title}\n\n"
        f"> 1帧6秒倡议 · {BASE}/{prefix}{name}.html · 本文为 Markdown 镜像,"
        f"[HTML 原版]({'' if lang == 'en' else ''}{name}.html)含交互组件。\n\n"
        f"---\n\n"
    )
    return header + "\n".join(out).strip() + "\n"


def sitemap_xml() -> str:
    urls = []
    for name in PAGES:
        zh, en = f"{BASE}/{name}.html", f"{BASE}/en/{name}.html"
        urls.append(
            f"  <url>\n    <loc>{zh}</loc>\n"
            f'    <xhtml:link rel="alternate" hreflang="zh-CN" href="{zh}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{zh}"/>\n'
            f"  </url>"
        )
        urls.append(
            f"  <url>\n    <loc>{en}</loc>\n"
            f'    <xhtml:link rel="alternate" hreflang="zh-CN" href="{zh}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{zh}"/>\n'
            f"  </url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls) + "\n</urlset>\n"
    )


def main() -> int:
    wrote = []
    zh_parts, en_parts = [], []
    for name in PAGES:
        zh_md = to_markdown(ROOT / f"{name}.html", name, "zh")
        en_md = to_markdown(ROOT / "en" / f"{name}.html", name, "en")
        (ROOT / f"{name}.md").write_text(zh_md, encoding="utf-8")
        (ROOT / "en" / f"{name}.md").write_text(en_md, encoding="utf-8")
        zh_parts.append(zh_md)
        en_parts.append(en_md)
        wrote += [f"{name}.md", f"en/{name}.md"]

    banner = (
        "# 1帧6秒(1 Frame / 6 Seconds)——讲解类视频压缩标准倡议 · 全站全文\n\n"
        f"> 本文件为 {BASE}/llms-full.txt,由 tools/build_md.py 自动生成,"
        "供 AI agent 一次性读取全站内容。规范版本 v1.0,CC BY 4.0。\n\n"
    )
    (ROOT / "llms-full.txt").write_text(banner + "\n\n---\n\n".join(zh_parts), encoding="utf-8")
    (ROOT / "en" / "llms-full.txt").write_text(
        banner.replace("1帧6秒(1 Frame / 6 Seconds)", "1 Frame / 6 Seconds (1f6s)")
        .replace("讲解类视频压缩标准倡议 · 全站全文", "Video Compression Initiative — full site text")
        .replace("供 AI agent 一次性读取全站内容", "generated for one-shot ingestion by AI agents")
        + "\n\n---\n\n".join(en_parts),
        encoding="utf-8",
    )
    (ROOT / "sitemap.xml").write_text(sitemap_xml(), encoding="utf-8")
    wrote += ["llms-full.txt", "en/llms-full.txt", "sitemap.xml"]
    print(f"生成 {len(wrote)} 个文件:", ", ".join(wrote))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
