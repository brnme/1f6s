#!/usr/bin/env python3
"""语言注册表 —— 全站 32 语言矩阵的唯一真相源。

tools/build_md.py / inject_meta.py / inject_langswitch.py / check_i18n.py /
merge_i18n.py 均从本模块读取语言列表,新增语言三步:
1. 在 LANGS 按顺序追加一条记录(subdir 一律 f"{code}/",zh 固定为 "")
2. 建好 {code}/ 目录(空目录即可,工具全部存在性驱动)
3. 翻译交付:tools/i18n/{code}.json(含 "_banner")→ merge_i18n → 
   inject_langswitch → inject_meta → build_md → check_i18n

纯 stdlib,无第三方依赖。
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://brnme.github.io/1f6s"

# 字段:code(目录/字典键) endonym(自称,语言切换器 label)
#      hreflang(<link hreflang> 与 JSON-LD inLanguage) og_locale(og:locale)
#      rtl(从右向左) subdir(站点内相对根目录,zh 为根)
LANGS = [
    {"code": "zh", "endonym": "中文",             "hreflang": "zh-CN", "og_locale": "zh_CN", "rtl": False, "subdir": ""},
    {"code": "en", "endonym": "English",          "hreflang": "en",    "og_locale": "en_US", "rtl": False, "subdir": "en/"},
    {"code": "ja", "endonym": "日本語",           "hreflang": "ja",    "og_locale": "ja_JP", "rtl": False, "subdir": "ja/"},
    {"code": "ko", "endonym": "한국어",           "hreflang": "ko",    "og_locale": "ko_KR", "rtl": False, "subdir": "ko/"},
    {"code": "vi", "endonym": "Tiếng Việt",       "hreflang": "vi",    "og_locale": "vi_VN", "rtl": False, "subdir": "vi/"},
    {"code": "th", "endonym": "ไทย",              "hreflang": "th",    "og_locale": "th_TH", "rtl": False, "subdir": "th/"},
    {"code": "id", "endonym": "Bahasa Indonesia", "hreflang": "id",    "og_locale": "id_ID", "rtl": False, "subdir": "id/"},
    {"code": "ms", "endonym": "Bahasa Melayu",    "hreflang": "ms",    "og_locale": "ms_MY", "rtl": False, "subdir": "ms/"},
    {"code": "hi", "endonym": "हिन्दी",            "hreflang": "hi",    "og_locale": "hi_IN", "rtl": False, "subdir": "hi/"},
    {"code": "bn", "endonym": "বাংলা",             "hreflang": "bn",    "og_locale": "bn_BD", "rtl": False, "subdir": "bn/"},
    {"code": "de", "endonym": "Deutsch",          "hreflang": "de",    "og_locale": "de_DE", "rtl": False, "subdir": "de/"},
    {"code": "fr", "endonym": "Français",         "hreflang": "fr",    "og_locale": "fr_FR", "rtl": False, "subdir": "fr/"},
    {"code": "es", "endonym": "Español",          "hreflang": "es",    "og_locale": "es_ES", "rtl": False, "subdir": "es/"},
    {"code": "pt", "endonym": "Português",        "hreflang": "pt",    "og_locale": "pt_PT", "rtl": False, "subdir": "pt/"},
    {"code": "it", "endonym": "Italiano",         "hreflang": "it",    "og_locale": "it_IT", "rtl": False, "subdir": "it/"},
    {"code": "ru", "endonym": "Русский",          "hreflang": "ru",    "og_locale": "ru_RU", "rtl": False, "subdir": "ru/"},
    {"code": "nl", "endonym": "Nederlands",       "hreflang": "nl",    "og_locale": "nl_NL", "rtl": False, "subdir": "nl/"},
    {"code": "pl", "endonym": "Polski",           "hreflang": "pl",    "og_locale": "pl_PL", "rtl": False, "subdir": "pl/"},
    {"code": "tr", "endonym": "Türkçe",           "hreflang": "tr",    "og_locale": "tr_TR", "rtl": False, "subdir": "tr/"},
    {"code": "cs", "endonym": "Čeština",          "hreflang": "cs",    "og_locale": "cs_CZ", "rtl": False, "subdir": "cs/"},
    {"code": "el", "endonym": "Ελληνικά",         "hreflang": "el",    "og_locale": "el_GR", "rtl": False, "subdir": "el/"},
    {"code": "hu", "endonym": "Magyar",           "hreflang": "hu",    "og_locale": "hu_HU", "rtl": False, "subdir": "hu/"},
    {"code": "ro", "endonym": "Română",           "hreflang": "ro",    "og_locale": "ro_RO", "rtl": False, "subdir": "ro/"},
    {"code": "sv", "endonym": "Svenska",          "hreflang": "sv",    "og_locale": "sv_SE", "rtl": False, "subdir": "sv/"},
    {"code": "uk", "endonym": "Українська",       "hreflang": "uk",    "og_locale": "uk_UA", "rtl": False, "subdir": "uk/"},
    {"code": "fi", "endonym": "Suomi",            "hreflang": "fi",    "og_locale": "fi_FI", "rtl": False, "subdir": "fi/"},
    {"code": "da", "endonym": "Dansk",            "hreflang": "da",    "og_locale": "da_DK", "rtl": False, "subdir": "da/"},
    {"code": "bg", "endonym": "Български",        "hreflang": "bg",    "og_locale": "bg_BG", "rtl": False, "subdir": "bg/"},
    {"code": "no", "endonym": "Norsk",            "hreflang": "no",    "og_locale": "nb_NO", "rtl": False, "subdir": "no/"},
    {"code": "ar", "endonym": "العربية",          "hreflang": "ar",    "og_locale": "ar_AR", "rtl": True,  "subdir": "ar/"},
    {"code": "fa", "endonym": "فارسی",            "hreflang": "fa",    "og_locale": "fa_IR", "rtl": True,  "subdir": "fa/"},
    {"code": "he", "endonym": "עברית",            "hreflang": "he",    "og_locale": "he_IL", "rtl": True,  "subdir": "he/"},
]

_BY_CODE = {l["code"]: l for l in LANGS}


def lang_by_code(code: str):
    """按 code 取语言记录,不存在返回 None。"""
    return _BY_CODE.get(code)


def page_path(name: str, code: str) -> Path:
    """某语言某页的 HTML 路径(不保证存在)。"""
    return ROOT / lang_by_code(code)["subdir"] / f"{name}.html"


def page_exists(name: str, code: str) -> bool:
    return page_path(name, code).exists()


def pages_with_lang(name: str) -> list:
    """该页面已落地的语言记录列表(保持 LANGS 顺序)。"""
    return [l for l in LANGS if page_exists(name, l["code"])]


def page_url(name: str, code: str) -> str:
    """某语言某页的绝对 URL。"""
    return f"{BASE}/{lang_by_code(code)['subdir']}{name}.html"


if __name__ == "__main__":
    print(f"{len(LANGS)} 种语言已注册:")
    for l in LANGS:
        mark = " [rtl]" if l["rtl"] else ""
        landed = sum(1 for n in
                     ("index", "levels", "scenarios", "redlines", "design",
                      "obs", "skill-ppt", "skill-compress", "license")
                     if page_exists(n, l["code"]))
        print(f"  {l['code']}\t{l['endonym']}\t{l['hreflang']}{mark}\t已落地 {landed} 页")
