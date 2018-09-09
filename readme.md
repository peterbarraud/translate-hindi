# Translation links
[Walkman to unicode](http://www.hindiconverter.com/Converter.php?q=Walkman-To-Unicode)

[English To Hindi Conversion](http://hindi.changathi.com)

How-to Translate:
1. get source.pdf from online
2. copy the text in source.txt (make source.txt, if required)
3. take each section (page or column) from source.pdf and translate font using http://www.hindiconverter.com/Converter.php?q=Walkman-To-Unicode
and paste it into source.text
4. Run make_chapter_wordlist.py to create a words.txt file in the chapter folder
5. check the end of each para in the source.pdf and in the source.txt separate paras by double-carriage return ("\n\n")
7. point the file_prepary.py -sd switch to the chapter folder and run it
this creates the text.txt with each para on a separate line
8. now manually break the line (not sentences!) by the length of max. 80-85 (or less) columns per line
a simple way to do this, is (in Notepad++) to search for ।  (पूर्ण विराम) followed by space and look at the Col: in the status bar
put a । and carriage return into the clipboard and when you hit a । at the appropriate col point just hit Ctrl+V
**Note:** In Notepad++ use F3 to search forward and Shift+F3 to search back


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