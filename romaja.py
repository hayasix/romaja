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


__version__ = "1.3.0"
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


def romaji(s, h=False, m=False, extend=True, apostrophe=True):
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
    if m:
        s = re.sub(ur"N([BMP])", ur"M\1", s)
    s = _translate(s, u"HU SI ZI TI TU SY ZY TY Sh Zh Th sI",
                      u"FU SHI JI CHI TSU SH J CH S Z T SI")
    if h:
        s = _translate(s, u"A^ I^ U^ E^ O^", u"AH II U E OH")
    else:
        s = _translate(s, u"A^ I^ U^ E^ O^", u"A II U E O")
    if not apostrophe:
        s = s.replace(u"'", "")
    return s


def main():

    from argparse import ArgumentParser
    import codecs

    parser = ArgumentParser(description=u"""\
            Convert Japanese words in kana into roman letters.
            If no argument is given, convert words read from standard-input.
            """)
    arg = parser.add_argument
    arg("-k", "--kunrei", action="store_true", help="use `kunrei' system")
    arg("--use-h", action="store_true", help="`h' for long")
    arg("--use-m", action="store_true", help="`m' before b/m/p")
    arg("-A", "--no-apostrophe", dest="apostrophe", action="store_false",
            help="suppress apostrophe (') e.g. hon'ya -> honya")
    arg("-X", "--no-extend", dest="extend", action="store_false",
            help="do not allow non-native pronounciation")
    arg("--encoding", help="set input-encoding")
    arg("-v", "--version", action="store_true", help="show version info")
    arg("words", nargs="*", metavar="word")
    args = parser.parse_args()

    enc = args.encoding or sys.stdin.encoding or \
            "cp932" if sys.platform.startswith("win") else "utf-8"

    if args.version:
        cmd = os.path.basename(sys.argv[0])
        print("{cmd} version {ver}".format(cmd=cmd, ver=__version__))
        print(__copyright__)
        sys.exit(0)

    if args.kunrei:
        roman = romazi
    else:
        roman = lambda s: romaji(s, h=args.use_h, m=args.use_m,
                        extend=args.extend, apostrophe=args.apostrophe)
    if args.words:
        print(u" ".join(roman(word.decode(enc)) for word in args.words))
    else:
        for line in codecs.getreader(enc)(sys.stdin):
            print(u" ".join(roman(word) for word in line.split()))


if __name__ == "__main__":
    main()
