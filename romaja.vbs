Rem EXCEL VBA version
Rem vim: set fileencoding=utf-8 fileformat=unix :

Rem Version: 3.0.0
Rem Author: HAYASI Hideki
Rem Copyright: Copyright (C) 2013 HAYASI Hideki <linxs@linxs.org>
Rem License: ZPL 2.1
Rem Email: linxs@linxs.org
Rem Status: Production


Option Explicit
Option Base 0


Private Const TR As String = _
        "XA XA XI XI XU XU XE XE XO XO " & _
        "KA GA KI GI KU GU KE GE KO GO " & _
        "SA ZA SI ZI SU ZU SE ZE SO ZO " & _
        "TA DA TI DI tU TU DU TE DE TO DO " & _
        "NA NI NU NE NO " & _
        "HA BA PA HI BI PI HU BU PU HE BE PE HO BO PO " & _
        "MA MI MU ME MO " & _
        "yA YA yU YU yO YO " & _
        "RA RI RU RE RO " & _
        "wA WA WI WE WO N' VU"
Private Const HIRACEIL As Integer = &H3094


Private Function h2k(s As String) As String

    Dim i As Long
    Dim char As String
    Dim ss As String
    Dim ceil As String

    s = Replace(s, "う゛", "ヴ")
    s = Replace(s, "ウ゛", "ヴ")
    ss = ""
    ceil = ChrW(HIRACEIL)
    For i = 1 To Len(s)
        char = Mid(s, i, 1)
        If "ぁ" <= char And char <= ceil Then char = ChrW(AscW(char) + &H60)
        ss = ss & char
    Next

    h2k = ss

End Function


Private Function use_composite(s, macron)

    Dim c As Long
    Dim subst As String

    Select Case macron
    Case "^"
        subst = ChrW(&HC2) & ChrW(&HCE) & ChrW(&HDB) & ChrW(&HCA) & ChrW(&HD4)
    Case "~"
        subst = ChrW(&H100) & ChrW(&H12A) & ChrW(&H16A) & ChrW(&H112) & ChrW(&H14C)
    Case Else
        use_composite = s
        Exit Function
    End Select
    For c = 1 To 5
        s = Replace(s, Mid("AIUEO", c, 1) & macron, Mid(subst, c, 1))
    Next

    use_composite = s

End Function


Private Function translate(s As String, before As String, after As String) As String

    Dim i As Long
    Dim words_before As Variant
    Dim words_after As Variant

    words_before = Split(before, " ")
    words_after = Split(after, " ")
    If UBound(words_before) <> UBound(words_after) Then
        Err.Raise Number:=9, Description:="Word count mismatch in translation."
        Exit Function
    End If
    For i = LBound(words_before) To UBound(words_before)
        s = Replace(s, words_before(i), words_after(i))
    Next

    translate = s

End Function


Private Function iso3602(s As String) As String

    Dim table As Variant
    Dim ss As String
    Dim i As Long
    Dim char As String
    Dim roman As String
    Dim sokuon As Boolean

    s = h2k(s)
    s = translate(s, "ヰ ヱ ヲ ヂ ヅ ウ゛ ヴ", "イ エ オ ジ ズ ヴ ブ")
    table = Split(TR, " ")
    ss = ""
    sokuon = False
    For i = 1 To Len(s)
        char = Mid(s, i, 1)
        Select Case char
        Case "ッ"
            sokuon = True
        Case "ー"  ' long vowel
            ss = ss & "^"
        Case "ァ" To "ヴ"
            roman = table(AscW(char) - AscW("ァ"))
            If InStr("yw", Left(roman, 1)) <> 0 Then ss = Left(ss, Len(ss) - 1)
            If sokuon Then ss = ss & Left(roman, 1)
            ss = ss & UCase(roman)
            sokuon = False
        Case Else
            ss = ss & char
        End Select
    Next
    s = translate(ss, "N'X N'Y N'", "N''X N''Y N")
    s = Replace(s, "X", "")
    s = Replace(s, "OUU", "O^U")
    Do
        i = Len(s)
        s = translate(s, "AA II UU EE OO", "A^ I^ U^ E^ O^")
    Loop Until Len(s) = i
    s = Replace(s, "OU", "O^")

    iso3602 = s

End Function


Public Function roma(ByVal s As String, _
        Optional ByVal system As String = "", _
        Optional ByVal macron As String = "~", _
        Optional ByVal apostrophe As String = "'", _
        Optional ByVal m4n As Boolean = False, _
        Optional ByVal extend As Boolean = True, _
        Optional ByVal composite As Boolean = False) As String

    s = h2k(s)
    Select Case UCase(system)
    Case "ANSI"
        macron = "~":
        apostrophe = "'"
        m4n = False
        extend = True
    Case "ISO"
        s = iso3602(s)
        If composite Then s = use_composite(s, "^")
        roma = s
        Exit Function
    Case "HEPBURN"
        macron = "+":
        apostrophe = "-"
        m4n = True
        extend = True
    Case "KUNREI2"
        s = translate(s, "ヂ ヅ ヂャ ヂュ ヂョ ヲ", "DI DU DYA DYU DYO WO")
        macron = "^":
        apostrophe = "'"
        m4n = False
        extend = False
    Case "ROAD"
        macron = "":
        apostrophe = "-"
        m4n = False
        extend = True
    Case "RAIL"
        macron = "~":
        apostrophe = "-"
        m4n = True
        extend = True
    Case "MOFA"
        macron = ""
        apostrophe = ""
        m4n = True
        extend = False
    Case Else
        Rem
    End Select
    s = translate(s, "クヮ グヮ", "KWA GWA")
    If extend Then s = translate(s, _
            "イェ ウィ ウェ ウォ ヴァ ヴィ ヴェ ヴォ ヴュ ヴ " & _
            "スィ シェ ズィ ジェ ティ トゥ チェ ディ ドゥ ヂェ " & _
            "ツァ ツィ ツェ ツォ ファ フィ フェ フォ", _
            "YE WI WE WO VA VI VE VO VYU VU " & _
            "ShI ShE ZhI JE ThI ThU CHE DI DU JE " & _
            "TSA TsI TSE TSO FA FI FE FO")
    s = iso3602(s)
    If m4n Then s = translate(s, "NB NM NP", "MB MM MP")
    s = translate(s, _
            "HU SI ZI TI TU SY ZY TY Sh Zh Th sI", _
            "FU SHI JI CHI TSU SH J CH S Z T SI")
    Select Case macron
    Case "+"
        s = translate(s, "A^ I^ U^ E^ O^", "AA II UU EE OO")
    Case "H"
    Case "h"
        s = translate(s, "A^ I^ U^ E^ O^", "AH II U E OH")
    Case ""
        s = translate(s, "A^ I^ U^ E^ O^", "A II U E O")
    Case "^"
        Rem
    Case Else
        s = Replace(s, "^", macron)
    End Select
    If composite And (macron = "^" Or macron = "~") Then
        s = use_composite(s, macron)
    End If
    If macron = "^" Then s = Replace(s, "TCH", "CCH")
    If apostrophe <> "'" Then s = Replace(s, "'", apostrophe)

    roma = s

End Function


Private Sub test_roma()

    Dim testpatterns As New Collection
    Dim testpattern As Variant
    Dim pattern As Variant
    Dim system As Variant
    Dim result As String
    Dim errors As Long

    testpatterns.Add Key:="ANSI", Item:=Array( _
            "かんだ KANDA", _
            "かんなみ KANNAMI", _
            "しんじゅく SHINJUKU", _
            "チェック CHEKKU", _
            "しんばし SHINBASHI", _
            "チェンマイ CHENMAI", _
            "さんあい SAN'AI", _
            "こんやく KON'YAKU", _
            "カード KA~DO", _
            "ジェラシー JERASHI~", _
            "まっちゃ MATCHA")
    testpatterns.Add Key:="ISO", Item:=Array( _
            "かんだ KANDA", _
            "かんなみ KANNAMI", _
            "しんじゅく SINZYUKU", _
            "チェック TIEKKU", _
            "しんばし SINBASI", _
            "チェンマイ TIENMAI", _
            "さんあい SAN'AI", _
            "こんやく KON'YAKU", _
            "カード KA^DO", _
            "ジェラシー ZIERASI^", _
            "まっちゃ MATTYA")
    testpatterns.Add Key:="HEPBURN", Item:=Array( _
            "かんだ KANDA", _
            "かんなみ KANNAMI", _
            "しんじゅく SHINJUKU", _
            "チェック CHEKKU", _
            "しんばし SHIMBASHI", _
            "チェンマイ CHEMMAI", _
            "さんあい SAN-AI", _
            "こんやく KON-YAKU", _
            "カード KAADO", _
            "ジェラシー JERASHII", _
            "まっちゃ MATCHA")
    testpatterns.Add Key:="KUNREI2", Item:=Array( _
            "かんだ KANDA", _
            "かんなみ KANNAMI", _
            "しんじゅく SHINJUKU", _
            "チェック CHIEKKU", _
            "しんばし SHINBASHI", _
            "チェンマイ CHIENMAI", _
            "さんあい SAN'AI", _
            "こんやく KON'YAKU", _
            "カード KA^DO", _
            "ジェラシー JIERASHI^", _
            "まっちゃ MACCHA", _
            "しゃししゅしょつ SHASHISHUSHOTSU", _
            "ちゃちちゅちょ CHACHICHUCHO", _
            "ふじゃじじゅじょ FUJAJIJUJO", _
            "ぢづぢゃぢゅぢょ DIDUDYADYUDYO", _
            "くゎぐゎを KWAGWAWO")
    testpatterns.Add Key:="ROAD", Item:=Array( _
            "かんだ KANDA", _
            "かんなみ KANNAMI", _
            "しんじゅく SHINJUKU", _
            "チェック CHEKKU", _
            "しんばし SHINBASHI", _
            "チェンマイ CHENMAI", _
            "さんあい SAN-AI", _
            "こんやく KON-YAKU", _
            "カード KADO", _
            "ジェラシー JERASHII", _
            "まっちゃ MATCHA")
    testpatterns.Add Key:="RAIL", Item:=Array( _
            "かんだ KANDA", _
            "かんなみ KANNAMI", _
            "しんじゅく SHINJUKU", _
            "チェック CHEKKU", _
            "しんばし SHIMBASHI", _
            "チェンマイ CHEMMAI", _
            "さんあい SAN-AI", _
            "こんやく KON-YAKU", _
            "カード KA~DO", _
            "ジェラシー JERASHI~", _
            "まっちゃ MATCHA")
    testpatterns.Add Key:="MOFA", Item:=Array( _
            "かんだ KANDA", _
            "かんなみ KANNAMI", _
            "しんじゅく SHINJUKU", _
            "チェック CHIEKKU", _
            "しんばし SHIMBASHI", _
            "チェンマイ CHIEMMAI", _
            "さんあい SANAI", _
            "こんやく KONYAKU", _
            "カード KADO", _
            "ジェラシー JIERASHII", _
            "まっちゃ MATCHA")
    errors = 0
    For Each system In Split("ANSI ISO HEPBURN KUNREI2 ROAD RAIL MOFA", " ")
        For Each testpattern In testpatterns(system)
            pattern = Split(testpattern, " ")
            result = roma(pattern(0), system)
            If result <> pattern(1) Then
                Debug.Print "Error(" & system & "):" & pattern(0) & " -> " & _
                            result & ", not " & pattern(1)
                errors = errors + 1
            End If
        Next
    Next
    Debug.Print CStr(errors) & " error(s)."

End Sub
