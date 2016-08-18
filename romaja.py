#!/usr/bin/env python2.7
# vim: set fileencoding=utf-8 fileformat=unix :

"""romaja.py: Japanese Kana to Romaji converter

Copyright (C) 2013 HAYASI Hideki <linxs@linxs.org>  All rights reserved.

This software is subject to the provisions of the Zope Public License,
Version 2.1 (ZPL). A copy of the ZPL should accompany this distribution.
THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
FOR A PARTICULAR PURPOSE.
"""

from __future__ import print_function

import sys
import os
import re


if sys.platform.startswith("win"):
    ################## py2exe compliant ##################
    import imp
    if hasattr(sys, "setdefaultencoding"):
        sys.setdefaultencoding("cp932")
    def frozen():
        return (hasattr(sys, "frozen") or
                hasattr(sys, "importers") or
                imp.is_frozen("__main__"))
    def modulepath():
        return os.path.abspath(os.path.dirname(
            sys.executable if frozen() else sys.argv[0]))
    ################## py2exe compliant ##################


__version__ = "1.4.0"
__author__ = "HAYASI Hideki"
__copyright__ = "Copyright (C) 2013 HAYASI Hideki <linxs@linxs.org>"
__license__ = "ZPL 2.1"
__email__ = "linxs@linxs.org"
__status__ = "Production"

__all__ = ("romazi", "romaji")

KT = dict(
        X=u"アイウエオ",
        K=u"カキクケコ",
        G=u"ガギグゲゴ",
        S=u"サシスセソ",
        Z=u"ザジズゼゾ",
        T=u"タチツテト",
        D=u"ダヂヅデド",
        N=u"ナニヌネノ",
        H=u"ハヒフヘホ",
        B=u"バビブベボ",
        P=u"パピプペポ",
        M=u"マミムメモ",
        Y=u"ヤ〓ユ〓ヨ",
        R=u"ラリルレロ",
        W=u"ワヰ〓ヱヲ",
        )
KR = dict((k[v], c + u"AIUEO"[v]) for (c, k) in KT.items() for v in range(5))
RECIPE = { # system: (macron, apostrophe, m4n, extend)
    u"HEPBURN": (u"+", u"-", True, True),
    u"ANSI":    (u"~", u"'", False, True),
    u"KUNREI2": (u"^", u"'", False, True),
    u"ROAD":    (u"", u"-", False, True),
    u"RAIL":    (u"~", u"-", True, True),
    u"MOFA":    (u"", u"", True, False),
    u"":        (u"^", u"'", False, False),
    }


def _translate(s, in_, out):
    for (a, b) in zip(in_.split(), out.split()):
        s = s.replace(a, b)
    return s


def h2k(s):
    ss = list(re.sub(ur"[うウ]゛", u"ヴ", s))
    for p, c in enumerate(ss):
        cc = ord(c)
        if 0x3041 <= cc <= 0x3096:
            ss[p] = unichr(cc + 0x60)
    return u"".join(ss)


def romazi(s):
    u"""Convert kana to its roman representation in ISO-style.

    s           (unicode) source text

    Example:
    >>> assert romaji(u"かんだ", "iso") == u"KANDA"
    >>> assert romaji(u"かんなみ", "iso") == u"KANNAMI"
    >>> assert romaji(u"しんじゅく", "iso") == u"SINZYUKU"
    >>> assert romaji(u"チェック", "iso") == u"TIEKKU"
    >>> assert romaji(u"しんばし", "iso") == u"SINBASI"
    >>> assert romaji(u"チェンマイ", "iso") == u"TIENMAI"
    >>> assert romaji(u"さんあい", "iso") == u"SAN'AI"
    >>> assert romaji(u"こんやく", "iso") == u"KON'YAKU"
    >>> assert romaji(u"カード", "iso") == u"KA^DO"
    >>> assert romaji(u"ジェラシー", "iso") == u"ZIERASI^"
    """
    s = h2k(s)
    s = _translate(s, u"ヰ ヱ ヲ ヂ ヅ ウ゛ ヴ", u"イ エ オ ジ ズ ヴ ブ")
    s = _translate(s, u"ァ ィ ゥ ェ ォ", u"XA XI XU XE XO")
    s = _translate(s, u"ン", u"N'")
    ss = list(s)
    bc = KR.keys()
    sokuon = False
    for p, c in enumerate(ss):
        if c in bc:
            ss[p] = KR[c]
            if sokuon:
                ss[p] = ss[p][0] + ss[p]
            sokuon = False
        elif c in u"ャュョ":
            pm = p - 1
            ss[pm] = ss[pm][:-1] + u"Y" + u"AUO"[u"ャュョ".index(c)]
            ss[p] = u""
        elif c == u"ッ":
            sokuon = True
            ss[p] = u""
        elif c == u"ー":
            ss[p] = u"^"
    s = u"".join(ss)
    s = s.replace(u"X", u"")
    s = re.sub(ur"N'([^AIUEOY])", ur"N\1", s)
    s = s.replace(u"OUU", u"O^U")
    for c in u"AIUEO":
        s = re.sub(c + u"{2,}", c + u"^", s)
    s = s.replace(u"OU", u"O^")
    s = s.strip(u"'")
    return s


def romaji(s, system="ansi",
        macron=None, apostrophe=None, m4n=None, extend=None):
    u"""Convert kana to its roman representation.

    s           (unicode) source text
    system      (str) 'ANSI' | 'ISO' | 'HEPBURN' | 'KUNREI2' |
                      'ROAD' | 'RAIL' | 'MOFA'
    macron      (str) '^' | '~' | '+' | ''; '+'=double vowel
    apostrophe  (str) "'" | '-' | ''
    m4n         (bool) use m instead of n before b/m/p
    extend      (bool) allow non-native pronounciation

    Example:
    >>> assert romaji(u"かんだ", "iso") == u"KANDA"
    >>> assert romaji(u"かんなみ", "iso") == u"KANNAMI"
    >>> assert romaji(u"しんじゅく", "iso") == u"SINZYUKU"
    >>> assert romaji(u"チェック", "iso") == u"TIEKKU"
    >>> assert romaji(u"しんばし", "iso") == u"SINBASI"
    >>> assert romaji(u"チェンマイ", "iso") == u"TIENMAI"
    >>> assert romaji(u"さんあい", "iso") == u"SAN'AI"
    >>> assert romaji(u"こんやく", "iso") == u"KON'YAKU"
    >>> assert romaji(u"カード", "iso") == u"KA^DO"
    >>> assert romaji(u"ジェラシー", "iso") == u"ZIERASI^"
    >>> assert romaji(u"かんだ", "hepburn") == u"KANDA"
    >>> assert romaji(u"かんなみ", "hepburn") == u"KANNAMI"
    >>> assert romaji(u"しんじゅく", "hepburn") == u"SHINJUKU"
    >>> assert romaji(u"チェック", "hepburn") == u"CHEKKU"
    >>> assert romaji(u"しんばし", "hepburn") == u"SHIMBASHI"
    >>> assert romaji(u"チェンマイ", "hepburn") == u"CHEMMAI"
    >>> assert romaji(u"さんあい", "hepburn") == u"SAN-AI"
    >>> assert romaji(u"こんやく", "hepburn") == u"KON-YAKU"
    >>> assert romaji(u"カード", "hepburn") == u"KAADO"
    >>> assert romaji(u"ジェラシー", "hepburn") == u"JERASHII"
    >>> assert romaji(u"かんだ", "ansi") == u"KANDA"
    >>> assert romaji(u"かんなみ", "ansi") == u"KANNAMI"
    >>> assert romaji(u"しんじゅく", "ansi") == u"SHINJUKU"
    >>> assert romaji(u"チェック", "ansi") == u"CHEKKU"
    >>> assert romaji(u"しんばし", "ansi") == u"SHINBASHI"
    >>> assert romaji(u"チェンマイ", "ansi") == u"CHENMAI"
    >>> assert romaji(u"さんあい", "ansi") == u"SAN'AI"
    >>> assert romaji(u"こんやく", "ansi") == u"KON'YAKU"
    >>> assert romaji(u"カード", "ansi") == u"KA~DO"
    >>> assert romaji(u"ジェラシー", "ansi") == u"JERASHI~"
    >>> assert romaji(u"かんだ", "kunrei2") == u"KANDA"
    >>> assert romaji(u"かんなみ", "kunrei2") == u"KANNAMI"
    >>> assert romaji(u"しんじゅく", "kunrei2") == u"SHINJUKU"
    >>> assert romaji(u"チェック", "kunrei2") == u"CHEKKU"
    >>> assert romaji(u"しんばし", "kunrei2") == u"SHINBASHI"
    >>> assert romaji(u"チェンマイ", "kunrei2") == u"CHENMAI"
    >>> assert romaji(u"さんあい", "kunrei2") == u"SAN'AI"
    >>> assert romaji(u"こんやく", "kunrei2") == u"KON'YAKU"
    >>> assert romaji(u"カード", "kunrei2") == u"KA^DO"
    >>> assert romaji(u"ジェラシー", "kunrei2") == u"JERASHI^"
    >>> assert romaji(u"かんだ", "road") == u"KANDA"
    >>> assert romaji(u"かんなみ", "road") == u"KANNAMI"
    >>> assert romaji(u"しんじゅく", "road") == u"SHINJUKU"
    >>> assert romaji(u"チェック", "road") == u"CHEKKU"
    >>> assert romaji(u"しんばし", "road") == u"SHINBASHI"
    >>> assert romaji(u"チェンマイ", "road") == u"CHENMAI"
    >>> assert romaji(u"さんあい", "road") == u"SAN-AI"
    >>> assert romaji(u"こんやく", "road") == u"KON-YAKU"
    >>> assert romaji(u"カード", "road") == u"KADO"
    >>> assert romaji(u"ジェラシー", "road") == u"JERASHII"
    >>> assert romaji(u"かんだ", "rail") == u"KANDA"
    >>> assert romaji(u"かんなみ", "rail") == u"KANNAMI"
    >>> assert romaji(u"しんじゅく", "rail") == u"SHINJUKU"
    >>> assert romaji(u"チェック", "rail") == u"CHEKKU"
    >>> assert romaji(u"しんばし", "rail") == u"SHIMBASHI"
    """
    system = system.upper()
    if system == "ISO": return romazi(s)
    opts = RECIPE[system]
    macron = macron or opts[0]
    apostrophe = apostrophe or opts[1]
    m4n = m4n or opts[2]
    extend = extend or opts[3]
    s = h2k(s)
    if extend:
        s = _translate(h2k(s),
                (u"イェ ウィ ウェ ウォ ヴァ ヴィ ヴェ ヴォ ヴュ ヴ "
                 u"スィ シェ ズィ ジェ ティ トゥ チェ ディ ドゥ ヂェ "
                 u"ツァ ツィ ツェ ツォ ファ フィ フェ フォ"),
                (u"YE WI WE WO VA VI VE VO VYU VU "
                 u"ShI ShE ZhI JE ThI ThU CHE DI DU JE "
                 u"TSA TsI TSE TSO FA FI FE FO"))
    s = romazi(s)
    if m4n:
        s = re.sub(ur"N([BMP])", ur"M\1", s)
    s = _translate(s, u"HU SI ZI TI TU SY ZY TY Sh Zh Th sI",
                      u"FU SHI JI CHI TSU SH J CH S Z T SI")
    if macron == u"+":
        s = _translate(s, u"A^ I^ U^ E^ O^", u"AA II UU EE OO")
    elif macron.upper() == u"H":
        s = _translate(s, u"A^ I^ U^ E^ O^", u"AH II U E OH")
    elif not macron:
        s = _translate(s, u"A^ I^ U^ E^ O^", u"A II U E O")
    elif macron != "^":
        s = s.replace(u"^", macron)
    if macron == "^":
        s = s.replace(u"TCH", u"CCH")
    if apostrophe != "'":
        s = s.replace(u"'", apostrophe)
    return s


def main():

    from argparse import ArgumentParser
    import codecs

    parser = ArgumentParser(description=u"""\
Convert Japanese words in kana into roman letters.
If no argument is given, convert words read from standard-input.
""")
    arg = parser.add_argument
    arg("--system", dest="system", default="ansi",
            help="'iso' | 'hepburn' | 'ansi' | 'kunrei2' | 'road' | 'rail' | 'mofa'")
    arg("-k", "--kunrei", dest="system", action="store_const", const="iso",
            help="adopt ISO3602-compatible system aka `kunrei system'")
    arg("--macron", dest="macron",
            help="subst char for long vowel symbol; 'no' for nothing")
    arg("--apostrophe", dest="apostrophe",
            help="subst char for apostrophe e.g. hon'ya; 'no' for nothing")
    arg("--m4n", dest="m4n", action="store_true",
            help="use `m' instead of `n' before b/m/p e.g. kombu")
    arg("-X", "--no-extend", dest="extend", action="store_false",
            help="do not allow non-native pronounciation")
    arg("--encoding", help="set input-encoding")
    arg("-v", "--version", action="store_true", help="show version info")
    arg("--test", action="store_true", help="test")
    arg("words", nargs="*", metavar="word")
    args = parser.parse_args()
    if args.test:
        import doctest
        doctest.testmod()
        sys.exit(0)
    if args.version:
        cmd = os.path.basename(sys.argv[0])
        print("{cmd} version {ver}".format(cmd=cmd, ver=__version__))
        print(__copyright__)
        sys.exit(0)
    enc = args.encoding or sys.stdin.encoding or \
            "cp932" if sys.platform.startswith("win") else "utf-8"
    if (not args.macron) or (args.macron.upper() == "NO"):
        args.macron = ""
    if (not args.apostrophe) or (args.apostrophe.upper() == "NO"):
        args.apostrophe == ""
    roman = lambda s: romaji(s, system=args.system,
                            macron=args.macron,
                            apostrophe=args.apostrophe,
                            m4n=args.m4n,
                            extend=args.extend)
    if args.words:
        print(u" ".join(roman(word.decode(enc)) for word in args.words))
    else:
        for line in codecs.getreader(enc)(sys.stdin):
            print(u" ".join(roman(word) for word in line.split()))


if __name__ == "__main__":
    main()
