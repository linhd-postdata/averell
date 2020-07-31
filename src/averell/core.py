import importlib
import logging
import os
from pathlib import Path

from slugify import slugify

from .utils import CORPORA_SOURCES
from .utils import download_corpora
from .utils import filter_corpus_features
from .utils import read_features
from .utils import write_json

DEFAULT_OUTPUT_FOLDER = Path.cwd() / "corpora"
logging.getLogger().setLevel(logging.INFO)


def get_corpora(corpus_indices=None, output_folder=DEFAULT_OUTPUT_FOLDER):
    """Download and uncompress selected corpora

    :param corpus_indices: Indices of the corpus that will be downloaded
    :param output_folder: Local folder where the corpus is going to be
        uncompressed
    :return: Python dict with all corpora features
    """
    corpora_features = []
    try:
        download_corpora(corpus_indices, output_folder)
        for index in corpus_indices:
            folder_name = CORPORA_SOURCES[index]["properties"]['folder_name']
            gen_path = Path(output_folder) / folder_name / "averell"
            get_features = getattr(importlib.import_module(
                CORPORA_SOURCES[index]["properties"]["reader"]), "get_features")
            features = get_features(Path(output_folder) / folder_name)
            for poem in features:
                # max_length=30 to avoid "too long file name" error
                author = slugify(poem["author"], max_length=30)
                author_path = gen_path / "parser" / author
                if not author_path.exists():
                    os.makedirs(author_path)
                write_json(poem, str(
                    author_path / slugify(poem["poem_title"], max_length=30)))
            corpora_features.append(features)
            logging.info(f"Downloaded {CORPORA_SOURCES[index]['name']} corpus")
    except IndexError:
        logging.error("Index number not in corpora list")
    finally:
        return corpora_features


def export_corpora(corpus_ids, granularity, corpora_folder, filename):
    """
    Generates a single JSON file with the chosen granularity for all of the
        selected corpora

    :param corpus_ids: IDs of the corpora that will be exported
    :param granularity: Level of parsing granularity
    :param corpora_folder: Local folder where the corpora is located
    :param filename: Name of the output file
    :return: Python dict with the chosen granularity for all of the selected
        corpora
    """
    corpora_features = []
    if Path(corpora_folder).exists():
        if not corpus_ids:
            logging.error("No CORPUS ID selected")
        else:
            if granularity is not None:
                for index in corpus_ids:
                    corpus_id = index - 1
                    try:
                        corpus = CORPORA_SOURCES[corpus_id]
                    except IndexError:
                        logging.error("ID not in corpora list")
                    else:
                        corpus_folder = corpus["properties"]["folder_name"]
                        corpus_name = corpus["name"]
                        if not (Path(corpora_folder) / corpus_folder).exists():
                            logging.error(f'"{corpus_name}" not found in '
                                          f'"{corpora_folder}" folder')
                            continue
                        granularities_list = corpus["properties"]["granularity"]
                        if granularity not in granularities_list:
                            logging.error(
                                f"'{granularity}' granularity not found on "
                                f"'{corpus_name}' properties")
                            continue
                        features = read_features(
                            Path(corpora_folder) / corpus_folder)
                        filtered_features = filter_corpus_features(features,
                                                                   corpus_id,
                                                                   granularity)
                        corpora_features.extend(filtered_features)
            else:
                logging.error("No GRANULARITY selected")
        if corpora_features:
            export_filename = filename
            if not filename:
                export_filename = granularity
            write_json(corpora_features,
                       str(Path(corpora_folder) / export_filename))
    else:
        logging.error("Corpora folder not found")
    return corpora_features
