#!/usr/bin/env python3
"""向全站已存在页面(zh 9 页 + en 9 页,矩阵可扩展)注入分享/SEO/agent 元数据。

注入内容(以 <!-- inject_meta:start --> / <!-- inject_meta:end --> 包裹,
置于 </head> 前):
- favicon(SVG)链接(相对前缀按语言目录)
- canonical + hreflang 全语言矩阵(该页存在的语言 + x-default→zh 根页)
- Open Graph(og:title/description/url/image/locale/locale:alternate/site_name/type)
- twitter:card summary_large_image 系列
- <link rel="alternate" type="text/markdown"> 指向同名 .md(agent 内容层)
- 仅 index 两页(每语言):JSON-LD WebSite

强制重写:每次运行先剥离旧注入块(标记注释,或无标记历史页的逐行模式
匹配)再重新注入——已注入页面也能随语言矩阵升级,不再是「注入即跳过」。
手写内容(<title>、<meta name="description">、charset/viewport、stylesheet)
永不触碰。
用法:python3 tools/inject_meta.py(在仓库根目录执行)
"""
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # 不留 __pycache__,保持 git status 干净
from langs import LANGS, lang_by_code, pages_with_lang

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://brnme.github.io/1f6s"
OG_IMAGE = f"{BASE}/assets/og-card.png"
PAGES = [
    "index", "levels", "scenarios", "redlines", "design",
    "obs", "skill-ppt", "skill-compress", "examples", "studio", "license",
]

INJECT_START = "<!-- inject_meta:start -->"
INJECT_END = "<!-- inject_meta:end -->"
MARKER_BLOCK_RE = re.compile(
    re.escape(INJECT_START) + r"\n.*?" + re.escape(INJECT_END) + r"\n", re.S
)

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
DESC_RE = re.compile(r'<meta\s+name="description"\s+content="(.*?)"', re.S)

# 无标记历史页的剥离模式:整行匹配才删,绝不波及 title/description/charset
LEGACY_LINE_PREFIXES = (
    '<link rel="icon"',
    '<link rel="canonical"',
    '<link rel="alternate"',  # 含 hreflang 与 text/markdown 两种
    '<meta property="og:',
    '<meta name="twitter:',
)


def strip_injected(html: str, name: str) -> str:
    """剥离旧注入块。两层:标记注释整体删除;无标记历史块逐行模式删除。"""
    html = MARKER_BLOCK_RE.sub("", html)
    kept = []
    for line in html.splitlines(keepends=True):
        s = line.strip()
        if s.startswith(LEGACY_LINE_PREFIXES):
            continue
        if (
            name == "index"
            and s.startswith('<script type="application/ld+json">')
            and '"@type":"WebSite"' in s
        ):
            continue
        kept.append(line)
    return "".join(kept)


def head_block(name: str, lang: str, title: str, desc: str) -> str:
    me = lang_by_code(lang)
    present = pages_with_lang(name)  # 该页已存在的语言,全矩阵互指
    rel = "../" if me["subdir"] else ""  # 相对资源前缀
    url = f"{BASE}/{me['subdir']}{name}.html"
    lines = [
        f'<link rel="icon" type="image/svg+xml" href="{rel}assets/favicon.svg">',
        f'<link rel="canonical" href="{url}">',
    ]
    for l in present:
        lines.append(
            f'<link rel="alternate" hreflang="{l["hreflang"]}"'
            f' href="{BASE}/{l["subdir"]}{name}.html">'
        )
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}/{name}.html">')
    lines.append(
        '<link rel="alternate" type="text/markdown" href="{0}.md"'
        ' title="Markdown version for AI agents">'.format(name)
    )
    lines += [
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        f'<meta property="og:image:width" content="1200">',
        f'<meta property="og:image:height" content="630">',
        f'<meta property="og:locale" content="{me["og_locale"]}">',
    ]
    for l in present:
        if l["code"] != lang:
            lines.append(
                f'<meta property="og:locale:alternate" content="{l["og_locale"]}">'
            )
    lines += [
        '<meta property="og:site_name" content="1帧6秒 · 1 Frame / 6 Seconds">',
        f'<meta property="og:type" content="{"website" if name == "index" else "article"}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{title}">',
        f'<meta name="twitter:description" content="{desc}">',
        f'<meta name="twitter:image" content="{OG_IMAGE}">',
    ]
    if name == "index":
        site_name = "1 Frame / 6 Seconds" if lang == "en" else "1帧6秒"
        jsonld = (
            '{"@context":"https://schema.org","@type":"WebSite",'
            f'"name":"{site_name}",'
            f'"alternateName":"1f6s video compression initiative",'
            f'"url":"{url}",'
            f'"description":"{desc}","inLanguage":"{me["hreflang"]}"}}'
        )
        lines.append(f'<script type="application/ld+json">{jsonld}</script>')
    return "\n".join(lines)


def main() -> int:
    injected = skipped = 0
    for l in LANGS:
        sub = l["subdir"]
        for name in PAGES:
            page = ROOT / sub / f"{name}.html"
            if not page.exists():
                continue
            html = strip_injected(page.read_text(encoding="utf-8"), name)
            m_title = TITLE_RE.search(html)
            m_desc = DESC_RE.search(html)
            if not m_title or not m_desc:
                print(f"[skip] {page} 缺少 title/description,未注入", file=sys.stderr)
                skipped += 1
                continue
            title = m_title.group(1).strip()
            desc = m_desc.group(1).strip().replace('"', "&quot;")
            block = INJECT_START + "\n" + head_block(name, l["code"], title, desc) + "\n" + INJECT_END
            html = html.replace("</head>", block + "\n</head>", 1)
            page.write_text(html, encoding="utf-8")
            injected += 1
    print(f"重写注入 {injected} 页,跳过(缺 title/description) {skipped} 页")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
