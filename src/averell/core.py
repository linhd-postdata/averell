import importlib
import yaml
from pathlib import Path

from averell.utils import download_corpora
from averell.utils import filter_features

DEFAULT_OUTPUT_FOLDER = Path.cwd() / "corpora"

CORPORA_SOURCES = [
    {
        'name': 'Disco V2',
        'properties': {
            'annotation_type': None,
            'folder_name': 'disco-master',
            'license': 'CC-BY',
            'reader': 'averell.readers.disco',
            'url': 'https://github.com/pruizf/disco/archive/master.zip',
            'size': '22M',
            'doc_quantity': 4088,
            'word_quantity': 381539,
            'granularity': ['stanza', 'line']
        }
    },
    {
        'name': 'Disco V3',
        'properties': {
            'folder_name': 'disco-3',
            'license': 'CC-BY',
            'reader': 'averell.readers.disco3',
            'url': 'https://github.com/pruizf/disco/archive/v3.zip',
            'size': '28M',
            'doc_quantity': 4080,
            'word_quantity': 377978,
            'granularity': ['stanza', 'line']
        }
    },
    {
        'name': 'Sonetos Siglo de Oro',
        'properties': {
            'folder_name': 'CorpusSonetosSigloDeOro-master',
            'license': 'CC-BY-NC 4.0',
            'reader': 'averell.readers.sdo',
            'url': 'https://github.com/bncolorado/CorpusSonetosSigloDeOro/archive/master.zip',
            'size': '6.8M',
            'doc_quantity': 5078,
            'word_quantity': 466012,
            'granularity': ['stanza', 'line']
        }
    },
    {
        'name': 'ADSO 100 poems corpus',
        'properties': {
            'folder_name': 'gold',
            'license': 'CC-BY-NC 4.0',
            'reader': 'averell.readers.goldpoems',
            'url': 'https://github.com/linhd-postdata/adsoScansionSystem/releases/download/1.0.0/ADSO_gold_standard_100poems.zip',
            'size': '128K',
            'doc_quantity': 100,
            'word_quantity': '------',
            'granularity': ['stanza', 'line']
        }
    },
    {
        'name': 'Poesía Lírica Castellana Siglo de Oro',
        'properties': {
            'folder_name': 'CorpusGeneralPoesiaLiricaCastellanaDelSigloDeOro-master',
            'license': 'Unspecified',
            'reader': 'averell.readers.plsdo',
            'url': 'https://github.com/bncolorado/CorpusGeneralPoesiaLiricaCastellanaDelSigloDeOro/archive/master.zip',
            'size': '3.8M',
            'doc_quantity': 475,
            'word_quantity': 299402,
            'granularity': ['stanza', 'line', 'word', 'syllable']
        }
    },
    {
        'name': 'Dracor Calderón',
        'properties': {
            'folder_name': 'caldracor-master',
            'license': 'CC0',
            'reader': 'averell.readers.dracor',
            'url': 'https://github.com/dracor-org/caldracor/archive/master.zip',
            'size': '1.7M',
            'doc_quantity': 55,
            'word_quantity': 514115,
            'granularity': ['stanza', 'line']
        }
    }]


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
