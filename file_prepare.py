import argparse
import os
import re
import sys


def main(source_dir):
    with open(source_dir + "/source.txt", 'r', encoding="UTF-8") as text_h:
        with open(source_dir + "/text.txt", 'w', encoding="UTF-8") as text_w:
            end_of_para_char = "\n\n"
            paras = text_h.read().split(end_of_para_char)
            for para in paras:
                text_w.write(para.replace("\n"," "))
                text_w.write("\n\n")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-sd", "--sourcedir", help="Please enter a source dir as argument")
    args = parser.parse_args()
    try:
        main(args.sourcedir)
    except FileNotFoundError as file_not_found_error:
        print(file_not_found_error)
    except:
        print(sys.exc_info()[0])
    print("all done!")
