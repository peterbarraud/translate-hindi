import argparse
import sys
import os


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


def get_blacklisted_words(source_dir):
    with open(source_dir + "/../word-black-list.txt", 'r', encoding="UTF-8") as text_h:
        return [blacklisted_word.rstrip() for blacklisted_word in text_h]


def main(source_dir):
    # first an important check to ensure that blacklisted words are not in the word-meaning file
    difficult_words, _ = word_meaning_translation(source_dir)
    blacklisted_words = get_blacklisted_words(source_dir)
    overlap_words = [overlap_word for overlap_word in difficult_words if overlap_word in blacklisted_words]
    if len(overlap_words) > 0:
        print("The following difficult words are also in the list of blacklisted words.")
        print("The procedure will NOT run. Please correct these errors first.")
        print("\n".join(overlap_words))
    else:
        with open(source_dir + "/source.txt", 'r', encoding="UTF-8") as text_h:
            with open(source_dir + "/words.txt", 'w', encoding="UTF-8") as text_w:
                text = text_h.read()
                # remove all ूर्ण विराम
                text = text.replace("\n", " ")
                text = text.replace("।", " ")
                text = text.replace("?", " ")
                text = text.replace("!", " ")
                text = text.replace(",", " ")
                chapter_words = set(text.split(" "))
                chapter_words = [word for word in chapter_words if word not in difficult_words]
                chapter_words = [word for word in chapter_words if word not in blacklisted_words]

                text_w.write("\n".join([chapter_word + "||" for chapter_word in chapter_words]))


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
