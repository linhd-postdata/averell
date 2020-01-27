import logging
import os
import urllib.request
from pathlib import Path
from zipfile import ZipFile

from tqdm import tqdm

from averell.core import CORPORA_SOURCES

DEFAULT_OUTPUT_FOLDER = Path.cwd() / "corpora"


def progress_bar(t):
    """ from https://gist.github.com/leimao/37ff6e990b3226c2c9670a2cd1e4a6f5
    Wraps tqdm instance.
    Don't forget to close() or __exit__() the tqdm instance once you're done
    (easiest using `with` syntax).
    Example:
        with tqdm(...) as t:
             reporthook = my_hook(t)
             urllib.urlretrieve(..., reporthook=reporthook)
    """
    last_b = [0]

    def update_to(b=1, bsize=1, tsize=None):
        """
        :param b: int, optional
            Number of blocks transferred so far [default: 1].
        :param bsize: int, optional
            Size of each block (in tqdm units) [default: 1].
        :param tsize: int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            t.total = tsize
        t.update((b - last_b[0]) * bsize)
        last_b[0] = b

    return update_to


def download_and_uncompress(url, save_dir):
    """
    :param url: URL of the corpus file
    :param save_dir: The folder where the corpus is going to be uncompressed
    """
    filename = url.split('/')[-1]
    with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
              desc=filename) as t:
        filename, _ = urllib.request.urlretrieve(url,
                                                 reporthook=progress_bar(t))
    with ZipFile(filename, 'r') as zipObj:
        zipObj.extractall(save_dir)
    os.remove(filename)


def already_downloaded(folder_name, output_folder):
    """

    """
    folder_path = Path(output_folder) / folder_name
    if folder_path.exists():
        return True
    else:
        return False


def download_corpora(corpus_indices=None,
                     output_folder=DEFAULT_OUTPUT_FOLDER):
    """
    Download corpus from a list of sources to a local folder
    :param corpus_indices: List with the indexes of CORPORA_SOURCES to choose
    which corpus is going to be downloaded
    :param output_folder: The folder where the corpus is going to be saved
    """
    if corpus_indices is not None:
        for index in tqdm(corpus_indices):
            if CORPORA_SOURCES.get(index):
                folder_name = CORPORA_SOURCES[index]["properties"]["folder_name"]
                if already_downloaded(folder_name, output_folder):
                    print(
                        f'Corpus {CORPORA_SOURCES[index]["name"]}'
                        f' already downloaded')
                    logging.info(
                        f'Corpus {CORPORA_SOURCES[index]["name"]}'
                        f' already downloaded')
                    continue
                else:
                    url = CORPORA_SOURCES[index]["properties"]["url"]
                    download_and_uncompress(url, output_folder)
            else:
                logging.error("Index number not in corpora list")
    else:
        logging.info("No corpus selected. Nothing will be downloaded")


def get_stanza_features(features):
    dict_lines = []
    for stanza_index, key in enumerate(features["stanzas"]):
        stanza_features = features['stanzas'][stanza_index]
        dic_final = {
            'stanza_number': stanza_features['stanza_number'],
            'manually_checked': features['manually_checked'],
            'title': features['title'],
            'author': features['author'],
            'stanza_text': stanza_features['stanza_text'],
            'stanza_type': stanza_features['stanza_type']
        }
        dict_lines.append(dic_final)
    return dict_lines


def get_line_features(features):
    stanza_features = get_stanza_features(features)
    lines_features = []
    for stanza_index, stanza in enumerate(stanza_features):
        key = features["stanzas"][stanza_index]
        for line in key["lines"]:
            line_features = {}
            if not line.get("words"):
                line_features.update(line)
            else:
                line_features['line_number'] = line['line_number']
                line_features['line_text'] = line['line_text']
                line_features['metrical_pattern'] = line['metrical_pattern']
            lines_features.append({**line_features, **stanza})
    return lines_features


def get_word_features(features):
    all_lines_features = get_line_features(features)
    all_words_features = []
    for stanza_index, stanza in enumerate(features["stanzas"]):
        line = stanza["lines"]
        for words in line:
            line_number = int(words["line_number"])
            for word in words["words"]:
                word_features = {"word_text": word["word_text"]}
                line_features = all_lines_features[line_number - 1]
                word_features.update(line_features)
                word_features.pop("stanza_text")
                all_words_features.append(word_features)
    return all_words_features


def get_syllable_features(features):
    all_words_features = get_word_features(features)
    all_syllable_features = []
    for stanza in features["stanzas"]:
        lines = stanza["lines"]
        for line_index, words in enumerate(lines):
            for word_index, word in enumerate(words["words"]):
                for syllable in word["syllables"]:
                    word_features = all_words_features[word_index]
                    line = lines[line_index]
                    syllable_features = {
                        "syllable": syllable,
                        "line_number": line["line_number"],
                        "metrical_pattern": line["metrical_pattern"],
                        "manually_checked": word_features["manually_checked"],
                        "title": word_features["title"],
                        "author": word_features["author"],
                        "stanza_type": word_features["stanza_type"],
                        "word_text": word_features["word_text"],
                        "line_text": line[line_index]["line_text"],
                        "stanza_number": word_features["stanza_number"]
                    }
                    all_syllable_features.append(syllable_features)
    return all_syllable_features


def filter_features(features, corpus_index, granularity=None):
    filtered_features = []
    granularities_list = CORPORA_SOURCES[corpus_index]["properties"]["granularity"]
    if granularity in granularities_list:
        if granularity == "stanza":
            filtered_features = get_stanza_features(features)
        elif granularity == "line":
            filtered_features = get_line_features(features)
        elif granularity == "word":
            filtered_features = get_word_features(features)
        elif granularity == "syllable":
            filtered_features = get_syllable_features(features)
        else:
            print(f"{granularity} not found on corpus properties")
    return filtered_features
