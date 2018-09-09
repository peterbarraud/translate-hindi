import argparse
from googletrans import Translator
import csv


class DuplicateWordsException(Exception):
    pass


class InvalidFieldsNamesInWordMeaningFile(Exception):
    pass


def check_for_duplicates(source_dir):
    with open(source_dir + "/words.txt", 'r', encoding="UTF-8") as word_meaning_r:
        reader = csv.DictReader(word_meaning_r, delimiter='|')
        bad_fieldnames = []
        if "word" not in reader.fieldnames:
            bad_fieldnames.append("word")
        if "meaning" not in reader.fieldnames:
            bad_fieldnames.append("meaning")
        if "translation" not in reader.fieldnames:
            bad_fieldnames.append("translation")
        if len(bad_fieldnames) > 0:
            raise InvalidFieldsNamesInWordMeaningFile("The word meaning file does not have the following field names: " + ", ".join(bad_fieldnames))
        word_list = []
        duplicates = []
        for row in reader:
            if row['word'] in word_list:
                duplicates.append(row['word'])
            else:
                word_list.append(row['word'])
        if len(duplicates):
            raise DuplicateWordsException("The following duplicate words were found in " + source_dir + "/word.txt" + + ":\n".join(duplicates))


def main(source_dir):
    try:
        check_for_duplicates(source_dir)
        translator = Translator()
        translation_items = []
        with open(source_dir + "/words.txt", 'r', encoding="UTF-8") as word_meaning_r:
            reader = csv.DictReader(word_meaning_r, delimiter='|')
            for row in reader:
                # if meaning is available and not translation, then translate from meaning
                # if meaning and translation are not available, then translate from word
                # if meaning and translation are both available, do nothing
                translation = row['translation']  # default
                if row['meaning'] and not row['translation']:
                    trans = translator.translate(row['meaning'], dest='en', src='hi')
                    translation = trans.text
                elif not row['meaning'] and not row['translation']:
                    trans = translator.translate(row['word'], dest='en', src='hi')
                    translation = trans.text
                if row['meaning']:
                    translation_items.append({'word': row['word'], 'meaning': row['meaning'], "translation":translation})
                else:
                    translation_items.append({'word': row['word'], 'meaning': "", "translation": translation})
                print(row['word'])
        with open(source_dir + "/words.txt", 'w', newline='', encoding="UTF-8") as word_meaning_w:
            fieldnames = ['word', 'meaning', 'translation']
            writer = csv.DictWriter(word_meaning_w, fieldnames=fieldnames, delimiter='|')
            writer.writeheader()
            writer.writerows(translation_items)

    except DuplicateWordsException as dwe:
        print(dwe)
    except InvalidFieldsNamesInWordMeaningFile as ifniwmf:
        print(ifniwmf)
    except Exception as ge:
        print(ge)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-sd", "--sourcedir", help="Please enter a source dir as argument")
    args = parser.parse_args()
    main(args.sourcedir)
    print("all done!")
