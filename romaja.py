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

"""{script}: Japanese Kana Romanizer

Usage: {script} [options] [WORD...]

Options:
  -h, --help            show this
  --version             show version
  -s, --system NAME     'ANSI' | 'ISO' | 'HEPBURN' | 'KUNREI2' |
                        'ROAD' | 'RAIL' | 'MOFA' | 'TEST'
  -k, --kunrei          adopt ISO3602:1989 aka Kunrei-shiki
  -K, --kunrei2         adopt Kunrei-shiki with table 2
  --long SYMBOL         subst char for long vowel [default: ~]
                        'NO' for nothing; '+' to double vowel
  --sep SYMBOL          subst char after n before vowels [default: ']
                        'NO' for nothing
  --m4n                 replace n before b/m/p with m
  -X, --no-extend       do not allow non-native pronounciation
  -c --composite        use composite chars
"""


import sys
import os
import re
from unicodedata import lookup


__version__ = "3.1.0.post1"
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
KR = dict((k[v], c + "AIUEO"[v]) for (c, k) in list(KT.items())
                                 for v in range(5))
RECIPE = { # system: (long, sep, m4n, extend)
    "ANSI":    dict(long="~", sep="'", m4n=False, extend=True),
    "HEPBURN": dict(long="+", sep="-", m4n=True, extend=True),
    "KUNREI2": dict(long="^", sep="'", m4n=False, extend=False),
    "ROAD":    dict(long="", sep="-", m4n=False, extend=True),
    "RAIL":    dict(long="~", sep="-", m4n=True, extend=True),
    "MOFA":    dict(long="", sep="", m4n=True, extend=False),
    "ISO":     dict(long="^", sep="'", m4n=False, extend=False),
    }
ACCENTNAME = {
    "~":    "MACRON",
    "^":    "CIRCUMFLEX",
    "'":    "ACUTE",
    "`":    "GRAVE",
    ":":    "DIAERESIS",
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


def makecomposite(s, longmark):
    accname = ACCENTNAME[longmark]
    charname = "LATIN CAPITAL LETTER {} WITH {}"
    for c in "AIUEO":
        if c not in s: continue
        s = s.replace(c + longmark, lookup(charname.format(c, accname)))
    return s


def iso3602(s):
    """Convert katakana to its roman repr in ISO style (aka Kunrei-shiki).

    s           (unicode) source text

    Example:
    >>> assert iso3602(u"カンダ") == u"KANDA"
    >>> assert iso3602(u"カンナミ") == u"KANNAMI"
    >>> assert iso3602(u"シンジュク") == u"SINZYUKU"
    >>> assert iso3602(u"チェック") == u"TIEKKU"
    >>> assert iso3602(u"シンバシ") == u"SINBASI"
    >>> assert iso3602(u"チェンマイ") == u"TIENMAI"
    >>> assert iso3602(u"サンアイ") == u"SAN'AI"
    >>> assert iso3602(u"コンヤク") == u"KON'YAKU"
    >>> assert iso3602(u"カード") == u"KA^DO"
    >>> assert iso3602(u"ジェラシー") == u"ZIERASI^"
    >>> assert iso3602(u"マッチャ") == u"MATTYA"
    """
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


def roma(s, system="ANSI", composite=False):
    """Convert kana to its roman repr in various styles.

    s           (unicode) source text
    system      (str) 'ANSI' | 'ISO' | 'HEPBURN' | 'KUNREI2' |
                      'ROAD' | 'RAIL' | 'MOFA'  [default: ANSI]
                (dict) conversion specification
    composite   (bool) use chars with composite glyphs

    Keys and values of conversion specification are as follows::
        long    (str) '^' | 'CIRCUMFLEX' | '~' | 'MACRON' |
                      '+' | 'H' | ''; '+'=double vowel [default: ^]
        sep     (str) "'" | '-' | '' [default: ']
        m4n     (bool) use m instead of n before b/m/p [default: False]
        extend  (bool) allow non-native pronounciation [default: True]

    Each system gives the following conversion specification:
                long    sep         m4n     extend
        ------------------------------------------
        ANSI    ~       '           False   True
        ISO     ~       '           False   False
        HEPBURN +       -           True    True
        KUNREI2 ~       '           False   False
        ROAD    (none)  -           False   True
        RAIL    ~       -           True    True
        MOFA    (none)  (none)      True    False

    Test:
    >>> assert roma("かんだ", "ANSI") == "KANDA"
    >>> assert roma("かんなみ", "ANSI") == "KANNAMI"
    >>> assert roma("しんじゅく", "ANSI") == "SHINJUKU"
    >>> assert roma("チェック", "ANSI") == "CHEKKU"
    >>> assert roma("しんばし", "ANSI") == "SHINBASHI"
    >>> assert roma("チェンマイ", "ANSI") == "CHENMAI"
    >>> assert roma("さんあい", "ANSI") == "SAN'AI"
    >>> assert roma("こんやく", "ANSI") == "KON'YAKU"
    >>> assert roma("カード", "ANSI") == "KA~DO"
    >>> assert roma("ジェラシー", "ANSI") == "JERASHI~"
    >>> assert roma("まっちゃ", "ANSI") == "MATCHA"
    >>> assert roma("かんだ", "ISO") == "KANDA"
    >>> assert roma("かんなみ", "ISO") == "KANNAMI"
    >>> assert roma("しんじゅく", "ISO") == "SINZYUKU"
    >>> assert roma("チェック", "ISO") == "TIEKKU"
    >>> assert roma("しんばし", "ISO") == "SINBASI"
    >>> assert roma("チェンマイ", "ISO") == "TIENMAI"
    >>> assert roma("さんあい", "ISO") == "SAN'AI"
    >>> assert roma("こんやく", "ISO") == "KON'YAKU"
    >>> assert roma("カード", "ISO") == "KA^DO"
    >>> assert roma("ジェラシー", "ISO") == "ZIERASI^"
    >>> assert roma("まっちゃ", "ISO") == "MATTYA"
    >>> assert roma("かんだ", "HEPBURN") == "KANDA"
    >>> assert roma("かんなみ", "HEPBURN") == "KANNAMI"
    >>> assert roma("しんじゅく", "HEPBURN") == "SHINJUKU"
    >>> assert roma("チェック", "HEPBURN") == "CHEKKU"
    >>> assert roma("しんばし", "HEPBURN") == "SHIMBASHI"
    >>> assert roma("チェンマイ", "HEPBURN") == "CHEMMAI"
    >>> assert roma("さんあい", "HEPBURN") == "SAN-AI"
    >>> assert roma("こんやく", "HEPBURN") == "KON-YAKU"
    >>> assert roma("カード", "HEPBURN") == "KAADO"
    >>> assert roma("ジェラシー", "HEPBURN") == "JERASHII"
    >>> assert roma("まっちゃ", "HEPBURN") == "MATCHA"
    >>> assert roma("かんだ", "KUNREI2") == "KANDA"
    >>> assert roma("かんなみ", "KUNREI2") == "KANNAMI"
    >>> assert roma("しんじゅく", "KUNREI2") == "SHINJUKU"
    >>> assert roma("チェック", "KUNREI2") == "CHIEKKU"
    >>> assert roma("しんばし", "KUNREI2") == "SHINBASHI"
    >>> assert roma("チェンマイ", "KUNREI2") == "CHIENMAI"
    >>> assert roma("さんあい", "KUNREI2") == "SAN'AI"
    >>> assert roma("こんやく", "KUNREI2") == "KON'YAKU"
    >>> assert roma("カード", "KUNREI2") == "KA^DO"
    >>> assert roma("ジェラシー", "KUNREI2") == "JIERASHI^"
    >>> assert roma("まっちゃ", "KUNREI2") == "MACCHA"
    >>> assert roma("しゃししゅしょつ", "KUNREI2") == "SHASHISHUSHOTSU"
    >>> assert roma("ちゃちちゅちょ", "KUNREI2") == "CHACHICHUCHO"
    >>> assert roma("ふじゃじじゅじょ", "KUNREI2") == "FUJAJIJUJO"
    >>> assert roma("ぢづぢゃぢゅぢょ", "KUNREI2") == "DIDUDYADYUDYO"
    >>> assert roma("くゎぐゎを", "KUNREI2") == "KWAGWAWO"
    >>> assert roma("かんだ", "ROAD") == "KANDA"
    >>> assert roma("かんなみ", "ROAD") == "KANNAMI"
    >>> assert roma("しんじゅく", "ROAD") == "SHINJUKU"
    >>> assert roma("チェック", "ROAD") == "CHEKKU"
    >>> assert roma("しんばし", "ROAD") == "SHINBASHI"
    >>> assert roma("チェンマイ", "ROAD") == "CHENMAI"
    >>> assert roma("さんあい", "ROAD") == "SAN-AI"
    >>> assert roma("こんやく", "ROAD") == "KON-YAKU"
    >>> assert roma("カード", "ROAD") == "KADO"
    >>> assert roma("ジェラシー", "ROAD") == "JERASHII"
    >>> assert roma("まっちゃ", "ROAD") == "MATCHA"
    >>> assert roma("かんだ", "RAIL") == "KANDA"
    >>> assert roma("かんなみ", "RAIL") == "KANNAMI"
    >>> assert roma("しんじゅく", "RAIL") == "SHINJUKU"
    >>> assert roma("チェック", "RAIL") == "CHEKKU"
    >>> assert roma("しんばし", "RAIL") == "SHIMBASHI"
    >>> assert roma("チェンマイ", "RAIL") == "CHEMMAI"
    >>> assert roma("さんあい", "RAIL") == "SAN-AI"
    >>> assert roma("こんやく", "RAIL") == "KON-YAKU"
    >>> assert roma("カード", "RAIL") == "KA~DO"
    >>> assert roma("ジェラシー", "RAIL") == "JERASHI~"
    >>> assert roma("まっちゃ", "RAIL") == "MATCHA"
    >>> assert roma("かんだ", "MOFA") == "KANDA"
    >>> assert roma("かんなみ", "MOFA") == "KANNAMI"
    >>> assert roma("しんじゅく", "MOFA") == "SHINJUKU"
    >>> assert roma("チェック", "MOFA") == "CHIEKKU"
    >>> assert roma("しんばし", "MOFA") == "SHIMBASHI"
    >>> assert roma("チェンマイ", "MOFA") == "CHIEMMAI"
    >>> assert roma("さんあい", "MOFA") == "SANAI"
    >>> assert roma("こんやく", "MOFA") == "KONYAKU"
    >>> assert roma("カード", "MOFA") == "KADO"
    >>> assert roma("ジェラシー", "MOFA") == "JIERASHII"
    >>> assert roma("まっちゃ", "MOFA") == "MATCHA"
    """
    s = h2k(s)
    if isinstance(system, str):
        system = (system or "ANSI").upper()
        if system == "ISO":
            s = iso3602(s)
            if composite: s = makecomposite(s, "^")
            return s
        if system == "KUNREI2":
            s = _translate(s,
                    "ヂ ヅ ヂャ ヂュ ヂョ ヲ",
                    "DI DU DYA DYU DYO WO")
        system = RECIPE[system]
    s = _translate(s, "クヮ グヮ", "KWA GWA")
    if system["extend"]:
        s = _translate(s,
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
    lng = system["long"].upper()
    if lng == "MACRON": lng = "~"
    elif lng == "CIRCUMFLEX": lng = "^"
    if lng == "+":
        s = _translate(s, "A^ I^ U^ E^ O^", "AA II UU EE OO")
    elif lng == "H":
        s = _translate(s, "A^ I^ U^ E^ O^", "AH II U E OH")
    elif not lng:
        s = _translate(s, "A^ I^ U^ E^ O^", "A II U E O")
    elif lng == "~":
        s = s.replace("^", "~")
    elif lng != "^":
        raise ValueError("invalid long vowel symbol '{}'".format(lng))
    if composite and lng:
        s = makecomposite(s, lng)
    if lng == "^":
        s = s.replace("TCH", "CCH")
    if system["sep"] != "'":
        s = s.replace("'", system["sep"])
    return s


# COMPATIBILITY
romazi = iso3602
romaji = roma


def main():

    import docopt

    args = docopt.docopt(__doc__.format(script=os.path.basename(__file__)),
                        version=__version__)
    if args["--kunrei"]: system = "ISO"
    elif args["--kunrei2"]: system = "KUNREI2"
    elif args["--system"]:
        system = args["--system"].upper()
        if system == "TEST":
            import doctest
            doctest.testmod()
            return
    else:
        system = dict(
                long=args["--long"] or "~",
                sep=args["--sep"] or "'",
                m4n=args["--m4n"] or False,
                extend=(not args["--no-extend"]),
                )
        if system["long"].upper() == "NO": system["long"] = ""
        if system["sep"].upper() == "NO": system["sep"] = ""
    c = args["--composite"]
    if args["WORD"]:
        print(" ".join(roma(word, system, c) for word in args["WORD"]))
    else:
        for line in sys.stdin:
            print(" ".join(roma(word, system, c) for word in line.split()))


if __name__ == "__main__":
    sys.exit(main())
