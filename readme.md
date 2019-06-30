# Translation links
[Walkman to unicode](http://www.hindiconverter.com/Converter.php?q=Walkman-To-Unicode)

[English To Hindi Conversion](http://hindi.changathi.com)

How-to Translate:
1. Open the ```source.pdf``` for a chapter
2. Copy one para at a time into (Hindi converter)[http://www.hindiconverter.com/Converter.php?q=Walkman-To-Unicode]
3. In the above converter make sure you separate each para with double-enter
4. After you've copied the entire chapters in the converter, run Convert - Walkman-To-Unicode.
5. Copy the converted Hindi text to a ```source.txt```. (Create ```source.txt```, if required)
(Preferably using Notepad++ and ensuring that the Encoding is set to UTF-8)
6. (Optionally) You might need to clean for badly converted chars.
7. Point file_prepare.py to the chapter and run it
This will put each para from ```source.txt``` into a single line and create the ```text.txt``` file
8. Now break the para lines into printable lines. Break the line at max. 90 chars (better in the range 70-85).
9. To break the lines, search for पूर्ण विराम space and copy पूर्ण विराम carriage return onto the clipboard.
10. Continue searching forward using F3 (for the पूर्ण विराम space) when you hit a convenient point, press Ctrl+V (with पूर्ण विराम carriage return on the clipboard)
Create a list of unique words that were not pre-listed in ```word-meaning.txt``` or ```word-black-list.txt```
11. Point ```make_chapter_wordlist.py``` to the chapter and run
This creates a ```words.txt``` in the chapter folder. This replicates ```word-meaning.txt```
12. First manually figure out words that we should know and move these into ```word-black-list.txt```.
13. Also, put translations against words that you know back into the ```words.txt```
14. Point ```translate_chapter_words.py``` to the chapter and run it.
Go through the translated list and find words that either have a bad translation or maybe ```Proper nouns```
15. If required, fix obviously bad translations and move any more words into ```word-black-list.txt```.
16. Remove ```words.txt```. Don't put this into ```git```
16. After you're done cleaning up ```words.txt```, copy the contents into ```word-meaning.txt```
17. Point ```main.py``` to the chapter and run it


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
##Some hindi chars that must be replaced in the source.txt
फ् = Nothing
य् = Nothing