import argparse
import os
import re
import sys


class ChapterLine:
    def __init__(self, line):
        self.__line = line
        self.__word_meaning_list = []

    def add_word_meaning(self, word_meaning):
        self.__word_meaning_list.append(word_meaning)

    @property
    def line(self):
        return self.__line

    @property
    def word_meanings(self):
        return self.__word_meaning_list


class WordMeaningDetails:
    def __init__(self, word_meaning, search_result):
        self.__word = word_meaning[0]
        self.__meaning = word_meaning[1]
        self.__translation = word_meaning[2]
        self.__posstart = search_result.start()
        self.__posend = search_result.end()

    @property
    def Word(self):
        return self.__word

    @property
    def Meaning(self):
        return self.__meaning

    @property
    def Translation(self):
        return self.__translation

    @property
    def PosStart(self):
        return self.__posstart

    @property
    def PosEnd(self):
        return self.__posend


def word_meaning_translation(source_dir):
    trans_file = source_dir + "/../word-meaning-trans.txt"
    if os.path.exists(trans_file):
        word_meanings_trans = {}
        words = []
        with open(trans_file, 'r', encoding="UTF-8") as word_meaning_r:
            for line in word_meaning_r:
                word_meanings_trans[line.rstrip().split("|")[0]] = [line.rstrip().split("|")[0], line.rstrip().split("|")[1], line.rstrip().split("|")[2]]
                words.append(line.rstrip().split("|")[0])
        return words, word_meanings_trans
    else:
        raise FileNotFoundError("Could not find the translation file. Maybe you need to \"run translate\"")


def get_sorted_word_meanings(chapter_line):
    word_meanings_temp = {}
    for word_meaning in chapter_line.word_meanings:
        search_result = re.search(word_meaning[0], chapter_line.line)
        if search_result.group() == word_meaning[0]:
            word_meanings_temp[search_result.start()] = WordMeaningDetails(word_meaning, search_result)
    sorted_word_meanings = []
    sorted_keys = sorted(word_meanings_temp.keys())
    for key in sorted_keys:
        sorted_word_meanings.append(word_meanings_temp[key])
    return sorted_word_meanings


def main(source_dir, only_english_translate):
    chapter_lines = []
    words_found = []
    words, word_meanings = word_meaning_translation(source_dir)
    with open(source_dir + "/text.txt", 'r', encoding="UTF-8") as text_h:
        tag_file_string = text_h.read().replace('\n', ' ')
        # split the file by the पूर्ण विराम
        lines = tag_file_string.split("।")
        # changing things around here a bit
        # we're going to split each chapter line into words
        for line in lines:
            chapter_line = ChapterLine(line)
            words_in_line = line.split(" ")
            for word_in_line in words_in_line:
                if word_in_line in words:
                    # print(words_in_line)
                    chapter_line.add_word_meaning(word_meanings[word_in_line])
            chapter_lines.append(chapter_line)

        # now the bad one
        # iterate over the items in the word meanings dict and check thru this list if you have a word that's in this line (horribly inefficient)
    #     for line in lines:
    #         chapter_line = ChapterLine(line)
    #         line_words = []
    #         for word in words:
    #             # match whole words only
    #             # but looks like the \b doesn't work on double-byte
    #             if re.search("(\s*|-|!|^)" + word + "(\s*|-|!|$)", line, re.I):
    #                 words_found.append(word)
    #                 chapter_line.add_word_meaning(word_meanings[word])
    #         chapter_lines.append(chapter_line)
    # words_not_found = [word_not_found for word_not_found in words if word_not_found not in words_found]
    # now we're going to put word meanings into a central file and get them out of there
    # should reduce the ammount of work we need to do for this and also gives Daniel a better view of things
    # words mean the same thing no matter where they are
    # print("words not found")
    # print("\n".join(words_not_found))
    # print("==========================\n")
    with open(source_dir + "/output.html", 'w', encoding="UTF-8") as html_w:
       for chapter_line in chapter_lines:
            html_w.write("<table>\n")
            pointer = 0
            if len(chapter_line.word_meanings):
                sentence_tr = "<tr>"
                meaning_tr = "<tr>"
                sentence = ""
                sorted_word_meanings = get_sorted_word_meanings(chapter_line)
                for word_meaning in sorted_word_meanings:
                    sentence_tr += "<td style='font-size:14px'>" + chapter_line.line[pointer:word_meaning.PosStart]\
                                                                                                            + "</td>"
                    meaning_tr += "<td>&nbsp;</td>"
                    sentence_tr += "<td align='center' style='font-size:14px;font; font-weight:bold;'>" +\
                                   chapter_line.line[word_meaning.PosStart:word_meaning.PosEnd] + "</td>"
                    if word_meaning.Meaning and only_english_translate:
                        meaning_tr += "<td style='font-size:11px'>(" + word_meaning.Meaning + " - " +\
                                      word_meaning.Translation + ")</td>"
                    else:
                        meaning_tr += "<td style='font-size:11px'>(" + word_meaning.Translation + ")</td>"
                    sentence += chapter_line.line[pointer:word_meaning.PosStart] +\
                                chapter_line.line[word_meaning.PosStart:word_meaning.PosEnd]
                    pointer = word_meaning.PosEnd
                sentence += chapter_line.line[pointer:]
                sentence_tr += "<td>" + chapter_line.line[pointer:] + "।</td></tr>\n"
                meaning_tr += "<td>&nbsp;</td></tr>\n"
                html_w.write(meaning_tr)
                html_w.write(sentence_tr)
                if sentence != chapter_line.line:
                    print("*********The original sentence:*********")
                    print(chapter_line.line)
                    print("*********is different from translated line*********")
                    print(sentence)
                    print("************************")
            else:
                html_w.write("<tr><td>" + chapter_line.line + "।</td></tr>\n")
            html_w.write("</table>\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-sd", "--sourcedir", help="Please enter a source dir as argument")
    # to tranlate only to english (not output Hindi word-meaning), use following switch
    # set oe = 1 to only include English translation. Use 0 (or don't include this swtich) to include Hindi word-meaning
    parser.add_argument("-oe", "--onlyenglish", help="Please enter True/False if you want to translate only to English")
    args = parser.parse_args()
    try:
        main(args.sourcedir, bool(args.onlyenglish))
    except FileNotFoundError as file_not_found_error:
        print(file_not_found_error)
    except:
        print(sys.exc_info()[0])
    print("all done!")
