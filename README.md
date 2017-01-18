# Duden.de-synonym-search
This Python 3 script searches through the raw html page of Duden.de for synonyms of the inputed word and makes it so incredible faster than the original page.

## How to use
By default the script starts only with a word prompt. If a word is typed in correctly spelled with upper and lower case, the script shows the synonyms that Duden.de knows for that word.

Example:
```
Search with: Öse
Synonyms:
• Loch, Öffnung, Schlinge; (süddeutsch, österreichisch) Haftel;
  (landschaftlich) Schlingel; (Seemannssprache) Auge, Gatt
```

It also automaticly adds linebreaks to the output, so that words are not broken between two letters and that it looks more organised.

The Tool also supports some other commands:
```
exit            leaves the script
with/no def     Activates/Deactivates definitons in answers
with/no url     Activates/Deactivates the url output
#..WORD...      Prints out the definition temporarily for the current input
```

## NOTE
Because it needs to download the full .html, it sometimes
can be quite slow to use it. But that should be in the
rarest cases.
  Also it uses a simlle HTML parser and works perfectly for
Duden.de at the 2016.01.10. This could change, if Duden
updates there webpage layout.
  On Windows please set your shell at the beginning to
UTF-8 encoding. That is possible by typing
`$chcp 65001`
into the terminal, before executing the script.
