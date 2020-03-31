#!/usr/bin/env python3
# vim: set fileencoding=utf-8 fileformat=unix expandtab :

# Copyright (C) 2020 HAYASHI Hideki <hideki@hayasix.com>  All rights reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL). A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.

"""{script}: Japanese Reverse Kana Romanizer

Usage: {script} [options] [WORD...]

Options:
  -h, --help            show this
  --version             show version
  --hiragana            return HIRAGANA instead of KATAKANA
  --mofa                MOFA system i.e. TIE=CHE
  --long-h              H is used for long syllables
  --test                test this program
"""

import sys
import os

import docopt


__version__ = "0.1.1"
__author__ = "HAYASHI Hideki"
__copyright__ = "Copyright (C) 2020 HAYASHI Hideki"
__license__ = "ZPL 2.1"
__email__ = "hideki@hayasix.com"
__status__ = "Beta"

__all__ = ("katakana", "hiragana")

RK = {
        "_": "アイウエオ", "K": "カキクケコ", "S": "サシスセソ",
        "T": "タチツテト", "N": "ナニヌネノ", "H": "ハヒフヘホ",
        "M": "マミムメモ", "Y": ("ヤ","イ","ユ","イェ","ヨ"),
        "R": "ラリルレロ", "W": "ワヰウヱヲ",
        "G": "ガギグゲゴ", "Z": "ザジズゼゾ", "D": "ダヂヅデド",
        "P": "パピプペポ", "B": "バビブベボ",
        "C": "〓チ〓〓〓", "X": "ァィゥェォ",
        "J": ("ジャ","ジ","ジュ","ジェ","ジョ"),
        "V": ("ヴァ","ヴィ","ヴ","ヴェ","ヴォ"),
        "t": ("テャ","ティ","テュ","テェ","テョ"),
        "s": ("ツァ","ツィ","ツ","ツェ","ツォ"),
        }
VOWELS = "AIUEO"


def _translate(s, in_, out):
    for (a, b) in zip(in_.split(), out.split()):
        s = s.replace(a, b)
    return s


def katakana(s, mofa=False, long_h=False):
    """Convert romaji expression to katakana.

    >>> assert katakana("KANDA") == "カンダ"
    >>> assert katakana("KANNAMI") == "カンナミ"
    >>> assert katakana("SINZYUKU") == "シンジュク"
    >>> assert katakana("SHINJUKU") == "シンジュク"
    >>> assert katakana("SHIMBASHI") == "シンバシ"
    >>> assert katakana("TIEKKU") == "チエック"
    >>> assert katakana("TIEKKU", mofa=True) == "チェック"
    >>> assert katakana("CHEKKU") == "チェック"
    >>> assert katakana("TIENMAI") == "チエンマイ"
    >>> assert katakana("TIENMAI", mofa=True) == "チェンマイ"
    >>> assert katakana("CHENMAI") == "チェンマイ"
    >>> assert katakana("SAN'AI") == "サンアイ"
    >>> assert katakana("KON'YAKU") == "コンヤク"
    >>> assert katakana("KON'NYAKU") == "コンニャク"
    >>> assert katakana("KONNYAKU") == "コンニャク"
    >>> assert katakana("MATTYA") == "マッチャ"
    >>> assert katakana("MACCHA") == "マッチャ"
    >>> assert katakana("MATCHA") == "マッチャ"
    >>> assert katakana("MATCHI") == "マッチ"
    >>> assert katakana("AHA") == "アハ"
    >>> assert katakana("AHA", long_h=True) == "アーア"
    >>> assert katakana("ÂA") == "アーア"
    """
    s = s.upper()
    s = _translate(s, "SHI CHI JI TCH", "SI TI ZI TTY")
    if mofa: s = _translate(s, "TIE", "CHE")
    pc = ""
    y = False
    el = False
    result = []
    for c in s:
        if c in "ÂÎÛÊÔ":
            c = _translate(c, "Â Î Û Ê Ô", "A I U E O")
            el = True
        if c in VOWELS:
            vi = VOWELS.index(c)
            if pc not in RK:
                result.append(pc)
                pc = ""
            if y:
                result.append(RK[pc or "_"][3 if pc == "d" else 1])
                result.append("ャィュェョ"[vi])
            else:
                result.append(RK[pc or "_"][vi])
            if el: result.append("ー")
            pc = ""
            y = False
            el = False
            continue
        pcc = pc + c
        if pc and c == "Y": y = True
        elif long_h and pc == "" and c == "H" and result: result.append("ー")
        elif pc == "N" or (pc == "M" and c in ("B", "P")):
            result.append("ン")
            pc = "" if c == "'" else c
        elif pc == c: result.append("ッ")
        elif pcc in ("DH", "TH"): pc = pc.lower()
        elif pcc == "SH": y = True
        elif pcc in ("CH", "TC"): pc = "T"; y = True
        elif pcc == "TS": pc = "s"
        else: result.append(pc); pc = c
    if pc == "N":
        result.append("ン")
    return "".join(result)


def k2h(s):
    return "".join(
            chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" or "ヽ" <= c <= "ヾ"
            else c
            for c in s)


def hiragana(s, mofa=False, long_h=False):
    return k2h(katakana(s, mofa, long_h))


def main():
    args = docopt.docopt(__doc__.format(script=os.path.basename(__file__)),
                         version=__version__)
    if args["--test"]:
        import doctest
        doctest.testmod()
        return
    kana = hiragana if args["--hiragana"] else katakana
    mofa = args["--mofa"]
    long_h = args["--long-h"]
    if args["WORD"]:
        print(" ".join(kana(word, mofa, long_h) for word in args["WORD"]))
    else:
        for line in sys.stdin:
            print(" ".join(kana(word, mofa, long_h) for word in line.split()))


if __name__ == "__main__":
    sys.exit(main())
