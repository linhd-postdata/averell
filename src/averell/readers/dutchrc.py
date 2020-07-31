import json
from pathlib import Path
import re


def parse_poem(annotated_path, original_text):
    """JSON poem parser for 'Dutch Renaissance poetry' corpus.
    We read the data and find elements like title, author, year, etc. Then
    we iterate over the poem text and we look for each stanza and line data.

    :param annotated_path: Path for the annotated csv file
    :param original_text: Path for the original txt file
    :return: Dict with the data obtained from the poem
    :rtype: dict
    """
    print(annotated_path)
    author = annotated_path.parts[3]
    title = annotated_path.stem
    manually_checked = False
    line_text_list = original_text.split("\n")
    with open(annotated_path) as f:
        annotated_line_list = f.readlines()
        if len(line_text_list) != len(annotated_line_list):
            print(f"{annotated_path}")
            return None
        for i, annotated_line in enumerate(annotated_line_list):
            original_line_text = line_text_list[i]

            if annotated_line.endswith("*\n"):
                manually_checked = True
            annotated_line = annotated_line.replace("*", "")
            line_syllables = []
            line_numbers = []
            annotation_list = annotated_line.split()
            # print(annotated_line)
            if "/" in annotated_line:
                for part in annotation_list:
                    annotation = part.split("/")
                    line_syllables.append(annotation[0])
                    line_numbers.append(annotation[1])
            else:
                line_syllables = annotation_list
                # print(annotated_path)
                # print(rgx.findall(original_line_text))
                # print(line_syllables)
            metrical_numbers = "".join(line_numbers)
            metrical_pattern = re.sub(r"[34]", "", metrical_numbers)
            metrical_pattern = re.sub(r"0", "-",
                                      re.sub(r"1", "+", metrical_pattern))
            metrical_pattern = "".join(line_numbers).replace('1', '+').replace(
                '0', '-').replace('4', '').replace('3', '')
            line_length = len(annotation_list)
            rgx = re.compile("(\w[\w']*\w|\w)")
            word_list = []
            for word in rgx.findall(original_line_text):
                syllable_list = []
                syllables = "".join(syllable_list)
                palabra = word.lower().replace("'", "")
                while syllables != palabra and line_syllables:
                    # en las sílabas que hay liaison no estamos generando bien las sílabas de la palabra
                    syllable = line_syllables.pop(0)
                    syllable_list.append(syllable)
                    syllables = "".join(syllable_list)
                print(word, syllable_list)


def read_original_text(corpora_path, annotated_file_path):
    index = annotated_file_path.parts.index('Annotated_texts')
    new_path = Path('Original_texts').joinpath(*annotated_file_path.parts[index+1:])
    new_ext = ".txt"
    original_file_path = corpora_path / str(new_path).replace("".join(new_path.suffixes), new_ext)
    original_text = ""
    try:
        with open(original_file_path, "r")as f:
            original_text = f.read()
    except FileNotFoundError as fnf:
        print(f"{original_file_path} not found.")
    finally:
        return original_text


def get_features(path):
    """Function to find each poem file and parse it

    :param path: Corpus Path
    :return: List of poem dicts
    :rtype: list
    """
    annotated_path = path / "Annotated_texts"
    feature_list = []
    for filename in annotated_path.glob("**/*.csv"):
        original_text = read_original_text(path, filename)
        if len(original_text) > 0:
            result = parse_poem(filename, original_text)
            feature_list.append(result)
    return feature_list
