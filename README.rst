======
README
======

| 2013-04-05 HAYASI,Hideki
| 2016-08-20 HAYASI,Hideki


Abstract
========

This archive contains a Python module which offers various ways to
transliterate Japanese words written in Katakana/Hiragana into Romanized
representation.

All programs, data, documents or files in this archive, including this
document, are copyrighted materials owned by HAYASI,Hideki, "Author"
hereinafter, and Author reserves all rights on them, except as noted
specifically.

    Copyright (C) 2013 HAYASI Hideki.  All rights reserved.

Python is a (registered) trademark of Python Software Foundation (PSF)
and all intellectual property rights of Python belongs to PSF.
For further information, visit: http://www.python.org/about/legal/


System Requirements
===================

Python 3.5


License
=======

Zope Public License (ZPL) Version 2.1


Contents
========

:README.rst:
:README_ja.rst:

    This document and its Japanese version.

:LICENSE:
:LICENSE.ja:

    Zope Public License (ZPL) Version 2.1 and its Japanese version.

:romaja.py:

    The module.

:setup.py:

    Installation script.


Usage
=====

``romaja.py`` offers the folowing module functions.

:roma(KANAWORD, system='ANSI', composite=False):

    Transliterates Japanese Katakana/Hiragana words in KANAWORD into
    Romanized representation i.e. Romaji, according to (obsolete) ANSI
    specification by default.  ``system`` can be a ``str`` or ``dict``,
    as described in the next section.  ``composite`` determines if
    composite (accented) letters are used for long vowels.  Note that
    composite letters are out of ASCII charset.

Following two functions are preserved for compatibility.  They are
deprecated and will be removed in the near future.

:romazi(KANAWORD):

    Transliterates Japanese Katanaka/Hiragana words in KANAWORD into
    Romanized representation i.e. Romaji, according to the official
    Kunrei-shiki system.

:romaji(KANAWORD):

    Transliterates Japanese Katanaka/Hiragana words in KANAWORD into
    Romanized representation i.e. Romaji, according to the de-facto
    modern Hepburn system.

Arguments for ``system``
========================

``system`` can be a ``str`` as followings.

``'ANSI'``
    Modern Hepburn system or (obsolete) ANSI Z39.11-1972.  A long vowel
    is expressed by a macron, or a straight line over the vowel letter.
    An apostrophe is placed just after 'N' if a vowel or contracted
    sound, ya, yu or yo, follows.  The syllabic (moraic) 'N' sound
    (nasal) is usually written with an 'N'.

``'ISO'``
    ISO3602:1989 or Kunrei-shiki system only with Table 1.  A long vowel
    is represented by a circumflex.  An apostrophe is placed just after
    'N' if a vowel follows.  The syllabic (moraic) 'N' sound (nasal) is
    usually written with an 'N'.  This system does not allow non-native
    (non-Japanese) sound like 'Di'.  Such sound is converted into a
    sequence of native sound like 'Dei'.

``'KUNREI2'``
    Kunrei-shiki with Table 2.  Note: 'SHI', 'JI', 'CHA' might be used.
    'MACCHA' is used instead of 'MATCHA'.  An apostrophe is placed just
    after 'N' if a vowel or contracted sound follows.  The 'N' sound is
    usually written with an 'N'.

``'HEPBURN'``
    Traditional Hepburn system.  A long vowel is represented with
    doubled letter such as 'aa'.  A hyphen is placed just after 'N' if
    a vowel follows.  The 'N' sound is written with an 'M' if a plosive
    or nasal sound, 'b', 'p' and 'm', follows.

``'ROAD'``
    Road sign system.  A long vowel is represented in the same way as
    a short one.  A hyphen is placed just after 'N' if a vowel or
    contracted sound follows.  The 'N' sound is usually written with an
    'N'.

``'RAIL'``
    Railway station name system.  A long vowel is represented with a
    macron.  A hyphen is placed just after 'N' if a vowel or contracted
    sound follows.  The 'N' sound is written with an 'M' if a plosive or
    nasal sound follows.

``'MOFA'``
    Japanese MOFA (Ministry of Foreign Affairs) system.  A long vowel is
    represented in the same way as the short one.  Nothing is placed
    after 'N' even if a vowel follows.  The 'N' sound is written with an
    'M' if a plosive or nasal sound follows.  This
    system does not allow non-native (non-Japanese) sound like 'Di'.
    Such sound is converted into a sequence of native sound like 'Dei'.
    CAUTION: MOFA actually allows derivative spelling for names of non-
    native people upon application.

The default value is ``'ANSI'``.

``system`` can also be a ``dict`` which has all of the following keys.

``'macron'``
    A symbol to represent a long vowel.  ``'+'`` means doubled letters.
    ``'H'`` means placing an ``'H'`` just after 'A' and 'O', doubling
    'I' and no operation for 'U' and 'E'.  ``''`` (null) means no
    operation for long vowels.

``'apostrophe'``
    A character to place just after 'N' if a vowel or contracted sound
    follows.

``'m4n'``
    True to write 'N' sound with an 'M' if a plosive or nasal sound
    follows.

``'extend'``
    True to express non-native sound like 'Di'.  False to strictly
    comply with ISO3602:1989 or Kunrei-shiki only with Table 1.

Command Line Tool
=================

As a CUI command, ``romaja.py`` transliterates Japanese words written in
Katakana/Hiragana read from command line arguments or stdin.::

    $ python romaja.py ローマじ へんかん は めんどう だ。
    RO~MAJI HENKAN HA MENDO~ DA。

Tildes (``~``) are used as substitutive symbols for macrons.  Assigning
``'ISO'`` or ``'KUNREI2'`` for ``system``, circumflexes (``^``) will be
used.  To represent long vowels in composite (accented) letters, add
option ``--composite`` or ``-c``.

    $ py romaja.py -c ローマじ へんかん は めんどう だ。
    RŌMAJI HENKAN HA MENDŌ DA。

(Unfortunately composite letters are displayed in the same way as non-
accented ones in some environments.)

To feed a null string for ``macron`` or ``apostrophe``, use ``'NO'``
instead.


Disclaimers
===========

All contents of this archive are intended for non-critical use and may
contain errors.  Author does not provide any guarantee on this program
to meet with any specific use.

This program does not perform morphological analysis, which is required
for strict Romanization of Japanese.  To get more precise results, try
MeCab (http://taku910.github.io/mecab/) etc.
