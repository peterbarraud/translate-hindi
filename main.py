import argparse
import os
import re
import sys


class TranslationNotFoundError(Exception):
    pass


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
    trans_file = source_dir + "/../../word-meaning.txt"
    if os.path.exists(trans_file):
        no_meanings = []
        word_meanings_trans = {}
        words = []
        with open(trans_file, 'r', encoding="UTF-8") as word_meaning_r:
            for line in word_meaning_r:
                if line.rstrip().split("|")[2] == '':
                    no_meanings.append(line.rstrip().split("|")[0])
                word_meanings_trans[line.rstrip().split("|")[0]] = [line.rstrip().split("|")[0], line.rstrip().split("|")[1], line.rstrip().split("|")[2]]
                words.append(line.rstrip().split("|")[0])
        if len(no_meanings) > 0:
            print("\n".join(no_meanings))
            raise TranslationNotFoundError("The following words do not have meanings in the \"word-meaning.txt\". \nPlease fix that file and then proceed")
        return words, word_meanings_trans
    else:
        raise FileNotFoundError("Could not find the translation file.")


def get_sorted_word_meanings(chapter_line):
    word_meanings_temp = {}
    for word_meaning in chapter_line.word_meanings:
        search_result = re.search(r"(?:\s*|^)(" + word_meaning[0] + r")(?:\s*|$|।)", chapter_line.line)
        if search_result.group().strip() == word_meaning[0]:
            word_meanings_temp[search_result.start()] = WordMeaningDetails(word_meaning, search_result)
    sorted_word_meanings = []
    sorted_keys = sorted(word_meanings_temp.keys())
    for key in sorted_keys:
        sorted_word_meanings.append(word_meanings_temp[key])
    return sorted_word_meanings


def get_printable_line_from_para(para_string):
    # end_of_line_char = '।'
    end_of_line_char = "\n"
    return para_string.split(end_of_line_char)


def main(source_dir, only_english_translate):
    FONT_SIZE = "16px"
    end_of_para_char = "\n\n"

    words, word_meanings = word_meaning_translation(source_dir)
    chapter_paras = []
    with open(source_dir + "/text.txt", 'r', encoding="UTF-8") as text_h:
        tag_file_string = text_h.read()
        # make sure you prepare the ``` file for para split
        # to do this, put the $ character at the end of every para in the file
        para_strings = tag_file_string.split(end_of_para_char)
        for para_string in para_strings:
            para_lines = []
            lines = get_printable_line_from_para(para_string)
            # changing things around here a bit
            # we're going to split each chapter line into words
            for line in lines:
                chapter_line = ChapterLine(line)
                words_in_line = line.split(" ")
                for word_in_line in words_in_line:
                    # because we are splitting by space and not sentence,
                    # the last word of a sentence comes with the पूर्ण विराम
                    # so check for the last word but without the पूर्ण विराम
                    if word_in_line[-1:] == '।' and word_in_line[:-1] in words:
                        chapter_line.add_word_meaning(word_meanings[word_in_line[:-1]])
                    elif word_in_line in words:
                        chapter_line.add_word_meaning(word_meanings[word_in_line])
                para_lines.append(chapter_line)
            chapter_paras.append(para_lines)

    with open(source_dir + "/output.html", 'w', encoding="UTF-8") as html_w:
        for chapter_para in chapter_paras:
            for chapter_line in chapter_para:
                html_w.write("<table>\n")
                pointer = 0
                if len(chapter_line.word_meanings):
                    sentence_tr = "<tr>"
                    meaning_tr = "<tr>"
                    sentence = ""
                    chapter_line_sorted_word_meanings = get_sorted_word_meanings(chapter_line)
                    for chapter_line_sorted_word_meaning in chapter_line_sorted_word_meanings:
                        sentence_tr += "<td style='font-size:18px'>" + chapter_line.line[pointer:chapter_line_sorted_word_meaning.PosStart] \
                                       + "</td>"
                        meaning_tr += "<td>&nbsp;</td>"
                        sentence_tr += "<td align='center' style='font-size:16px;font; font-weight:bold;'>" + \
                                       chapter_line.line[chapter_line_sorted_word_meaning.PosStart:chapter_line_sorted_word_meaning.PosEnd] + "</td>"
                        # the following line is used for unit testing
                        # to ensure that the constructed sentence is identicle to the sentence on file
                        # see the comparison check:
                        # if sentence != chapter_line.line:
                        sentence += chapter_line.line[pointer:chapter_line_sorted_word_meaning.PosStart] + \
                                    chapter_line.line[chapter_line_sorted_word_meaning.PosStart:chapter_line_sorted_word_meaning.PosEnd]
                        if chapter_line_sorted_word_meaning.Meaning and only_english_translate:
                            meaning_tr += "<td style='font-size:11px'>(" + chapter_line_sorted_word_meaning.Meaning + " - " + \
                                          chapter_line_sorted_word_meaning.Translation + ")</td>"
                        else:
                            meaning_tr += "<td style='font-size:11px'>(" + chapter_line_sorted_word_meaning.Translation + ")</td>"
                        pointer = chapter_line_sorted_word_meaning.PosEnd
                    sentence += chapter_line.line[pointer:]
                    sentence_tr += "<td>" + chapter_line.line[pointer:] + "</td></tr>\n"
                    meaning_tr += "<td>&nbsp;</td></tr>\n"
                    # sadly because I'm not able to figure out a proper regex in get_sorted_word_meanings
                    # (that does not pick up the spaces before and after a word)
                    # I have to put in this horrible, horrible HACK
                    while sentence.find("  ") > -1:
                        sentence = sentence.replace("  ", " ")
                    while sentence_tr.find("  ") > -1:
                        sentence_tr = sentence_tr.replace("  ", " ")
                    html_w.write(meaning_tr)
                    html_w.write(sentence_tr)
                    if sentence != chapter_line.line:
                        print("*********The original sentence:*********")
                        print(chapter_line.line)
                        print("*********is different from translated line*********")
                        print(sentence)
                        print("************************")
                else:
                    html_w.write("<tr><td>" + chapter_line.line + "</td></tr>\n")
                html_w.write("</table>\n")
            # end of para
            html_w.write("<div>&nbsp;</div>\n")


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
