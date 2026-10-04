#!/usr/bin/env python3
"""规范站的 agent 内容层构建管线。

HTML 是唯一内容源,本脚本按 语言矩阵(tools/langs.py)× PAGES 存在性派生:
- 每页 {subdir}{page}.md(agent 友好的 Markdown 镜像,zh 在根、en 在 en/)
- {subdir}llms-full.txt(各语言全站合并单文件)
- sitemap.xml(已存在页面的全语言矩阵 + hreflang,x-default 指向 zh 根页)

存在性驱动:{subdir}{name}.html 存在才生成对应 .md 并收入该语言 llms parts;
新语言目录建好即自动纳入矩阵,无需改本脚本(仅 banner/翻译另行交付)。
幂等:每次从 HTML 全量重新生成,重复运行零 diff(HTML 不变则产物不变)。
用法:.venv-md/bin/python tools/build_md.py(需 markdownify + beautifulsoup4)
"""
import json
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify

sys.dont_write_bytecode = True  # 不留 __pycache__,保持 git status 干净
from langs import LANGS, lang_by_code, pages_with_lang

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://brnme.github.io/1f6s"
PAGES = [
    "index", "levels", "scenarios", "redlines", "design",
    "obs", "skill-ppt", "skill-compress", "examples", "studio", "license",
]
PAGE_TITLES = {}  # name -> {lang: title},运行时填充,sitemap 与 md 头部共用

# 各语言 llms-full.txt 头部 banner。zh/en 为字面基线文本(en 与历史
# replace 链的输出逐字节一致,勿改动);其余语言从 tools/i18n/{code}.json
# 的 "_banner" 键读取,读不到则回退 en banner。
BANNERS = {
    "zh": (
        "# 1帧6秒(1 Frame / 6 Seconds)——讲解类视频压缩标准倡议 · 全站全文\n\n"
        f"> 本文件为 {BASE}/llms-full.txt,由 tools/build_md.py 自动生成,"
        "供 AI agent 一次性读取全站内容。规范版本 v1.0,CC BY 4.0。\n\n"
    ),
    "en": (
        "# 1 Frame / 6 Seconds (1f6s)——Video Compression Initiative — full site text\n\n"
        f"> 本文件为 {BASE}/llms-full.txt,由 tools/build_md.py 自动生成,"
        "generated for one-shot ingestion by AI agents。规范版本 v1.0,CC BY 4.0。\n\n"
    ),
}

# 移除:导航/页脚/交互控件/画布——对 agent 无信息量,保留会稀释正文
STRIP_SELECTORS = [
    "header.site-header", "footer.site-footer", "script", "noscript",
    "canvas", ".tool-panel", ".lang-switch", "#hero-canvas",
]


def banner_for(code: str) -> str:
    """取某语言的 llms-full.txt banner;翻译片段优先,缺失回退 en。"""
    if code in BANNERS:
        return BANNERS[code]
    frag = Path(__file__).resolve().parent / "i18n" / f"{code}.json"
    if frag.exists():
        data = json.loads(frag.read_text(encoding="utf-8"))
        banner = data.get("_banner")
        if banner:
            return banner
    return BANNERS["en"]


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
    sub = lang_by_code(lang)["subdir"]
    header = (
        f"# {title}\n\n"
        f"> 1帧6秒倡议 · {BASE}/{sub}{name}.html · 本文为 Markdown 镜像,"
        f"[HTML 原版]({name}.html)含交互组件。\n\n"
        f"---\n\n"
    )
    return header + "\n".join(out).strip() + "\n"


def sitemap_xml() -> str:
    """存在性驱动:某页存在的语言集合内生成全矩阵 hreflang + x-default。"""
    urls = []
    for name in PAGES:
        present = pages_with_lang(name)
        if not present:
            continue
        alternates = "".join(
            f'\n    <xhtml:link rel="alternate" hreflang="{l["hreflang"]}"'
            f' href="{BASE}/{l["subdir"]}{name}.html"/>'
            for l in present
        )
        alternates += (
            f'\n    <xhtml:link rel="alternate" hreflang="x-default"'
            f' href="{BASE}/{name}.html"/>'
        )
        for l in present:
            loc = f"{BASE}/{l['subdir']}{name}.html"
            urls.append(f"  <url>\n    <loc>{loc}</loc>{alternates}\n  </url>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls) + "\n</urlset>\n"
    )


def main() -> int:
    wrote = []
    parts = {l["code"]: [] for l in LANGS}
    # 语言 × 页面 存在性驱动:页面 HTML 存在才生成 .md 并收入该语言 parts
    for l in LANGS:
        code, sub = l["code"], l["subdir"]
        for name in PAGES:
            page = ROOT / sub / f"{name}.html"
            if not page.exists():
                continue
            md = to_markdown(page, name, code)
            (ROOT / sub / f"{name}.md").write_text(md, encoding="utf-8")
            parts[code].append(md)
            wrote.append(f"{sub}{name}.md")

    for l in LANGS:
        code = l["code"]
        if not parts[code]:
            continue
        out = ROOT / l["subdir"] / "llms-full.txt"
        out.write_text(
            banner_for(code) + "\n\n---\n\n".join(parts[code]), encoding="utf-8"
        )
        wrote.append(f"{l['subdir']}llms-full.txt")

    (ROOT / "sitemap.xml").write_text(sitemap_xml(), encoding="utf-8")
    wrote.append("sitemap.xml")
    print(f"生成 {len(wrote)} 个文件:", ", ".join(wrote))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
