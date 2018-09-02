# Translation links
[Walkman to unicode](http://www.hindiconverter.com/Converter.php?q=Walkman-To-Unicode)

[English To Hindi Conversion](http://hindi.changathi.com)

# Word meaning file format
Pipe separated file with a header of (exactly) this format:
```
word|meaning|translation
```
**Notes:**
* To get the word-meaning and the English translation, just put the word
```
<word>
```
* To get only English translation (*no local language meaning*):
```
<word>||
```
### Important:
The translate.py does not do word-meaning. That means, you have to do word-meaning manually.
So, a line like this will not generate meaning of "work":
```
<word>||<translation>
# Bal ram katha
[Online](http://ncertbooks.prashanthellina.com/class_6.Hindi.BalRamKatha/index.html)

# Known problems and solutions (workarounds)

## Problem
You see the following in read Hindi text: \ufeff
## Issue
There is a problem with the file encoding
##Solution
Open the file in Notepad++ and choose Encoding > Encode in UTF-8