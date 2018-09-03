# Translation links
[Walkman to unicode](http://www.hindiconverter.com/Converter.php?q=Walkman-To-Unicode)

[English To Hindi Conversion](http://hindi.changathi.com)

# Preparing text file for translation
The translation program (```main.py```) expects a text file with the name ```text.txt``` in the folder specified in the ```sourcedir``` command line arg

The text.txt should be cleaned as follows:
Lines in the file must be separated by carriage return (```\n```). So you can have multiple sentences within the same line
Paragraphs in the file must be separated by double carriage return (```\n\n```).


## Using file_prepare.py
After you get the text from the ```source.pdf``` into a ```source.txt``` file, put double carriage return (```\n\n```) after each paragraph and then run the ```file_prepare.py```

After that, you should break the paras into lines that will fit a printable page

**Hint:**: If you're using Notepad++, recommendation is to make a line ```105 Col max```. This ensure the line doesn't wrap and also reads well

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