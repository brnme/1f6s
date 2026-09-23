#!/usr/bin/env python3
"""从 studio.html 生成 en/studio.html 英文镜像。

studio.html 内嵌双语字典（<script id="i18n-data">）是唯一真相源：
- 静态 HTML 文案 = zh 值；镜像时把文件中出现的 zh 值整串替换为 en 值
  （<title> 与 <meta name="description"> 亦然，对应键 page.title / page.desc）；
- 字典 JSON 块本身原样保留（运行时动态文案仍按 URL 判语言）；
- <html lang> 改为 en。

幂等：每次从 studio.html 全量重新生成，重复运行零 diff。
用法：python3 tools/mirror_studio.py（在仓库根目录执行）
"""
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # 不留 __pycache__,保持 git status 干净

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "studio.html"
DST = ROOT / "en" / "studio.html"


def main() -> int:
    html = SRC.read_text(encoding="utf-8")
    m = re.search(
        r'<script type="application/json" id="i18n-data">(.*?)</script>', html, re.S
    )
    if not m:
        print("[err] studio.html 未找到 i18n 字典块", file=sys.stderr)
        return 1
    data = json.loads(m.group(1))
    zh, en = data["zh"], data["en"]

    pre, dict_block, post = html[: m.start(1)], m.group(1), html[m.end(1):]

    # 只替换字典块之外出现的 zh 值（静态 HTML 文本 / title / description）
    body = pre + post
    pats = sorted(
        {v for v in zh.values() if v and v in body}, key=len, reverse=True
    )
    back = {}
    for k, v in zh.items():
        if v in pats:
            if v in back and back[v] != en.get(k):
                print(f"[warn] zh 值重复但 en 不同: {v[:30]}…", file=sys.stderr)
            back[v] = en.get(k, v)
    rx = re.compile("|".join(re.escape(p) for p in pats))
    count = [0]

    def rep(mm):
        count[0] += 1
        return back[mm.group(0)]

    def subst(seg):
        # 注释段整段跳过，避免短 zh 值误伤注释文字（如「导入中心」）
        parts = re.split(r"(<!--.*?-->)", seg)
        return "".join(
            p if p.startswith("<!--") else rx.sub(rep, p) for p in parts
        )

    # pre/post 各自替换后再拼接：替换会改变长度，不能按原始偏移切分
    new_html = subst(pre) + dict_block + subst(post)
    new_html = new_html.replace('<html lang="zh-CN">', '<html lang="en">', 1)

    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(new_html, encoding="utf-8")
    print(f"en/studio.html 已生成（替换 {count[0]} 处静态文案）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
