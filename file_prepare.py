import argparse
import os
import re
import sys
import os.path


class FileFoundError(Exception):
    pass


def get_split_file_contents(file_contents):
    max_line_break_point = 85
    last_line_break_point = 0
    # first let's pull it all into a single line
    file_contents = file_contents.replace("\n", " ")
    # and remove any double spaces
    file_contents = file_contents.replace("  ", " ")
    location_pointer = 0
    last_exclaimation_or_questionmark_location = 0
    last_comma_location = 0
    last_pornaviram_location = 0
    last_next_best_punctuation_location = 0
    lines = []
    while True:
        if file_contents[location_pointer] == "!" or file_contents[location_pointer] == "?":
            last_exclaimation_or_questionmark_location = location_pointer
        elif file_contents[location_pointer] == ",":
            last_comma_location = location_pointer
        elif file_contents[location_pointer] == "।":
            last_pornaviram_location = location_pointer
        if location_pointer == max_line_break_point + 1 + last_line_break_point:
            if last_pornaviram_location > 0:
                lines.append(file_contents[last_line_break_point:last_pornaviram_location+1])
                last_line_break_point = last_pornaviram_location + 2
                location_pointer = last_line_break_point
            elif last_exclaimation_or_questionmark_location > 0:
                lines.append(file_contents[last_line_break_point:last_exclaimation_or_questionmark_location+1])
                last_line_break_point = last_exclaimation_or_questionmark_location + 2
                location_pointer = last_line_break_point
            elif last_comma_location > 0:
                lines.append(file_contents[last_line_break_point:last_comma_location+1])
                last_line_break_point = last_comma_location + 2
                location_pointer = last_line_break_point
            else:
                # the freak case when there's nothing to break at 85
                # then let's go backwards to the last space and break there
                while True:
                    print(file_contents[location_pointer])
                    if file_contents[location_pointer] == " ":
                        lines.append(file_contents[last_line_break_point:location_pointer + 1])
                        last_line_break_point = location_pointer + 1
                        location_pointer = last_line_break_point
                        break
                    location_pointer = location_pointer - 1
            # reset punctuations
            last_exclaimation_or_questionmark_location = 0
            last_comma_location = 0
            last_pornaviram_location = 0
        location_pointer += 1
        if location_pointer == len(file_contents):
            lines.append(file_contents[last_line_break_point:location_pointer])
            break

    return lines

def main(source_dir):
    if os.path.isfile(source_dir + "/text.txt"):
        raise FileFoundError(source_dir + "/text.txt" + " found in the destination folder. "
                                                        "This is a destructive procedure so we never overwrite. "
                                                        "If you really want to do this, "
                                                        "delete the destination file manually.")
    else:
        with open(source_dir + "/source.txt", 'r', encoding="UTF-8") as text_h:
            output_file_lines = get_split_file_contents(text_h.read())
            with open(source_dir + "/text.txt", 'w', encoding="UTF-8") as text_w:
                text_w.write("\n".join(output_file_lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-sd", "--sourcedir", help="Please enter a source dir as argument")
    args = parser.parse_args()
    try:
        main(args.sourcedir)
    except FileNotFoundError as file_not_found_error:
        print(file_not_found_error)
    except TypeError as typeError:
        print(typeError)
    except FileFoundError as ffe:
        print(ffe)
    except:
        print(sys.exc_info()[0])
    print("all done!")
