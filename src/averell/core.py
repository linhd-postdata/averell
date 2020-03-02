import importlib
import logging
import os
from pathlib import Path

from .utils import CORPORA_SOURCES
from .utils import download_corpora
from .utils import filter_features
from .utils import write_json

DEFAULT_OUTPUT_FOLDER = Path.cwd() / "corpora"


def get_corpora(corpus_indices=None, granularity=None,
                output_folder=DEFAULT_OUTPUT_FOLDER):
    """
    Download and uncompress selected corpora
    :param corpus_indices: Indices of the corpus that will be downloaded
    :param granularity: Level of the corpus that will be parsered
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
                author_path = gen_path / "parser" / poem["author"].replace(" ",
                                                                           "")
                if not author_path.exists():
                    os.makedirs(author_path)
                write_json(poem, str(
                    author_path / poem["poem_title"].title().replace(" ", "")))
            if granularity is not None:
                granularities_list = CORPORA_SOURCES[index]["properties"][
                    "granularity"]
                if granularity in granularities_list:
                    for poem in features:
                        filtered_features = filter_features(poem, index,
                                                            granularity)
                        granularity_path = gen_path / granularity / poem[
                            "author"].replace(" ", "")
                        if filtered_features:
                            if not granularity_path.exists():
                                os.makedirs(granularity_path)
                            write_json(filtered_features, str(
                                granularity_path / poem[
                                    "poem_title"].title().replace(" ", "")))
                            corpora_features.append(filtered_features)
                else:
                    corpus_name = CORPORA_SOURCES[index]["name"]
                    logging.error(
                        f"'{granularity}' granularity not found on "
                        f"'{corpus_name}' properties")
            else:
                corpora_features.append(features)
    except IndexError:
        logging.error("Index number not in corpora list")
    finally:
        return corpora_features
