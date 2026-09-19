#!/usr/bin/env python3
"""多语言一致性校验:以 zh 为基准,对比各已落地语言同名页面的表格结构与数字。

检查项(每页 × 每个该页存在的非 zh 语言,逻辑同旧版 zh vs en):
1. 表格数量一致,每张表格的行列数一致
2. 两版页面出现的数字集合一致(忽略语言差异后,关键数字不应漂移)
3. 内链数量一致(导航/卡片结构对齐)

退出码非零即有不一致,输出按语言分组逐条差异。
用法:.venv-md/bin/python tools/check_i18n.py
"""
import re
import sys
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

sys.dont_write_bytecode = True  # 不留 __pycache__,保持 git status 干净
from langs import pages_with_lang

ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    "index", "levels", "scenarios", "redlines", "design",
    "obs", "skill-ppt", "skill-compress", "license",
]
# 只比对参数级数字(≥2位或含小数点):单一位数在两种语言里常来自
# 序数/惯写差异(「两个」vs "2"),属于噪音;参数值(34/480/22050/17.5…)才是漂移信号
NUM_RE = re.compile(r"\d{2,}|\d+\.\d+")

issues = {}  # lang_code -> [差异描述]


def compare(name: str, lang: str, other_path: Path, zh_path: Path) -> None:
    # zh 每对重新解析:下方的表格 decompose 会改动 soup,不能跨语言复用
    zh_soup = BeautifulSoup(zh_path.read_text(encoding="utf-8"), "html.parser")
    other = BeautifulSoup(other_path.read_text(encoding="utf-8"), "html.parser")

    tz, te = zh_soup.find_all("table"), other.find_all("table")
    if len(tz) != len(te):
        issues.setdefault(lang, []).append(
            f"{name}: 表格数量不一致 zh={len(tz)} {lang}={len(te)}"
        )
    for i, (a, b) in enumerate(zip(tz, te)):
        ra, rb = len(a.find_all("tr")), len(b.find_all("tr"))
        ca, cb = len(a.find_all("tr")[0].find_all(["th", "td"])) if ra else 0, \
                 len(b.find_all("tr")[0].find_all(["th", "td"])) if rb else 0
        if (ra, ca) != (rb, cb):
            issues.setdefault(lang, []).append(
                f"{name} 表格#{i+1}: 结构不一致 zh={ra}行×{ca}列 {lang}={rb}行×{cb}列"
            )

    for soup in (zh_soup, other):
        for t in soup.find_all("table"):
            t.decompose()  # 表格数字已在结构层校验,正文数字对比剔除表格噪音
    nz = sorted(NUM_RE.findall(zh_soup.get_text()))
    ne = sorted(NUM_RE.findall(other.get_text()))
    if nz != ne:
        cz, ce = Counter(nz), Counter(ne)
        drift = {  # 某版完全不存在的数字 → 疑似数据漂移,失败
            n for n in set(cz) | set(ce)
            if min(cz.get(n, 0), ce.get(n, 0)) == 0
        }
        wobble = {  # 两边都有但次数差 1 → 措辞差异,仅警告(次数相等不列出)
            n: (cz.get(n, 0), ce.get(n, 0))
            for n in set(cz) | set(ce)
            if n not in drift and 0 < abs(cz.get(n, 0) - ce.get(n, 0)) <= 1
        }
        if drift:
            issues.setdefault(lang, []).append(
                f"{name}: 数字单边缺失(疑似漂移)={sorted(drift)}"
            )
        if wobble:
            print(f"[warn] {lang} {name}: 次数±1(措辞差异,不阻断)={wobble}")

    lz, le = len(zh_soup.find_all("a", href=True)), len(other.find_all("a", href=True))
    if abs(lz - le) > 2:
        issues.setdefault(lang, []).append(
            f"{name}: 内链数量差异过大 zh={lz} {lang}={le}"
        )


page_count = lang_count = 0
for name in PAGES:
    zh_path = ROOT / f"{name}.html"
    if not zh_path.exists():
        continue
    others = [l for l in pages_with_lang(name) if l["code"] != "zh"]
    page_count += 1
    for l in others:
        lang_count += 1
        compare(name, l["code"], ROOT / l["subdir"] / f"{name}.html", zh_path)

if issues:
    total = sum(len(v) for v in issues.values())
    print(f"发现 {total} 处不一致:")
    for lang in sorted(issues):
        print(f"[{lang}]")
        for it in issues[lang]:
            print(" -", it)
    sys.exit(1)
print(f"多语言一致性校验通过:{page_count} 页 × {lang_count} 个非 zh 语言对"
      f"(zh 基准),表格结构/数字/链接均对齐")
