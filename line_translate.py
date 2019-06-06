import argparse
import sys
from googletrans import Translator


def get_printable_line_from_para(para_string):
    # end_of_line_char = '।'
    end_of_line_char = "\n"
    return para_string.split(end_of_line_char)


def main(source_dir, only_english_translate):
    end_of_para_char = "\n\n"
    translator = Translator()
    with open(source_dir + "/line-translation.html", 'w', encoding="UTF-8") as html_w:
        with open(source_dir + "/text.txt", 'r', encoding="UTF-8") as text_h:
            tag_file_string = text_h.read()
            # make sure you prepare the ``` file for para split
            # to do this, put the $ character at the end of every para in the file
            para_strings = tag_file_string.split(end_of_para_char)
            html_w.write("<table border=1>\n")
            for para_string in para_strings:
                para_lines = []
                lines = get_printable_line_from_para(para_string)
                # changing things around here a bit
                # we're going to split each chapter line into words
                for line in lines:
                    trans = translator.translate(line, dest='en', src='hi')
                    print("Translating: ", line)
                    html_w.write("<tr>\n")
                    html_w.write("<td>" + line + "</td>\n")
                    html_w.write("<td>" + trans.text + "</td>\n")
                    html_w.write("</tr>\n")
            html_w.write("</table>")


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
