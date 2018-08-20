import argparse
import os
import re


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
    if os.path.exists(source_dir + "/word-meaning-trans.txt"):
        word_meanings_trans = {}
        words = []
        with open(source_dir + "/word-meaning-trans.txt", 'r', encoding="UTF-8") as word_meaning_r:
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


def main(source_dir):
    chapter_lines = []
    words_found = []
    words, word_meanings = word_meaning_translation(source_dir)
    with open(source_dir + "/text.txt", 'r', encoding="UTF-8") as text_h:
        tag_file_string = text_h.read().replace('\n', ' ')
        # split the file by the पूर्ण विराम
        lines = tag_file_string.split("।")
        # now the bad one
        # iterate over the items in the word meanings dict and check thru this list if you have a word that's in this line (horribly inefficient)
        for line in lines:
            chapter_line = ChapterLine(line)
            line_words = []
            for word in words:
                # match whole words only
                # but looks like the \b doesn't work on double-byte
                if re.search("(\s*|-|!|^)" + word + "(\s*|-|!|$)", line, re.I):
                    words_found.append(word)
                    chapter_line.add_word_meaning(word_meanings[word])
            chapter_lines.append(chapter_line)
    words_not_found = [word_not_found for word_not_found in words if word_not_found not in words_found]
    print("words not found")
    print("\n".join(words_not_found))
    with open(source_dir + "/output.html", 'w', encoding="UTF-8") as html_w:
        # for chapter_line in chapter_lines:
        #     pointer = 0
        #     if len(chapter_line.word_meanings):
        #         sentence_p = "<p>"
        #         meaning_p = "<p>"
        #         sentence = ""
        #         sorted_word_meanings = get_sorted_word_meanings(chapter_line)
        #         for word_meaning in sorted_word_meanings:
        #             sentence_p += "<td style='font-size:14px'>" + chapter_line.line[pointer:word_meaning.PosStart] + "</td>"
        #             meaning_p += "<td>&nbsp;</td>"
        #             sentence_p += "<td align='center' style='font-size:14px'>" + chapter_line.line[word_meaning.PosStart:word_meaning.PosEnd] + "</td>"
        #             meaning_p += "<td style='font-size:11px'>(" + word_meaning.Meaning + " - " + word_meaning.Translation + ")</td>"
        #             sentence += chapter_line.line[pointer:word_meaning.PosStart] + chapter_line.line[word_meaning.PosStart:word_meaning.PosEnd]
        #             pointer = word_meaning.PosEnd
        #         sentence += chapter_line.line[pointer:]
        #         sentence_p += "<td>" + chapter_line.line[pointer:] + "।</td></tr>"
        #         meaning_p += "<td>&nbsp;</td></tr>"
        #         html_w.write(meaning_p)
        #         html_w.write(sentence_p)
        #         if sentence != chapter_line.line:
        #             print(sentence)
        #             print(chapter_line.line)
        #     else:
        #         html_w.write("<tr><td>" + chapter_line.line + "।</td>")
        #     html_w.write("</table>")
       for chapter_line in chapter_lines:
            html_w.write("<table>")
            pointer = 0
            if len(chapter_line.word_meanings):
                sentence_tr = "<tr>"
                meaning_tr = "<tr>"
                sentence = ""
                sorted_word_meanings = get_sorted_word_meanings(chapter_line)
                for word_meaning in sorted_word_meanings:
                    sentence_tr += "<td style='font-size:14px'>" + chapter_line.line[pointer:word_meaning.PosStart] + "</td>"
                    meaning_tr += "<td>&nbsp;</td>"
                    sentence_tr += "<td align='center' style='font-size:14px;font; font-weight:bold;'>" + chapter_line.line[word_meaning.PosStart:word_meaning.PosEnd] + "</td>"
                    if word_meaning.Meaning:
                        meaning_tr += "<td style='font-size:11px'>(" + word_meaning.Meaning + " - " + word_meaning.Translation + ")</td>"
                    else:
                        meaning_tr += "<td style='font-size:11px'>(" + word_meaning.Translation + ")</td>"
                    sentence += chapter_line.line[pointer:word_meaning.PosStart] + chapter_line.line[word_meaning.PosStart:word_meaning.PosEnd]
                    pointer = word_meaning.PosEnd
                sentence += chapter_line.line[pointer:]
                sentence_tr += "<td>" + chapter_line.line[pointer:] + "।</td></tr>"
                meaning_tr += "<td>&nbsp;</td></tr>"
                html_w.write(meaning_tr)
                html_w.write(sentence_tr)
                if sentence != chapter_line.line:
                    print(sentence)
                    print(chapter_line.line)
            else:
                html_w.write("<tr><td>" + chapter_line.line + "।</td>")
            html_w.write("</table>")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-sd", "--sourcedir", help="Please enter a source dir as argument")
    args = parser.parse_args()
    try:
        main(args.sourcedir)
    except FileNotFoundError as fnfe:
        print(fnfe)
    print("all done!")
