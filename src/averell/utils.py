import json
import logging
import os
import urllib.request
from pathlib import Path
from zipfile import ZipFile

import yaml
from tqdm import tqdm

BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
with open(BASE_DIR / 'corpora.yaml', 'r') as config_file:
    CORPORA_SOURCES = yaml.load(config_file, Loader=yaml.FullLoader)

DEFAULT_OUTPUT_FOLDER = Path.cwd() / "corpora"

TEI_NAMESPACE = "{http://www.tei-c.org/ns/1.0}"
XML_NS = "{http://www.w3.org/XML/1998/namespace}"


def progress_bar(t):
    """ from https://gist.github.com/leimao/37ff6e990b3226c2c9670a2cd1e4a6f5
    Wraps tqdm instance.
    Don't forget to close() or __exit__() the tqdm instance once you're done
    (easiest using `with` syntax).
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


def download_corpus(url):
    """Function to download the corpus zip file from external source

    :param url: string
        URL of the corpus file
    :return: string
        Local filename of the corpus
    """
    filename = url.split('/')[-1]
    with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
              desc=filename) as t:
        filename, *_ = urllib.request.urlretrieve(url,
                                                  reporthook=progress_bar(t))
    return filename


def uncompress_corpus(filename, save_dir):
    """Simple function to uncompress the corpus zip file

    :param filename: string
        The file that is going to be uncompressed
    :param save_dir: string
        The folder where the corpus is going to be uncompressed
    :return: string
        Filename of uncompressed corpus
    """""
    with ZipFile(filename, 'r') as zipObj:
        zipObj.extractall(save_dir)
    os.remove(filename)
    return filename


def download_corpora(corpus_indices=None,
                     output_folder=DEFAULT_OUTPUT_FOLDER):
    """Download corpus from a list of sources to a local folder

    :param corpus_indices: list
        List with the indexes of CORPORA_SOURCES to choose which corpus
        is going to be downloaded
    :param output_folder: string
        The folder where the corpus is going to be saved
    """
    folder_list = []
    if corpus_indices:
        for index in tqdm(corpus_indices):
            if index < 0:
                raise IndexError
            folder_name = CORPORA_SOURCES[index]["properties"][
                "folder_name"]
            folder_path = Path(output_folder) / folder_name
            if folder_path.exists():
                logging.info(f'Corpus {CORPORA_SOURCES[index]["name"]}'
                             f' already downloaded')
                continue
            else:
                url = CORPORA_SOURCES[index]["properties"]["url"]
                filename = download_corpus(url)
                folder_list.append(uncompress_corpus(
                    filename, output_folder))
    else:
        logging.error("No corpus selected. Nothing will be downloaded")
    return folder_list


def get_stanza_features(poem_features):
    """Filter the stanza features of a poem

    :param poem_features: dict
        Poem dictionary
    :return: dict list
        Stanzas dict list
    """
    stanza_list = []
    for stanza_index, key in enumerate(poem_features["stanzas"]):
        stanza_features = poem_features['stanzas'][stanza_index]
        dic_final = {
            'stanza_number': stanza_features['stanza_number'],
            'manually_checked': poem_features['manually_checked'],
            'poem_title': poem_features['poem_title'],
            'author': poem_features['author'],
            'stanza_text': stanza_features['stanza_text'],
            'stanza_type': stanza_features['stanza_type']
        }
        stanza_list.append(dic_final)
    return stanza_list


def get_line_features(features):
    """Filter the line features of a poem

    :param features: dict
        Poem dictionary
    :return: dict list
        Lines dict list
    """
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
    """Filter the word features of a poem

    :param features: dict
        Poem dictionary
    :return: dict list
        Words dict list
    """
    all_lines_features = get_line_features(features)
    all_words_features = []
    for stanza_index, stanza in enumerate(features["stanzas"]):
        lines = stanza["lines"]
        for line in lines:
            line_number = int(line["line_number"])
            for word in line["words"]:
                word_features = {"word_text": word["word_text"]}
                line_features = all_lines_features[line_number - 1]
                word_features.update(line_features)
                word_features.pop("stanza_text")
                all_words_features.append(word_features)
    return all_words_features


def get_syllable_features(features):
    """Filter the syllable features of a poem

    :param features: dict
        Poem dictionary
    :return: dict list
        Syllables dict list
    """
    all_words_features = get_word_features(features)
    all_syllable_features = []
    word_number = 0
    for stanza_index, stanza in enumerate(features["stanzas"]):
        lines = stanza["lines"]
        for line in lines:
            line_number = int(line["line_number"])
            words = line["words"]
            for word_index, word in enumerate(words):
                syllables = word["syllables"]
                for syllable in syllables:
                    syllable_features = {
                        "syllable": syllable,
                        "line_number": line_number,
                    }
                    word_features = all_words_features[word_number]
                    syllable_features.update(word_features)
                    all_syllable_features.append(syllable_features)
                word_number += 1
    return all_syllable_features


def filter_features(features, corpus_index, granularity=None):
    """Select the granularity

    :param features: dict
        Poem python dict
    :param corpus_index: int
        Corpus index to be filtered
    :param granularity: string
        Level to filter the poem (stanza, line, word or syllable)
    :return: list
        List of rows with the poem granularity info
    """
    filtered_features = []
    granularities_list = CORPORA_SOURCES[corpus_index]["properties"][
        "granularity"]
    if granularity in granularities_list:
        if granularity == "stanza":
            filtered_features = get_stanza_features(features)
        elif granularity == "line":
            filtered_features = get_line_features(features)
        elif granularity == "word":
            filtered_features = get_word_features(features)
        elif granularity == "syllable":
            filtered_features = get_syllable_features(features)
    return filtered_features


def filter_corpus_features(corpus_features, corpus_id, granularity):
    """Get the granularity features for each poem in corpus

    :param corpus_features: list of dicts
        List of corpus poems python dicts
    :param corpus_id: int
        Corpus id to be filtered
    :param granularity: string
        Level to filter the poem (stanza, line, word or syllable)
    :return: list
        List of rows with the corpus granularity info
    """
    corpus_filtered_features = []
    for poem_features in corpus_features:
        poem_filtered_features = filter_features(poem_features, corpus_id,
                                                 granularity)
        corpus_filtered_features.extend(poem_filtered_features)
    return corpus_filtered_features


def write_json(poem_dict, filename):
    """Simple function to save data in json format

    :param poem_dict: dict
        Python dict with poem data
    :param filename: string
        JSON filename that will be written with the poem data
    """
    file_path = Path(filename)
    if os.path.exists(f"{filename}.json"):
        file_count = len(list(file_path.parent.glob(f"{file_path.stem}*.json")))
        filename = f"{filename}{file_count + 1}"
    with open(filename + ".json", 'w', encoding='utf-8') as f:
        json.dump(poem_dict, f, ensure_ascii=False, indent=4)


def read_features(corpus_folder):
    """Read the dictionary of each poem in "corpus_folder" and
    return the list of python dictionaries

    :param corpus_folder: Local folder where the corpus is located
    :return: List of python dictionaries with the poems features
    """
    features_path = Path.cwd() / Path(corpus_folder) / "averell" / "parser"
    features = []
    for json_file in features_path.rglob("*.json"):
        features.append(json.loads(json_file.read_text()))

    features = sorted(features, key=lambda i: i['poem_title'])
    return features


def pretty_string(text, num_words):
    """Add a line break every number of words into a text to create multiline
    cells to use in :py:func:`~averell.utils.get_main_corpora_info`

    :param text: String to be split
    :param num_words: Number of words to add a line break after
    :return: String with line break every number of words entered
    :rtype: str
    """
    words = text.split()
    grouped_words = [' '.join(words[i: i + num_words]) for i in
                     range(0, len(words), num_words)]
    return '\n'.join(grouped_words)


def get_main_corpora_info():
    """Create dict with the main corpora info saved in CORPORA_SOURCES

    :return: Dictionary with the corpora info to be shown
    :rtype: dict
    """
    table = []
    for corpus_info in CORPORA_SOURCES:
        corpus_id = CORPORA_SOURCES.index(corpus_info) + 1
        props = corpus_info["properties"]
        table.append({
            "id": corpus_id,
            "name": pretty_string(corpus_info["name"], 2),
            "size": props["size"],
            "docs": props["doc_quantity"],
            "words": props["word_quantity"],
            "granularity": pretty_string('\n'.join(props["granularity"]), 1),
            "license": pretty_string(props["license"], 1),
        })
    return table
