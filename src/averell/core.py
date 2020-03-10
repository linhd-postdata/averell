import importlib
import logging
import os
from pathlib import Path

from .utils import CORPORA_SOURCES
from .utils import download_corpora
from .utils import filter_corpus_features
from .utils import read_features
from .utils import write_json

DEFAULT_OUTPUT_FOLDER = Path.cwd() / "corpora"
logging.getLogger().setLevel(logging.INFO)


def get_corpora(corpus_indices=None, output_folder=DEFAULT_OUTPUT_FOLDER):
    """
    Download and uncompress selected corpora
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
                author = poem["author"].replace(" ", "")
                author_path = gen_path / "parser" / author
                if not author_path.exists():
                    os.makedirs(author_path)
                write_json(poem, str(
                    author_path / poem["poem_title"].title().replace(" ", "")))
            else:
                corpora_features.append(features)
    except IndexError:
        logging.error("Index number not in corpora list")
    finally:
        return corpora_features


def export_corpora(corpus_ids, granularity, corpora_folder):
    """
    Generates a single JSON file with the chosen granularity for all of the
    selected corpora
    :param corpus_ids: IDs of the corpora that will be exported
    :param granularity: Level of parsing granularity
    :param corpora_folder: Local folder where the corpora is located
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
                        corpus_folder = CORPORA_SOURCES[corpus_id][
                            "properties"]["folder_name"]
                    except IndexError:
                        logging.error("ID not in corpora list")
                    else:
                        if not (Path(corpora_folder) / corpus_folder).exists():
                            logging.error(
                                f'{CORPORA_SOURCES[corpus_id]["name"]}'
                                f' not downloaded')
                            continue
                        granularities_list = CORPORA_SOURCES[corpus_id][
                            "properties"]["granularity"]
                        if granularity not in granularities_list:
                            corpus_name = CORPORA_SOURCES[corpus_id]["name"]
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
            write_json(corpora_features,
                       str(Path(corpora_folder) / granularity))
    else:
        logging.error("Corpora folder not found")
    return corpora_features
