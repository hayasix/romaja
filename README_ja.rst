======
README
======

| 2013-04-05 林秀樹
| 2016-08-18 林秀樹


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

- Python 2.7

Python 3 で使用するには、2to3 で Python 3 用コードへ変換してください。


ライセンス
==========

Zope Public License (ZPL) Version 2.1 を採用しています。


収録物
======

:README_ja.rst:

    本書

:LICENSE:
:LICENSE.ja:

    Zope Public License (ZPL) Version 2.1

:romaja.py:

    プログラム本体

:setup.py:

    ``romaja.py`` から py2exe を利用して Windows 実行形式を生成したり
    ソースファイル配布用 zip ファイルを生成したりするためのスクリプト
    です。


使い方
======

``romaja.py`` は次のモジュール関数を提供します。

:romazi(KANAWORD):

    KANAWORD 中のひらがなまたはカタカナを訓令式ローマ字へ変換します。

:romaji(KANAWORD, system='ANSI'):

    KANAWORD 中のひらがなまたはカタカナをヘボン式ローマ字へ変換します。
    system には 'ANSI', 'ISO', 'HEPBURN', 'KUNREI2', 'ROAD', 'RAIL'
    または 'MOFA' を 指定できます。デフォルト値は 'ANSI' です。'ISO'
    は訓令式 (第一表のみ) で、第二表も用いるものが 'KUNREI2' です。
    'MOFA' は外務省式です。

``romaja.py`` をスクリプトとして実行すると、コマンドライン引数
または標準入力から得た表記のうちひらがなまたはカタカナの部分をローマ字
へ変換します。::

    C:> python romaja.py ローマじ へんかん は めんどう だ。
    RO~MAJI HENKAN HA MENDO~ DA。

チルダ (~) はマクロンの代用として出力されているものです。system に 'ISO'
や 'KUNREI2' を指定した場合はサーカムフレックス (^) が出力されます。


注意事項
========

- 人名変換を目的としていますので、複数の単語をならべたかな表記は
  正しく変換できないことがあります。


py2exe による Windows 実行形式
==================================

py2exe を利用して Windows 実行形式を生成する場合は、次のとおり実行します。::

    C:> python setup.py py2exe

``dist`` ディレクトリの中に ``romaja.exe`` および ``romaja.zip`` が
できています。
``romaja.exe`` と ``romaja.zip`` は、同じフォルダに置いてください。
