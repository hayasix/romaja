#!/usr/bin/env python3
# vim: set fileencoding=utf-8 fileformat=unix :

# Copyright (C) 2013 HAYASI Hideki <linxs@linxs.org>  All rights reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL). A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.

"""{script}: Japanese Kana to Romaji converter

Usage: {script} [options] [WORD...]

Options:
  -h, --help            show this
  --version             show version
  -s, --system NAME     'ANSI' | 'ISO' | 'HEPBURN' | 'KUNREI2' |
                        'ROAD' | 'RAIL' | 'MOFA' | 'TEST'
  -k, --kunrei          adopt ISO3602 aka Kunrei-shiki
  --macron SYMBOL       subst char for long vowel [default: ~]
                        'NO' for nothing; '+' to double vowel
  --apostrophe SYMBOL   subst char after n before vowels [default: ']
                        'NO' for nothing
  --m4n                 replace n before b/m/p with m
  -X, --no-extend       do not allow non-native pronounciation
"""


import sys
import os
import re


__version__ = "3.0.0a2"
__author__ = "HAYASI Hideki"
__copyright__ = "Copyright (C) 2013 HAYASI Hideki <linxs@linxs.org>"
__license__ = "ZPL 2.1"
__email__ = "linxs@linxs.org"
__status__ = "Production"

__all__ = ("roma", "romazi", "romaji")

KT = dict(
        X="アイウエオ",
        K="カキクケコ",
        G="ガギグゲゴ",
        S="サシスセソ",
        Z="ザジズゼゾ",
        T="タチツテト",
        D="ダヂヅデド",
        N="ナニヌネノ",
        H="ハヒフヘホ",
        B="バビブベボ",
        P="パピプペポ",
        M="マミムメモ",
        Y="ヤ〓ユ〓ヨ",
        R="ラリルレロ",
        W="ワヰ〓ヱヲ",
        )
KR = dict((k[v], c + "AIUEO"[v]) for (c, k) in list(KT.items()) for v in range(5))
RECIPE = { # system: (macron, apostrophe, m4n, extend)
    "ANSI":    dict(macron="~", apostrophe="'", m4n=False, extend=True),
    "HEPBURN": dict(macron="+", apostrophe="-", m4n=True, extend=True),
    "KUNREI2": dict(macron="^", apostrophe="'", m4n=False, extend=True),
    "ROAD":    dict(macron="", apostrophe="-", m4n=False, extend=True),
    "RAIL":    dict(macron="~", apostrophe="-", m4n=True, extend=True),
    "MOFA":    dict(macron="", apostrophe="", m4n=True, extend=False),
    "ISO":     dict(macron="^", apostrophe="'", m4n=False, extend=False),
    }


def _translate(s, in_, out):
    for (a, b) in zip(in_.split(), out.split()):
        s = s.replace(a, b)
    return s


def h2k(s):
    ss = list(re.sub(r"[うウ]゛", "ヴ", s))
    for p, c in enumerate(ss):
        cc = ord(c)
        if 0x3041 <= cc <= 0x3096:
            ss[p] = chr(cc + 0x60)
    return "".join(ss)


def iso3602(s):
    """Convert kana to its roman repr in ISO style (aka Kunrei-shiki).

    s           (unicode) source text

    Example:
    >>> assert iso3602(u"かんだ") == u"KANDA"
    >>> assert iso3602(u"かんなみ") == u"KANNAMI"
    >>> assert iso3602(u"しんじゅく") == u"SINZYUKU"
    >>> assert iso3602(u"チェック") == u"TIEKKU"
    >>> assert iso3602(u"しんばし") == u"SINBASI"
    >>> assert iso3602(u"チェンマイ") == u"TIENMAI"
    >>> assert iso3602(u"さんあい") == u"SAN'AI"
    >>> assert iso3602(u"こんやく") == u"KON'YAKU"
    >>> assert iso3602(u"カード") == u"KA^DO"
    >>> assert iso3602(u"ジェラシー") == u"ZIERASI^"
    >>> assert iso3602(u"まっちゃ") == u"MATTYA"
    """
    s = h2k(s)
    s = _translate(s, "ヰ ヱ ヲ ヂ ヅ ウ゛ ヴ", "イ エ オ ジ ズ ヴ ブ")
    s = _translate(s, "ァ ィ ゥ ェ ォ", "XA XI XU XE XO")
    s = _translate(s, "ン", "N'")
    ss = list(s)
    bc = list(KR.keys())
    sokuon = False
    for p, c in enumerate(ss):
        if c in bc:
            ss[p] = KR[c]
            if sokuon:
                ss[p] = ss[p][0] + ss[p]
            sokuon = False
        elif c in "ャュョ":
            pm = p - 1
            ss[pm] = ss[pm][:-1] + "Y" + "AUO"["ャュョ".index(c)]
            ss[p] = ""
        elif c == "ッ":
            sokuon = True
            ss[p] = ""
        elif c == "ー":
            ss[p] = "^"
    s = "".join(ss)
    s = s.replace("X", "")
    s = re.sub(r"N'([^AIUEOY])", r"N\1", s)
    s = s.replace("OUU", "O^U")
    for c in "AIUEO":
        s = re.sub(c + "{2,}", c + "^", s)
    s = s.replace("OU", "O^")
    s = s.strip("'")
    return s


def roma(s, system="ANSI"):
    """Convert kana to its roman repr in various styles.

    s           (unicode) source text
    system      (str) 'ANSI' | 'ISO' | 'HEPBURN' | 'KUNREI2' |
                      'ROAD' | 'RAIL' | 'MOFA'  [default: ANSI]
                (dict) conversion specification

    Keys and values of conversion specification are as follows::
        macron      (str) '^' | '~' | '+' | 'H' | '';
                          '+'=double vowel [default: ^]
        apostrophe  (str) "'" | '-' | '' [default: ']
        m4n         (bool) use m instead of n before b/m/p [default: False]
        extend      (bool) allow non-native pronounciation [default: True]

    Each system gives the following conversion specification:
                macron  apostrophe  m4n     extend
        ------------------------------------------
        ANSI    ~       '           False   True
        ISO     ~       '           False   False
        HEPBURN +       -           True    True
        KUNREI2 ~       '           False   True
        ROAD    (none)  -           False   True
        RAIL    ~       -           True    True
        MOFA    (none)  (none)      True    False

    Test:
    >>> assert roma(u"かんだ", "ANSI") == u"KANDA"
    >>> assert roma(u"かんなみ", "ANSI") == u"KANNAMI"
    >>> assert roma(u"しんじゅく", "ANSI") == u"SHINJUKU"
    >>> assert roma(u"チェック", "ANSI") == u"CHEKKU"
    >>> assert roma(u"しんばし", "ANSI") == u"SHINBASHI"
    >>> assert roma(u"チェンマイ", "ANSI") == u"CHENMAI"
    >>> assert roma(u"さんあい", "ANSI") == u"SAN'AI"
    >>> assert roma(u"こんやく", "ANSI") == u"KON'YAKU"
    >>> assert roma(u"カード", "ANSI") == u"KA~DO"
    >>> assert roma(u"ジェラシー", "ANSI") == u"JERASHI~"
    >>> assert roma(u"まっちゃ", "ANSI") == u"MATCHA"
    >>> assert roma(u"かんだ", "ISO") == u"KANDA"
    >>> assert roma(u"かんなみ", "ISO") == u"KANNAMI"
    >>> assert roma(u"しんじゅく", "ISO") == u"SINZYUKU"
    >>> assert roma(u"チェック", "ISO") == u"TIEKKU"
    >>> assert roma(u"しんばし", "ISO") == u"SINBASI"
    >>> assert roma(u"チェンマイ", "ISO") == u"TIENMAI"
    >>> assert roma(u"さんあい", "ISO") == u"SAN'AI"
    >>> assert roma(u"こんやく", "ISO") == u"KON'YAKU"
    >>> assert roma(u"カード", "ISO") == u"KA^DO"
    >>> assert roma(u"ジェラシー", "ISO") == u"ZIERASI^"
    >>> assert roma(u"まっちゃ", "ISO") == u"MATTYA"
    >>> assert roma(u"かんだ", "HEPBURN") == u"KANDA"
    >>> assert roma(u"かんなみ", "HEPBURN") == u"KANNAMI"
    >>> assert roma(u"しんじゅく", "HEPBURN") == u"SHINJUKU"
    >>> assert roma(u"チェック", "HEPBURN") == u"CHEKKU"
    >>> assert roma(u"しんばし", "HEPBURN") == u"SHIMBASHI"
    >>> assert roma(u"チェンマイ", "HEPBURN") == u"CHEMMAI"
    >>> assert roma(u"さんあい", "HEPBURN") == u"SAN-AI"
    >>> assert roma(u"こんやく", "HEPBURN") == u"KON-YAKU"
    >>> assert roma(u"カード", "HEPBURN") == u"KAADO"
    >>> assert roma(u"ジェラシー", "HEPBURN") == u"JERASHII"
    >>> assert roma(u"まっちゃ", "HEPBURN") == u"MATCHA"
    >>> assert roma(u"かんだ", "KUNREI2") == u"KANDA"
    >>> assert roma(u"かんなみ", "KUNREI2") == u"KANNAMI"
    >>> assert roma(u"しんじゅく", "KUNREI2") == u"SHINJUKU"
    >>> assert roma(u"チェック", "KUNREI2") == u"CHEKKU"
    >>> assert roma(u"しんばし", "KUNREI2") == u"SHINBASHI"
    >>> assert roma(u"チェンマイ", "KUNREI2") == u"CHENMAI"
    >>> assert roma(u"さんあい", "KUNREI2") == u"SAN'AI"
    >>> assert roma(u"こんやく", "KUNREI2") == u"KON'YAKU"
    >>> assert roma(u"カード", "KUNREI2") == u"KA^DO"
    >>> assert roma(u"ジェラシー", "KUNREI2") == u"JERASHI^"
    >>> assert roma(u"まっちゃ", "KUNREI2") == u"MACCHA"
    >>> assert roma(u"かんだ", "ROAD") == u"KANDA"
    >>> assert roma(u"かんなみ", "ROAD") == u"KANNAMI"
    >>> assert roma(u"しんじゅく", "ROAD") == u"SHINJUKU"
    >>> assert roma(u"チェック", "ROAD") == u"CHEKKU"
    >>> assert roma(u"しんばし", "ROAD") == u"SHINBASHI"
    >>> assert roma(u"チェンマイ", "ROAD") == u"CHENMAI"
    >>> assert roma(u"さんあい", "ROAD") == u"SAN-AI"
    >>> assert roma(u"こんやく", "ROAD") == u"KON-YAKU"
    >>> assert roma(u"カード", "ROAD") == u"KADO"
    >>> assert roma(u"ジェラシー", "ROAD") == u"JERASHII"
    >>> assert roma(u"まっちゃ", "ROAD") == u"MATCHA"
    >>> assert roma(u"かんだ", "RAIL") == u"KANDA"
    >>> assert roma(u"かんなみ", "RAIL") == u"KANNAMI"
    >>> assert roma(u"しんじゅく", "RAIL") == u"SHINJUKU"
    >>> assert roma(u"チェック", "RAIL") == u"CHEKKU"
    >>> assert roma(u"しんばし", "RAIL") == u"SHIMBASHI"
    >>> assert roma(u"チェンマイ", "RAIL") == u"CHEMMAI"
    >>> assert roma(u"さんあい", "RAIL") == u"SAN-AI"
    >>> assert roma(u"こんやく", "RAIL") == u"KON-YAKU"
    >>> assert roma(u"カード", "RAIL") == u"KA~DO"
    >>> assert roma(u"ジェラシー", "RAIL") == u"JERASHI~"
    >>> assert roma(u"まっちゃ", "RAIL") == u"MATCHA"
    >>> assert roma(u"かんだ", "MOFA") == u"KANDA"
    >>> assert roma(u"かんなみ", "MOFA") == u"KANNAMI"
    >>> assert roma(u"しんじゅく", "MOFA") == u"SHINJUKU"
    >>> assert roma(u"チェック", "MOFA") == u"CHIEKKU"
    >>> assert roma(u"しんばし", "MOFA") == u"SHIMBASHI"
    >>> assert roma(u"チェンマイ", "MOFA") == u"CHIEMMAI"
    >>> assert roma(u"さんあい", "MOFA") == u"SANAI"
    >>> assert roma(u"こんやく", "MOFA") == u"KONYAKU"
    >>> assert roma(u"カード", "MOFA") == u"KADO"
    >>> assert roma(u"ジェラシー", "MOFA") == u"JIERASHII"
    >>> assert roma(u"まっちゃ", "MOFA") == u"MATCHA"
    """
    if isinstance(system, str):
        system = (system or "ANSI").upper()
        if system == "ISO": return iso3602(s)
        system = RECIPE[system]
    s = h2k(s)
    if system["extend"]:
        s = _translate(h2k(s),
                ("イェ ウィ ウェ ウォ ヴァ ヴィ ヴェ ヴォ ヴュ ヴ "
                 "スィ シェ ズィ ジェ ティ トゥ チェ ディ ドゥ ヂェ "
                 "ツァ ツィ ツェ ツォ ファ フィ フェ フォ"),
                ("YE WI WE WO VA VI VE VO VYU VU "
                 "ShI ShE ZhI JE ThI ThU CHE DI DU JE "
                 "TSA TsI TSE TSO FA FI FE FO"))
    s = iso3602(s)
    if system["m4n"]:
        s = re.sub(r"N([BMP])", r"M\1", s)
    s = _translate(s, "HU SI ZI TI TU SY ZY TY Sh Zh Th sI",
                      "FU SHI JI CHI TSU SH J CH S Z T SI")
    if system["macron"] == "+":
        s = _translate(s, "A^ I^ U^ E^ O^", "AA II UU EE OO")
    elif system["macron"].upper() == "H":
        s = _translate(s, "A^ I^ U^ E^ O^", "AH II U E OH")
    elif not system["macron"]:
        s = _translate(s, "A^ I^ U^ E^ O^", "A II U E O")
    elif system["macron"] != "^":
        s = s.replace("^", system["macron"])
    if system["macron"] == "^":
        s = s.replace("TCH", "CCH")
    if system["apostrophe"] != "'":
        s = s.replace("'", system["apostrophe"])
    return s


# COMPATIBILITY
romazi = iso3602
romaji = lambda s: roma(s)


def main():

    import docopt

    args = docopt.docopt(__doc__.format(script=os.path.basename(__file__)),
                        version=__version__)
    if args["--kunrei"]:
        system = "ISO"
    elif args["--system"]:
        system = args["--system"].upper()
        if system == "TEST":
            import doctest
            doctest.testmod()
            return
    else:
        system = dict(
                macron=args["--macron"] or "~",
                apostrophe=args["--apostrophe"] or "'",
                m4n=args["--m4n"] or False,
                extend=(not args["--no-extend"]),
                )
        if system["macron"].upper() == "NO": system["macron"] = ""
        if system["apostrophe"].upper() == "NO": system["apostrophe"] = ""
    if args["WORD"]:
        print(" ".join(roma(word, system) for word in args["WORD"]))
    else:
        for line in sys.stdin:
            print(" ".join(roma(word, system) for word in line.split()))


if __name__ == "__main__":
    sys.exit(main())
