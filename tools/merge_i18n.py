#!/usr/bin/env python3
"""把 tools/i18n/{code}.json 翻译片段幂等合并进 assets/js/main.js 的 I18N 字典。

- json 结构与 main.js 内 zh/en 字典内层一致(可含嵌套 levels/lvlName/selReason);
  以下划线开头的键为元数据(如 "_banner" 供 build_md.py 用),不合并
- calcSummary 在 main.js 中是函数 T.calcSummary(min, sec),json 无法表达:
  片段里写成含 {min}/{sec} 占位符的模板字符串,合并时自动包装为 JS 函数;
  缺失或不含占位符则该语言整体跳过并报错(避免线上 TypeError)
- 合并区以 // i18n:merge:start / // i18n:merge:end 标记,位于 I18N 对象字面量
  内 zh/en 之后;各语言块以「,code:」前导逗号书写,区间为空时语法仍成立
- 语言顺序与是否合并完全由 tools/langs.py × i18n/ 目录存在性决定(zh/en 除外)
- 无任何 json 时区间重写为空,保证幂等可回退
纯 stdlib。用法:python3 tools/merge_i18n.py
"""
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # 不留 __pycache__,保持 git status 干净
from langs import LANGS

ROOT = Path(__file__).resolve().parent.parent
MAIN_JS = ROOT / "assets" / "js" / "main.js"
I18N_DIR = Path(__file__).resolve().parent / "i18n"

MERGE_START = "// i18n:merge:start"
MERGE_END = "// i18n:merge:end"
MERGE_RE = re.compile(
    r"[ \t]*" + re.escape(MERGE_START) + r"\n.*?[ \t]*" + re.escape(MERGE_END), re.S
)


class RawJS:
    """已生成的 JS 源码片段(js_literal 原样输出)。"""

    def __init__(self, src: str):
        self.src = src


def wrap_calc_summary(template: str, code: str) -> RawJS:
    """把含 {min}/{sec} 占位符的模板包装为 main.js 所需的 JS 函数字面量。"""
    parts = re.split(r"(\{min\}|\{sec\})", template)
    if "{min}" not in template or "{sec}" not in template:
        raise ValueError(f"[{code}] calcSummary 模板必须同时含 {{min}} 与 {{sec}}")
    expr = []
    for p in parts:
        if p == "{min}":
            expr.append("min")
        elif p == "{sec}":
            expr.append("sec")
        elif p:
            expr.append(json.dumps(p, ensure_ascii=False))
    return RawJS(f"function (min, sec) {{ return {' + '.join(expr)}; }}")


def js_literal(value, indent: int) -> str:
    """dict/list/标量 → JS 对象字面量(json 字符串转义是合法 JS;处理 U+2028/9)。"""
    if isinstance(value, RawJS):
        return value.src
    pad = "  " * indent
    if isinstance(value, dict):
        if not value:
            return "{}"
        items = [
            f'{pad}  {json.dumps(str(k), ensure_ascii=False)}: {js_literal(v, indent + 1)}'
            for k, v in value.items()
        ]
        return "{\n" + ",\n".join(items) + "\n" + pad + "}"
    if isinstance(value, list):
        if not value:
            return "[]"
        items = [pad + "  " + js_literal(v, indent + 1) for v in value]
        return "[\n" + ",\n".join(items) + "\n" + pad + "]"
    if isinstance(value, bool):  # 须先于 int 判定(bool 是 int 子类)
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return json.dumps(value)
    return (
        json.dumps(str(value), ensure_ascii=False)
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def build_region() -> str:
    """按 LANGS 顺序重写合并区;无翻译片段时为空区间。"""
    lines = [f"    {MERGE_START}"]
    for l in LANGS:
        code = l["code"]
        if code in ("zh", "en"):
            continue  # 两语字典内联维护在 main.js
        frag = I18N_DIR / f"{code}.json"
        if not frag.exists():
            continue
        data = json.loads(frag.read_text(encoding="utf-8"))
        data = {k: v for k, v in data.items() if not k.startswith("_")}
        try:
            if "calcSummary" in data:
                data["calcSummary"] = wrap_calc_summary(data["calcSummary"], code)
        except ValueError as e:
            print(f"[error] {e},该语言未合并", file=sys.stderr)
            continue
        lines.append(f"    ,{code}: {js_literal(data, 2)}")
    lines.append(f"    {MERGE_END}")
    return "\n".join(lines)


def main() -> int:
    html = MAIN_JS.read_text(encoding="utf-8")
    m = MERGE_RE.search(html)
    if not m:
        print(f"[error] {MAIN_JS} 缺少 i18n:merge 标记区", file=sys.stderr)
        return 1
    region = build_region()
    n_langs = sum(1 for ln in region.splitlines() if ln.startswith("    ,"))
    html = MERGE_RE.sub(lambda _: region, html, count=1)
    MAIN_JS.write_text(html, encoding="utf-8")
    print(f"I18N 合并完成:本次合并 {n_langs} 个语言片段(zh/en 内联不动)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
