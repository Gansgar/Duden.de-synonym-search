#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script allows one to easily search through the
# synonym and definition library of Duden.de
#
# ### USAGE
# For simply searching for synonyms, type in the
# correspondig word with correct lower and upper cases.
#
# But there are also some special commands:
#   exit            Closes the script
#   with/no def     Activates/Deactivates definitons in answers
#   with/no url     Activates/Deactivates the url output
#
# You can also add '#' in front of your input,
# to get an answer with definition, even when
# definitions are turned off
#
# ### NOTE
# Because it needs to download the full .html, it sometimes
# can be quite slow to use it. But that should be in the
# rarest cases.
#   Also it uses a simlle HTML parser and works perfectly for
# Duden.de at the 2016.01.10. This could change, if Duden
# updates there webpage layout.
#   On Windows please set your shell at the beginning to
# UTF-8 encoding. That is possible by typing
#  $chcp 65001
# into the terminal, before executing the script.
#
# ### COMPATIBILITY
# It was tested Python 3.6.0 on an macOS Sierra
#
#
# ©2017 Georg Friedrich

import urllib.request
from html.parser import HTMLParser
import shutil
import html


def updateWidth():
    return shutil.get_terminal_size((80, 20))[0]  # Terminal width

def printWithTS(strings, delimiter,):
    max_width = updateWidth() - 2

    for string in strings.split('\n'):
        if len(string) == 0:
            continue

        spaces = 0
        while len(string) > spaces and string[spaces] in myParser._points and string[spaces+1] == ' ':
            spaces += 2

        ret = ""
        while len(string) >= max_width:
            i = max_width
            while string[i - 1] not in delimiter:
                i = i - 1
            ret += string[:i] + "\n" + (spaces-1)*' '
            if string[i] is not ' ':
                ret += ' '
            string = string[i:]

        print(ret + string)
    print()

class myParser(HTMLParser):
    _debug = False
    _points = [u"•", "x"]

    def __init__(self):
        HTMLParser.__init__(self)
        self.in_section = False
        self.in_title = False
        self.in_syn = False
        self.in_def = False
        self.in_ul = False
        self.data = ""
        self.nested = 0

        self.with_def = False

    def handle_starttag(self, tag, attrs):
        if tag in "section":
            self.in_section = True
        if tag in "h2" and self.in_section:
            self.in_title = True
        if tag in "li" and (self.in_syn or self.in_def) and self.in_ul:
            if self._points[self.nested-1] not in self.data[-4:]:
                self.data += self.nested*'  '
            self.data += self._points[self.nested] + ' '
            self.nested += 1

        if self._debug:
            print("Start", tag)

    def handle_endtag(self, tag):
        if tag in "section":
            if len(self.data):
                if "•" not in self.data:
                    self.data = u"• " + self.data

                if self.in_syn:
                    printWithTS("Synonyms:\n" + self.data + "\n", [',', ';'])
                if self.in_def and self.with_def:
                    printWithTS("Definition:\n" + self.data + "\n", [' '])

            self.data = ""
            self.nested = 0

            self.in_section = False
            self.in_syn = False
            self.in_def = False
            self.in_ul = False

        if tag in "li" and (self.in_syn or self.in_def) and self.in_ul:
            self.data += "\n"
            self.nested -= 1

        if tag in "h2":
            self.in_title = False

        if tag in "header":
            self.in_ul = True

        if self._debug:
            print("End", tag)

    def handle_data(self, data):
        if (self.in_syn or self.in_def) and self.in_ul and len(data) > 1:
            if "Beispiele" == data or "Beispiel" == data and self.in_def:
                self.in_ul = False
            else:
                i = 0
                while data[i] == ' ':
                    i+=1
                self.data += data[i:]

        if "Synonyme zu" in data and self.in_title:
            self.in_syn = True
        if u"Bedeutungsübersicht" in data and self.in_title:
            self.in_def = True

        if self._debug:
            print("data", data, len(data), "Yes" if self.in_def else "No")


if __name__ == '__main__':
    main_url = "http://www.duden.de/rechtschreibung/"
    opener = urllib.request.FancyURLopener({})
    parser = myParser()
    
    if False:
        myParser._debug = True
        parser.with_def = True
        parser.feed('<section id="block-duden-tiles-1" class="block has-title"><header class="block-title"><div class="block-title-inner"><h2>Bedeutungsübersicht</h2><nav class="contextual-links"><a href="http://www.duden.de/node/7361" target="_blank" title="Mehr Infos">ℹ</a> </nav></div></header><div class="entry"><span class="lexem">Freiheit, unabhängig, nach eigenem Wunsch oder Ermessen zu handeln<section class="term-section"><h3>Beispiele</h3><ul><li><span><span>jemandes Handlungsfreiheit einschränken</span></span></li><li><span><span>er verlangte volle Handlungsfreiheit</span></span></li></ul></section></span></div></section>')
        exit()

    with_def = parser.with_def
    with_url = False

    # exit()
    while True:
        parser.with_def = with_def
        term = input("Search with: ")

        if len(term) < 2:
            continue
        if "exit" == term:
            exit()

        if term[:5] == "with " or term[:3] == "no ":
            tmp = term[:5] == "with "
            str_tmp = "Activating " if tmp else "Deactivating "

            if "def" in term:
                print( str_tmp + "definition for words.\n")
                with_def = tmp
                continue
            if "debug" in term:
                print( str_tmp + "debug mode.\n")
                myParser._debug = tmp
                continue
            if "url" in term:
                print( str_tmp + "url mode.\n")
                with_url = tmp
                continue

        if term[0] == '#':
            parser.with_def = True
            term = term[1:]

        url = (main_url + term)
        url = url.replace(u"ä", "ae").replace(u"ö", "oe") \
            .replace(u"ü", "ue").replace(u"ß", "sz").replace(" ", "_")
        url = url.replace(u"Ä", "Ae").replace(u"Ö", "Oe") \
            .replace(u"Ü", "Ue")

        if with_url:
            print(url)

        f = opener.open(url)
        try:
            content = f.read().decode("utf-8")
            content = html.unescape(content)
            parser.feed(content)
            # print(content)
        except ValueError as e:
            print("   There was no synonym behind that word!\n", e, "\n")
