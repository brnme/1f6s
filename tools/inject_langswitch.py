#!/usr/bin/env python3
"""向全部已存在页面注入纯 CSS 语言切换下拉(details/summary,无 JS)。

- 存在性驱动:列表只列该页已存在的语言(tools/langs.py × PAGES)
- label 用 endonym,a 带 lang 属性;当前语言项 aria-current="true"(自身链接,
  CSS 高亮,保持可访问)
- 相对路径:页面在根 → {name}.html / {code}/{name}.html;
  页面在 {code}/ 下 → ../{name}.html / ../{code2}/{name}.html;同名 page
- 幂等:整块 <div class="lang-switch">…</div>(内部无嵌套 div)重写,
  details 结构同样落在该匹配内,重复运行零 diff
用法:python3 tools/inject_langswitch.py
"""
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # 不留 __pycache__,保持 git status 干净
from langs import LANGS, lang_by_code, pages_with_lang

ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    "index", "levels", "scenarios", "redlines", "design",
    "obs", "skill-ppt", "skill-compress", "license",
]

LANGSWITCH_RE = re.compile(r'<div class="lang-switch">.*?</div>', re.S)


def build_switch(name: str, cur_code: str) -> str:
    cur = lang_by_code(cur_code)
    rel = "../" if cur["subdir"] else ""
    items = []
    for l in pages_with_lang(name):
        href = f"{rel}{l['subdir']}{name}.html"
        current = ' aria-current="true"' if l["code"] == cur_code else ""
        items.append(
            f'        <li><a href="{href}" lang="{l["hreflang"]}"{current}>'
            f'{l["endonym"]}</a></li>'
        )
    return (
        '<div class="lang-switch">\n'
        f'      <details class="lang-menu">\n'
        f'        <summary lang="{cur["hreflang"]}" aria-label="Switch language / 切换语言">'
        f'{cur["endonym"]}</summary>\n'
        '        <ul>\n' + "\n".join(items) + '\n        </ul>\n'
        '      </details>\n'
        '    </div>'
    )


def main() -> int:
    injected = missing = 0
    for l in LANGS:
        sub = l["subdir"]
        for name in PAGES:
            page = ROOT / sub / f"{name}.html"
            if not page.exists():
                continue
            html = page.read_text(encoding="utf-8")
            block = build_switch(name, l["code"])
            new_html, n = LANGSWITCH_RE.subn(lambda m: block, html, count=1)
            if n == 0:
                print(f"[warn] {page} 无 lang-switch 块,未注入", file=sys.stderr)
                missing += 1
                continue
            if new_html != html:
                page.write_text(new_html, encoding="utf-8")
                injected += 1
    print(f"语言切换器已写入 {injected} 页,缺失块 {missing} 页")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
