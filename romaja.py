#!/usr/bin/env python2.6
# vim: fileencoding=utf-8 fileformat=unix

"""romaja.py: Japanese Kana to Romaji converter

Copyright (C) 2013 HAYASI Hideki <linxs@linxs.org>  All rights reserved.

This software is subject to the provisions of the Zope Public License,
Version 2.1 (ZPL). A copy of the ZPL should accompany this distribution.
THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
FOR A PARTICULAR PURPOSE.
"""


import sys
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


__version__ = "0.3.1"
__author__ = "HAYASI Hideki"
__copyright__ = "Copyright (C) 2013 HAYASI Hideki <linxs@linxs.org>"
__license__ = "ZPL 2.1"
__email__ = "linxs@linxs.org"
__status__ = "Development"

__all__ = ("romazi", "romaji")

KT = dict(
        x=u"アイウエオ",
        k=u"カキクケコ",
        g=u"ガギグゲゴ",
        s=u"サシスセソ",
        z=u"ザジズゼゾ",
        t=u"タチツテト",
        d=u"ダヂヅデド",
        n=u"ナニヌネノ",
        h=u"ハヒフヘホ",
        b=u"バビブベボ",
        p=u"パピプペポ",
        m=u"マミムメモ",
        y=u"ヤ〓ユ〓ヨ",
        r=u"ラリルレロ",
        w=u"ワヰ〓ヱヲ",
        )
KR = dict((k[v], c + "aiueo"[v]) for (c, k) in KT.items() for v in range(5))


def _replace(s, in_, out):
    for (a, b) in zip(in_.split(), out.split()):
        s = s.replace(a, b)
    return s


def hira_to_kata(s):
    ss = list(s)
    for p, c in enumerate(ss):
        cc = ord(c)
        if 0x3041 <= cc <= 0x3096:
            ss[p] = unichr(cc + 0x60)
    return "".join(ss)


def romazi(s):
    s = hira_to_kata(s)
    s = _replace(s, u"ヰ ヱ ヲ ヂ ヅ", u"イ エ オ ジ ズ")
    s = _replace(s, u"ファ フィ フェ フォ", u"fa fi fe fo")
    s = _replace(s, u"ウ゛", u"ヴ")
    s = _replace(s, u"ヴァ ヴィ ヴ ヴェ ヴォ", u"va vi vu ve vo")
    s = _replace(s, u"ディ ドゥ", u"di du")
    s = _replace(s, u"ァ ィ ゥ ェ ォ", u"a i u e o")
    s = _replace(s, u"ン", u"n'")
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
            ss[pm] = ss[pm][:-1] + "y" + "auo"[u"ャュョ".index(c)]
            ss[p] = ""
        elif c == u"ッ":
            sokuon = True
            ss[p] = ""
        elif c == u"ー":
            ss[p] = "^"
    s = "".join(ss)
    s = s.replace("x", "")
    s = re.sub(r"n'([^aiueoy])", r"n\1", s)
    s = s.replace("ouu", "o^u")
    for c in "aiueo":
        s = re.sub(c + "{2,}", c + "^", s)
    s = s.replace("ou", "o^")
    s = s.strip("'")
    return s


def romaji(s, use_h=False, sup_apo=False):
    s = romazi(s)
    s = re.sub(r"n([bmp])", r"m\1", s)
    s = _replace(s, "hu si zi ti tu sy zy ty", "fu shi ji chi tsu sh j ch")
    s = _replace(s, "a^ i^ u^ e^ o^", "ah ii u e oh")
    if not use_h:
        s = _replace(s, "ah oh", "a o")
    if sup_apo:
        s = s.replace("'", "")
    return s


def main():

    from optparse import OptionParser
    import codecs

    parser = OptionParser(usage=u"""\
    {python}{script} [options] [word_in_kana ...]

    Convert Japanese words in kana into roman letters.
    If no argument is given, convert words read from standard-input.""".format(
        python="python " if sys.argv[0].endswith(".py") else "",
        script=sys.argv[0]))
    parser.add_option("--use_h",
            dest="use_h", action="store_true",
            help="represent long syllable with `h'")
    parser.add_option("-A", "--suppress-apostrophe",
            dest="sup_apo", action="store_true",
            help="suppress apostrophe (') e.g. hon'ya -> honya")
    parser.add_option("-k", "--kunrei",
            dest="kunrei", action="store_true",
            help="convert in kunrei-style")
    parser.add_option("--encoding", dest="encoding",
            help="set input-encoding")
    parser.add_option("-v", "--version", dest="version", action="store_true",
            help="show version information")
    opts, args = parser.parse_args()

    enc = opts.encoding or sys.stdin.encoding or \
            "cp932" if sys.platform.startswith("win") else "utf-8"

    if opts.version:
        cmd = sys.argv[0].decode(enc).split("\\")[-1].lower()
        print "{cmd} version {version}".format(cmd=cmd, version=__version__)
        print __copyright__
        sys.exit(0)

    if opts.kunrei:
        roman = romazi
    else:
        roman = lambda s: romaji(s, use_h=opts.use_h, sup_apo=opts.sup_apo)
    if args:
        print " ".join(roman(arg.decode(enc)) for arg in args)
    else:
        for line in codecs.getreader(enc)(sys.stdin):
            print " ".join(roman(word) for word in line.split())


if __name__ == "__main__":

    main()
