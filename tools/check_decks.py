#!/usr/bin/env python3
"""1f6s deck 静态校验器：对仓库内自包含 HTML deck 做与 Studio「规范体检」同口径的静态检查。

体检（studio.html lint()）按 iframe 内 computed style 实测；本脚本在生成侧做静态等价约束：
1. 结构：DOCTYPE / charset / title / html lang；≥8 个 <section class="slide">；
   active 恰好落在第一个 slide；.pager 与零依赖翻页脚本存在
2. 样式：<style> 块唯一，且逐字等于 CANONICAL_CSS（studio.html DECK_CSS 基准，
   全字号 ≥32px 口径）——deck 不得私自新增/修改 CSS 规则
3. 元素级：内联 style 仅允许 --h:NN%（图表柱高）；禁 <img>/<link>/<iframe>/
   <script src> 等一切外部引用（deck 必须零依赖单文件）
4. 禁用模式（样式层）：box-shadow / text-shadow / 衬线字体 / 三色之外颜色 /
   repeating-linear-gradient 之外的渐变 / <32px 字号 / <3px 边框

用法：python3 tools/check_decks.py [deck.html ...]
      无参数时扫描 examples/ 下全部 deck。退出码非零即有违规。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 与 studio.html 的 DECK_CSS 逐字一致（≥32px 口径）；deck 必须原样内嵌
CANONICAL_CSS = '''\
:root{--black:#000000;--gray:#808080;--white:#FFFFFF;--line:3px solid var(--black);--sans:"Source Han Sans SC","Microsoft YaHei","微软雅黑",Arial,Helvetica,sans-serif;--mono:"Cascadia Code","Consolas","Courier New",monospace;}
*{box-sizing:border-box;margin:0;padding:0;}html,body{height:100%;}
body{font-family:var(--sans);background:var(--white);color:var(--black);overflow:hidden;}
.deck{width:100vw;height:100vh;position:relative;}
.slide{width:100vw;height:100vh;padding:64px 80px;display:none;flex-direction:column;justify-content:center;background:var(--white);color:var(--black);}
.slide.active{display:flex;}
.slide-dark{background:var(--black);color:var(--white);}.slide-dark .deck-h2,.slide-dark .deck-h3{color:var(--white);}
.deck-h2-light{color:var(--white) !important;}
.slide-cover{align-items:center;text-align:center;}
.deck-title{font-size:56px;font-weight:700;line-height:1.2;}
.deck-h2{font-size:48px;font-weight:700;line-height:1.25;margin-bottom:32px;}
.deck-h3{font-size:40px;font-weight:700;line-height:1.3;margin-bottom:20px;}
.deck-body{font-size:32px;font-weight:700;line-height:1.5;}
.deck-muted{font-size:37px;color:var(--gray);font-weight:700;line-height:1.4;}
.deck-list{list-style:none;padding:0;}
.deck-list li{font-size:32px;font-weight:700;line-height:1.5;padding:10px 0;border-bottom:var(--line);}
.deck-list li:last-child{border-bottom:none;}
ol.deck-list{counter-reset:deck;}ol.deck-list li{counter-increment:deck;padding-left:56px;position:relative;}
ol.deck-list li::before{content:counter(deck)". ";position:absolute;left:0;font-weight:700;}
.deck-tbl-wrap{overflow-x:auto;}
.deck-tbl{width:100%;border-collapse:collapse;font-size:32px;font-weight:700;}
.deck-tbl th,.deck-tbl td{border:var(--line);padding:14px 18px;text-align:left;}
.deck-tbl thead th{background:var(--black);color:var(--white);}.deck-tbl tbody tr{background:var(--white);}
.deck-callout{border:var(--line);padding:24px 28px;margin-top:24px;background:var(--white);}
.deck-callout-title{font-size:36px;font-weight:700;margin-bottom:12px;}
.deck-callout p{font-size:32px;font-weight:700;line-height:1.5;}
.deck-callout-warn{border-width:5px;}.deck-callout-warn .deck-callout-title::before{content:"⚠ ";}
.deck-badge{display:inline-block;border:var(--line);padding:4px 14px;font-size:32px;font-weight:700;margin-right:12px;background:var(--white);}
.deck-checklist{list-style:none;padding:0;}.deck-checklist li{font-size:32px;font-weight:700;line-height:1.6;padding:8px 0;}
.deck-code{background:var(--black);color:var(--white);font-family:var(--mono);font-size:32px;line-height:1.5;padding:28px 32px;overflow-x:auto;white-space:pre;border:var(--line);}
.deck-chart{display:flex;align-items:flex-end;gap:32px;height:300px;border-bottom:var(--line);}
.bar{width:96px;background:var(--white);border:var(--line);height:var(--h);}
.bar-solid{background:var(--black);}.bar-outline{background:var(--white);}
.bar-hatch{background:repeating-linear-gradient(45deg,var(--black) 0 8px,var(--white) 8px 16px);}
.deck-legend{list-style:none;display:flex;gap:28px;margin-top:20px;padding:0;}
.deck-legend li{font-size:32px;font-weight:700;display:flex;align-items:center;gap:10px;}
.sw{display:inline-block;width:24px;height:24px;border:3px solid var(--black);}
.sw-solid{background:var(--black);}.sw-outline{background:var(--white);}
.sw-hatch{background:repeating-linear-gradient(45deg,var(--black) 0 4px,var(--white) 4px 8px);}
.deck-two{display:flex;gap:0;margin-top:16px;}.deck-two>div{flex:1;padding:0 32px;}.deck-two>div+div{border-left:var(--line);}
.pager{position:fixed;right:32px;bottom:24px;font-size:32px;font-weight:700;color:var(--gray);background:var(--white);padding:4px 12px;border:var(--line);}'''

OK_HEX = {"#000000", "#808080", "#ffffff"}
EXTERNAL_TAGS = ("<img", "<link", "<iframe", "<video", "<audio", "<object", "<embed", "<source", "<picture")


def check(path: Path) -> list:
    errs = []
    html = path.read_text(encoding="utf-8")

    # ---- 1) 结构 ----
    if "<!DOCTYPE html>" not in html:
        errs.append("缺少 <!DOCTYPE html>")
    if '<meta charset="UTF-8">' not in html:
        errs.append("缺少 charset 声明")
    if not re.search(r'<html lang="', html):
        errs.append("缺少 <html lang=...>")
    if not re.search(r"<title>\s*\S.*?</title>", html, re.S):
        errs.append("缺少非空 <title>")
    slide_classes = []
    for attrs in re.findall(r"<section\b([^>]*)>", html):
        m = re.search(r'class="([^"]*)"', attrs)
        slide_classes.append((m.group(1) if m else "").split())
    slides = [i for i, c in enumerate(slide_classes) if "slide" in c]
    if len(slides) < 8:
        errs.append(f"slide 页数不足: {len(slides)} < 8")
    if slides:
        actives = [i for i in slides if "active" in slide_classes[i]]
        if actives != [slides[0]]:
            errs.append(f"active 必须恰好出现在第一个 slide 上,实际落在 {actives}")
    if '<div class="pager">' not in html:
        errs.append("缺少 .pager 页码")
    if "querySelectorAll('.slide')" not in html:
        errs.append("缺少零依赖翻页脚本")

    # ---- 2) 样式块唯一且为 canonical ----
    styles = re.findall(r"<style[^>]*>(.*?)</style>", html, re.S)
    if len(styles) != 1:
        errs.append(f"<style> 块应为 1 个,实际 {len(styles)}")
        css = ""
    else:
        css = styles[0].strip()
        if css != CANONICAL_CSS.strip():
            got, want = css.splitlines(), CANONICAL_CSS.strip().splitlines()
            diff = next(
                (i for i, (a, b) in enumerate(zip(got, want)) if a != b),
                min(len(got), len(want)),
            )
            detail = got[diff][:60] if diff < len(got) else "<无此行>"
            errs.append(f"<style> 与 DECK_CSS 基准不一致(第 {diff + 1} 行起): {detail}")

    # ---- 3) 元素级 ----
    for m in re.finditer(r'style="([^"]*)"', html):
        v = m.group(1).strip()
        if not re.fullmatch(r"--h:\d{1,3}%", v):
            errs.append(f"非法内联 style: {v!r}(仅允许 --h:NN% 柱高)")
    for tag in EXTERNAL_TAGS:
        if tag in html:
            errs.append(f"出现外部引用标签 {tag}")
    if re.search(r"<script[^>]*\ssrc=", html):
        errs.append("出现 <script src=...> 外部脚本")

    # ---- 4) 禁用模式(样式层) ----
    for pat in ("box-shadow", "text-shadow", "rgb(", "hsl("):
        if pat in css:
            errs.append(f"样式含禁用声明: {pat}")
    if re.search(r"(?<!sans-)serif", css) or re.search(r"宋体|楷体|Times|Song|Kai", css):
        errs.append("样式含衬线字体")
    for m in re.finditer(r"(repeating-)?(linear|radial|conic)-gradient", css):
        if not m.group(1) or m.group(2) != "linear":
            errs.append(f"非斜纹渐变: {m.group(0)}")
    for h in re.findall(r"#[0-9a-fA-F]{3,8}\b", css):
        if h.lower() not in OK_HEX:
            errs.append(f"三色之外的颜色: {h}")
    for v in re.findall(r"font-size:\s*([\d.]+)px", css):
        if float(v) < 32:
            errs.append(f"字号 <32px: {v}px")
    for v in re.findall(r"border[a-z-]*:\s*([\d.]+)px", css):
        if float(v) < 3:
            errs.append(f"边框 <3px: {v}px")
    return errs


def main() -> int:
    args = sys.argv[1:]
    paths = [Path(a) for a in args] if args else sorted(ROOT.glob("examples/*/*-deck.html"))
    if not paths:
        print("未找到待校验 deck(examples/*/*-deck.html)")
        return 0
    failed = 0
    for p in paths:
        errs = check(p)
        if errs:
            failed += 1
            print(f"[FAIL] {p}")
            for e in errs:
                print(f"       - {e}")
        else:
            n = len(re.findall(r'<section\b[^>]*class="[^"]*\bslide\b', p.read_text(encoding="utf-8")))
            print(f"[PASS] {p} ({n} 页)")
    if failed:
        print(f"共 {failed}/{len(paths)} 个 deck 未通过")
        return 1
    print(f"全部 {len(paths)} 个 deck 通过校验")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
