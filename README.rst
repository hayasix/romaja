======
README
======

| 2013-04-05 HAYASHI,Hideki
| 2022-03-21 HAYASHI,Hideki


Preface
=======

This archive contains a Python module which offers various ways to
transliterate Japanese words written in Katakana/Hiragana into Romanized
representation, and vice versa.

All programs, data, documents or files in this archive are copyrighted
materials owned by HAYASI,Hideki, "Author" hereinafter, and Author
reserves all rights on them, except as noted specifically.

    Copyright (C) 2013 HAYASI Hideki.  All rights reserved.

Python is a (registered) trademark of Python Software Foundation (PSF)
and all intellectual property rights of Python belong to PSF.
For further information, visit http://www.python.org/about/legal/


System Requirements
===================

Python 3.2+


License
=======

Zope Public License (ZPL) Version 2.1


Contents
========

README.rst
    This document.

README_ja.rst
    README in Japanese.

LICENSE
    Zope Public License (ZPL) Version 2.1.

LICENSE.ja
    ZPL in Japanese (unofficial).

romaja.py
    Romanizer/deromanizer script.

setup.py
    Installation script.


Usage
=====

Module romaja
-------------

roma(KANAWORDS, system='ANSI', composite=False, name=False)
    Transliterates Japanese Katakana/Hiragana words in KANAWORDS into
    Romanized representation i.e. Romaji, according to (obsolete) ANSI
    specification by default.  `system` can be a ``str`` or ``dict``,
    as described in the next section.  `composite` determines if
    composite (accented) letters are used for long vowels.  Note that
    composite letters are out of ASCII charset.  `name` determines if
    conversion is focused on names of people.  Note that conversion CANNOT
    be flawless based on Furigana, especially for names.

katakana(ROMANWORDS, mofa=False, long_h=False)
    Transliterates romanized Japanese words into Katakana representation.
    To regard 'TIE' as 'CHE', set `mofa=True`.  To regard 'H' after
    vowels as long syllable marks, set `long_h=True`.

hiragana(ROMANWORDS, mofa=False, long_h=False)
    Transliterates romanized Japanese words into Hiragana representation.
    To regard 'TIE' as 'CHE', set `mofa=True`.  To regard 'H' after
    vowels as long syllable marks, set `long_h=True`.

Following two functions are preserved for compatibility.  They are
deprecated and will be removed in the near future.

romazi(KANAWORDS)
    Transliterates Japanese Katanaka/Hiragana words in KANAWORDS into
    Romanized representation i.e. Romaji, according to the official
    Kunrei-shiki system.

romaji(KANAWORDS)
    Transliterates Japanese Katanaka/Hiragana words in KANAWORDS into
    Romanized representation i.e. Romaji, according to the de-facto
    modern Hepburn system.


Transliteration Systems for Module romaja
=========================================

There is a variety of transliteration (Romanization) systems for
Japanese.  `system` keyword argument determines which system is used,
and furthermore, customizes how the Romanization is performed.

Prebuilt Systems
----------------

Assigning a ``str`` to `system` means a choice of prebuilt trans-
literation system among the ones listed below.

ANSI
    Modern Hepburn system or (obsolete) ANSI Z39.11-1972.  A long vowel
    is represented with a macron, or a straight line over the vowel
    letter.  An apostrophe is placed just after 'N' if a vowel or
    contracted sound, ya, yu or yo, follows.  The syllabic (moraic) 'N'
    sound (nasal) is always written with an 'N'.

ISO
    ISO3602:1989 or Kunrei-shiki system only with Table 1.  A long vowel
    is represented by a circumflex.  An apostrophe is placed just after
    'N' if a vowel follows.  The syllabic (moraic) 'N' sound (nasal) is
    always written with an 'N'.  This system does not allow non-native
    (non-Japanese) sound like 'Di'.  Such sound is converted into a
    sequence of native sound like 'Dei'.

KUNREI2
    Kunrei-shiki with Table 2.  Note: 'SHI', 'JI', 'CHA' might be used.
    'MACCHA' is used instead of 'MATCHA'.  An apostrophe is placed just
    after 'N' if a vowel or contracted sound follows.  The 'N' sound is
    always written with an 'N'.

HEPBURN
    Traditional Hepburn system.  A long vowel is represented with
    doubled letter such as 'aa'.  A hyphen is placed just after 'N' if
    a vowel follows.  The 'N' sound is written with an 'M' if a plosive
    or nasal sound, 'b', 'p' and 'm', follows.

ROAD
    Road sign system.  A long vowel is represented in the same way as
    a short one.  A hyphen is placed just after 'N' if a vowel or
    contracted sound follows.  The 'N' sound is always written with an
    'N'.

RAIL
    Railway station name system.  A long vowel is represented with a
    macron.  A hyphen is placed just after 'N' if a vowel or contracted
    sound follows.  The 'N' sound is written with an 'M' if a plosive or
    nasal sound follows.

MOFA
    Japanese MOFA (Ministry of Foreign Affairs) system.  A long vowel is
    represented in the same way as the short one.  Nothing is placed
    after 'N' even if a vowel follows.  The 'N' sound is written with an
    'M' if a plosive or nasal sound follows.  This system does not allow
    non-native (non-Japanese) sound like 'Di'.  Such sound is converted
    into a sequence of native sound like 'Dei'.  CAUTION: MOFA actually
    allows derivative spelling for names of non-native people upon
    application.

The default value is 'ANSI'.

Custom System
-------------

Assigning a ``dict`` to `system` customizes the way of transliteration.
Key values are as follows, all of which are required.

long
    A symbol to represent a long vowel.  '+' means doubled letters.
    'H' means placing an 'H' just after 'A' and 'O', doubling 'I' and
    no operation for 'U' and 'E'.  '' (null) means no operation for long
    vowels.

sep
    A character to place just after 'N' if a vowel or contracted sound
    follows.

m4n
    True to write 'N' sound with an 'M' if a plosive or nasal sound
    follows.

extend
    True to express non-native sound like 'Di'.  False to strictly
    comply with ISO3602:1989 or Kunrei-shiki only with Table 1.


Command Line Tool
=================

As a CUI command, ``romaja`` transliterates Japanese words written in
Katakana/Hiragana read from command line arguments or stdin::

    $ romaja ローマじ へんかん は めんどう だ。
    RO~MAJI HENKAN HA MENDO~ DA。

Tildes (``~``) are used as substitutive symbols for macrons.  Assigning
'ISO' or 'KUNREI2' to `system`, circumflexes (``^``) will be used.  To
represent long vowels in composite (accented) letters, add ``--composite``
or ``-c`` option [1]_::

    $ romaja -c ローマじ へんかん は めんどう だ。
    RŌMAJI HENKAN HA MENDŌ DA。

.. [1] Composite letters may be displayed in the same way as
    non-accented ones in some environments.

To assign nothing to `long` or `sep`, use ``NO`` instead.

Another CUI command ``jaroma`` transliterates romanized Japanese words
read from command line arguments or stdin::

    $ jaroma --long-h --hiragana ROHMAJI HENKAN HA MENDOH DA.
    ろーまじ へんかん は めんどー だ


Disclaimer
==========

All contents of this archive are intended for non-critical use and may
contain errors.  Author does not provide any guarantee on this program
to meet with any particular use.  For more information, read LICENSE.

This program does not perform morphological analysis, which is required
for strict Romanization of Japanese.  To get more precise results, try
MeCab (http://taku910.github.io/mecab/) etc.


Acknowledgment
==============

Romaji's for names are based on https://green.adam.ne.jp/roomazi/namae.html
by Hypnos, following the terms and conditions written on the website.
I would like to thank Hypnos for sharing the dataset.

--- END OF TEXT ---
