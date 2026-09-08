#!/usr/bin/env python3
"""向全站 18 页(zh 9 页 + en 9 页)注入分享/SEO/agent 元数据。

注入内容:
- favicon(SVG)链接
- canonical + hreflang 双语互指(zh / en / x-default)
- Open Graph(og:title/description/url/image/locale/site_name/type)
- twitter:card summary_large_image 系列
- <link rel="alternate" type="text/markdown"> 指向同名 .md(agent 内容层)
- 仅 index 两页:JSON-LD WebSite

幂等:已有 og:title 的页面自动跳过;重复运行无副作用。
用法:python3 tools/inject_meta.py(在仓库根目录执行)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://brnme.github.io/1f6s"
OG_IMAGE = f"{BASE}/assets/og-card.png"
PAGES = [
    "index", "levels", "scenarios", "redlines", "design",
    "obs", "skill-ppt", "skill-compress", "license",
]

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
DESC_RE = re.compile(r'<meta\s+name="description"\s+content="(.*?)"', re.S)
# 旧的单条 hreflang 行(改版前遗留),注入 hreflang 簇前先移除避免重复
OLD_HREFLANG_RE = re.compile(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*">')


def head_block(name: str, lang: str, title: str, desc: str) -> str:
    is_en = lang == "en"
    prefix = "en/" if is_en else ""
    url = f"{BASE}/{prefix}{name}.html"
    canonical_zh = f"{BASE}/{name}.html"
    canonical_en = f"{BASE}/en/{name}.html"
    canonical = canonical_en if is_en else canonical_zh
    md_href = f"{name}.md"  # .md 与页面同目录
    locale = "en_US" if is_en else "zh_CN"
    lines = [
        f'<link rel="icon" type="image/svg+xml" href="{"" if not is_en else "../"}assets/favicon.svg">',
        f'<link rel="canonical" href="{canonical}">',
        f'<link rel="alternate" hreflang="zh-CN" href="{canonical_zh}">',
        f'<link rel="alternate" hreflang="en" href="{canonical_en}">',
        f'<link rel="alternate" hreflang="x-default" href="{canonical_zh}">',
        f'<link rel="alternate" type="text/markdown" href="{md_href}" title="Markdown version for AI agents">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        f'<meta property="og:image:width" content="1200">',
        f'<meta property="og:image:height" content="630">',
        f'<meta property="og:locale" content="{locale}">',
        f'<meta property="og:locale:alternate" content="{"zh_CN" if is_en else "en_US"}">',
        f'<meta property="og:site_name" content="1帧6秒 · 1 Frame / 6 Seconds">',
        f'<meta property="og:type" content="{"website" if name == "index" else "article"}">',
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{title}">',
        f'<meta name="twitter:description" content="{desc}">',
        f'<meta name="twitter:image" content="{OG_IMAGE}">',
    ]
    if name == "index":
        site_name = "1 Frame / 6 Seconds" if is_en else "1帧6秒"
        jsonld = (
            '{"@context":"https://schema.org","@type":"WebSite",'
            f'"name":"{site_name}",'
            f'"alternateName":"1f6s video compression initiative",'
            f'"url":"{canonical}",'
            f'"description":"{desc}","inLanguage":"{"en" if is_en else "zh-CN"}"}}'
        )
        lines.append(f'<script type="application/ld+json">{jsonld}</script>')
    return "\n".join(lines)


def main() -> int:
    injected = skipped = 0
    for name in PAGES:
        for lang, subdir in (("zh", ROOT), ("en", ROOT / "en")):
            page = subdir / f"{name}.html"
            html = page.read_text(encoding="utf-8")
            if 'property="og:title"' in html:
                skipped += 1
                continue
            m_title = TITLE_RE.search(html)
            m_desc = DESC_RE.search(html)
            if not m_title or not m_desc:
                print(f"[skip] {page} 缺少 title/description,未注入", file=sys.stderr)
                continue
            title = m_title.group(1).strip()
            desc = m_desc.group(1).strip().replace('"', "&quot;")
            html = OLD_HREFLANG_RE.sub("", html)
            block = head_block(name, lang, title, desc)
            html = html.replace("</head>", block + "\n</head>", 1)
            page.write_text(html, encoding="utf-8")
            injected += 1
    print(f"注入 {injected} 页,跳过(已注入) {skipped} 页")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
