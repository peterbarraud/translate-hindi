import argparse
from googletrans import Translator
import csv


def main(source_dir):
    translator = Translator()
    with open(source_dir + "/word-meaning.txt", 'r', encoding="UTF-8") as word_meaning_r:
        reader = csv.DictReader(word_meaning_r, delimiter='|')
        with open(source_dir + "/word-meaning-trans.txt", 'w', encoding="UTF-8") as word_meaning_w:
            for row in reader:
                # if meaning is available and not translation, then translate from meaning
                # if meaning and translation are not available, then translate from word
                # if meaning and translation are both available, do nothing

                if row['meaning'] and not row['translation']:
                    translation = translator.translate(row['meaning'], dest='en', src='hi')
                elif not row['meaning'] and not row['translation']:
                    translation = translator.translate(row['word'], dest='en', src='hi')
                
                    row['meaning'] = tra
                stripped_line = line.strip()
                if stripped_line:
                    parts = stripped_line.split("|")
                    if len(parts) == 2:
                        word, meaning = parts

                        word_meaning_w.write(word + "|" + meaning + "|" + translation.text + "\n")
                    else:
                        word, meaning, translate = parts
                        word_meaning_w.write(word + "|" + meaning + "|" + translate + "\n")
                    print(word)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-sd", "--sourcedir", help="Please enter a source dir as argument")
    args = parser.parse_args()
    main(args.sourcedir)
    print("all done!")
