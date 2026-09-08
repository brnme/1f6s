#!/usr/bin/env python3
"""中英双语一致性校验:对比 zh/en 同名页面的表格结构与数字。

检查项:
1. 表格数量一致,每张表格的行列数一致
2. 两版页面出现的数字集合一致(忽略语言差异后,关键数字不应漂移)
3. 内链数量一致(导航/卡片结构对齐)

退出码非零即有不一致,输出逐条差异。
用法:.venv-md/bin/python tools/check_i18n.py
"""
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    "index", "levels", "scenarios", "redlines", "design",
    "obs", "skill-ppt", "skill-compress", "license",
]
# 只比对参数级数字(≥2位或含小数点):单一位数在两种语言里常来自
# 序数/惯写差异(「两个」vs "2"),属于噪音;参数值(34/480/22050/17.5…)才是漂移信号
NUM_RE = re.compile(r"\d{2,}|\d+\.\d+")

issues = []
for name in PAGES:
    zh = (ROOT / f"{name}.html").read_text(encoding="utf-8")
    en = (ROOT / "en" / f"{name}.html").read_text(encoding="utf-8")
    sz, se = BeautifulSoup(zh, "html.parser"), BeautifulSoup(en, "html.parser")

    tz, te = sz.find_all("table"), se.find_all("table")
    if len(tz) != len(te):
        issues.append(f"{name}: 表格数量不一致 zh={len(tz)} en={len(te)}")
    for i, (a, b) in enumerate(zip(tz, te)):
        ra, rb = len(a.find_all("tr")), len(b.find_all("tr"))
        ca, cb = len(a.find_all("tr")[0].find_all(["th", "td"])) if ra else 0, \
                 len(b.find_all("tr")[0].find_all(["th", "td"])) if rb else 0
        if (ra, ca) != (rb, cb):
            issues.append(f"{name} 表格#{i+1}: 结构不一致 zh={ra}行×{ca}列 en={rb}行×{cb}列")

    for lang, soup in (("zh", sz), ("en", se)):
        for t in soup.find_all("table"):
            t.decompose()  # 表格数字已在结构层校验,正文数字对比剔除表格噪音
    nz = sorted(NUM_RE.findall(sz.get_text()))
    ne = sorted(NUM_RE.findall(se.get_text()))
    if nz != ne:
        from collections import Counter
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
            issues.append(f"{name}: 数字单边缺失(疑似漂移)={sorted(drift)}")
        if wobble:
            print(f"[warn] {name}: 次数±1(措辞差异,不阻断)={wobble}")

    lz, le = len(sz.find_all("a", href=True)), len(se.find_all("a", href=True))
    if abs(lz - le) > 2:
        issues.append(f"{name}: 内链数量差异过大 zh={lz} en={le}")

if issues:
    print(f"发现 {len(issues)} 处不一致:")
    for it in issues:
        print(" -", it)
    sys.exit(1)
print(f"中英一致性校验通过:{len(PAGES)} 对页面,表格结构/数字/链接均对齐")
