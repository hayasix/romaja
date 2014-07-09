======
README
======

| 2013-04-05 林秀樹
| 2013-04-09 林秀樹
| 2013-04-10 林秀樹


このアーカイブについて
======================

このアーカイブには、日本語のかな表記 (ひらがなまたはカタカナ) を
ローマ字表記へ変換するプログラムを収録しています。

このアーカイブに含まれるプログラム、データ、本書を含む文書その他の
ファイルは、特に記載がない限り、林秀樹が著作権を有し、所有権を
留保しています。

    Copyright (C) 2013 HAYASI Hideki.  All rights reserved.

Python は Python Software Foundation の登録商標または商標であり、
その知的財産権は同団体が保有し管理しています。
詳しくは http://www.python.org/about/legal/ をご覧ください。


動作条件
========

- Python 2.6+

Python 3 で使用するには、2to3 で Python 3 用コードへ変換してください。


ライセンス
==========

Zope Public License (ZPL) Version 2.1 を採用しています。


収録物
======

:README.rst:

    本書

:LICENSE:
:LICENSE.ja:

    Zope Public License (ZPL) Version 2.1

:romaja.py:

    プログラム本体

:setup.py:

    ``romaja.py`` から py2exe を利用して Windows 実行形式を生成したり
    ソースファイル配布用 zip ファイルを生成したりするためのスクリプトです。


使い方
======

``romaja.py`` は次のモジュール関数を提供します。

:romazi(KANAWORD):

    KANAWORD 中のひらがなまたはカタカナを訓令式ローマ字へ変換します。

:romaji(KANAWORD, use_h=False):

    KANAWORD 中のひらがなまたはカタカナをヘボン式ローマ字へ変換します。
    ``use_h=True`` とすると、アーおよびオーを ah, oh へ変換します。
    なお、イーは常に ii となり、ウーおよびエーは長音でも短音の場合と
    同じ表記になります。

``romaja.py`` をスクリプトとして実行すると、コマンドライン引数
または標準入力から得た表記のうちひらがなまたはカタカナの部分をローマ字へ
変換します。::

    C:>　python romaja.py --help
    Usage:     python romaja.py [options] [word_in_kana ...]

        Convert Japanese words in kana into roman letters.
        If no argument is given, convert words read from standard-input.

    Options:
      -h, --help           show this help message and exit
      --use_h              represent long syllable with `h'
      --kunrei             convert in kunrei-style
      --encoding=ENCODING  set input-encoding
      -v, --version        show version information

    C:> python romaja.py ローマじ へんかん は めんどう だ。
    romaji henkan ha mendo da。


注意事項
========

- 人名変換を目的としていますので、複数の単語をならべたかな表記は
  正しく変換できないことがあります。

- 日本語を想定しており、外国人名は適切に変換できないことがあります。
  次の例では「ッティ」は「tti」となりません。::

    C:> romaja まっちょ マセラッティ カルヴァン
    matcho maserattei karuvan


py2exe による Windows 実行形式
==================================

py2exe を利用して Windows 実行形式を生成する場合は、次のとおり実行します。::

    C:> python setup.py py2exe

``dist`` ディレクトリの中に ``romaja.exe`` および ``romaja.zip`` が
できています。
``romaja.exe`` と ``romaja.zip`` は、同じフォルダに置いてください。
