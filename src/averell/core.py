import importlib
from pathlib import Path

import yaml

from averell.utils import download_corpora
from averell.utils import filter_features

DEFAULT_OUTPUT_FOLDER = Path.cwd() / "corpora"

CORPORA_SOURCES = yaml.load("corpora.yaml", Loader=yaml.FullLoader)


def get_corpora(corpus_indices=None, granularity=None,
                output_folder=DEFAULT_OUTPUT_FOLDER):
    """

    """
    download_corpora(corpus_indices, output_folder)
    corpora_features = []
    for index in corpus_indices:
        folder_name = CORPORA_SOURCES[index]["properties"]['folder_name']
        get_features = getattr(importlib.import_module(
            CORPORA_SOURCES[index]["properties"]["reader"]), "get_features")
        features = get_features(Path(output_folder) / folder_name)
        if granularity is not None:
            features = filter_features(features, index, granularity)
        corpora_features.append(features)
    return corpora_features
