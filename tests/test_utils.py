import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from averell.utils import download_corpora
from averell.utils import download_corpus
from averell.utils import filter_corpus_features
from averell.utils import filter_features
from averell.utils import get_ids
from averell.utils import get_line_features
from averell.utils import get_stanza_features
from averell.utils import get_syllable_features
from averell.utils import get_word_features
from averell.utils import pretty_string
from averell.utils import read_features
from averell.utils import write_json

_corpora_sources = [
    {'name': 'testing',
     'properties':
         {
             'license': 'CC-BY',
             'size': '22M',
             'language': 'es',
             'doc_quantity': 4088,
             'word_quantity': 381539,
             'granularity': ['stanza'],
             'slug': 't1'
         }
     },
    {'name': 'testing2',
     'properties':
         {
             'license': 'CC-BY',
             'size': '22M',
             'language': 'fr',
             'doc_quantity': 4088,
             'word_quantity': 381539,
             'granularity': ['stanza'],
             'slug': 't2'
         }
     }
]

TESTS_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
FIXTURES_DIR = TESTS_DIR / "fixtures"


@pytest.fixture
def zip_test():
    return str(Path.cwd() / "tests" / "fixtures" / "test.zip")


@pytest.fixture
def stanza_features():
    return json.loads((FIXTURES_DIR / "stanza_features.json").read_text())


@pytest.fixture
def line_features():
    return json.loads((FIXTURES_DIR / "line_features.json").read_text())


@pytest.fixture
def word_features():
    return json.loads((FIXTURES_DIR / "word_features.json").read_text())


@pytest.fixture
def syllable_features():
    return json.loads((FIXTURES_DIR / "syllable_features.json").read_text())


@pytest.fixture
def sdo():
    return json.loads((FIXTURES_DIR / "sdo.json").read_text())


@pytest.fixture
def plsdo():
    return json.loads((FIXTURES_DIR / "plsdo.json").read_text())


@patch('urllib.request.urlretrieve')
def test_download_corpus(mock_request):
    url = "https://github.com/pruizf/disco/archive/master.zip"
    mock_request.return_value = "master.zip", None
    assert "master.zip" == download_corpus(url)


def test_download_corpora_no_indices():
    assert download_corpora([]) == []


def test_download_corpora_index_not_in_range():
    try:
        download_corpora([-3])
    except IndexError:
        assert True
    else:
        assert False


@patch('averell.utils.Path.exists')
def test_download_corpora_already_downloaded(mock_exists):
    mock_exists.return_value = True
    assert [] == download_corpora([1])


def test_download_corpora():
    assert True


def test_get_stanza_features(stanza_features, sdo):
    assert get_stanza_features(sdo) == stanza_features


def test_get_line_features(line_features):
    features = json.loads((FIXTURES_DIR / "sdo.json").read_text())
    assert get_line_features(features) == line_features


def test_get_word_features(word_features):
    features = json.loads((FIXTURES_DIR / "plsdo.json").read_text())
    assert get_word_features(features) == word_features


def test_get_syllable_features(syllable_features):
    features = json.loads((FIXTURES_DIR / "plsdo.json").read_text())
    assert get_syllable_features(features) == syllable_features


def test_filter_features_granularity_not_in_list():
    output = []
    granularity = "gjasdh"
    assert output == filter_features([], 4, granularity)


def test_filter_features_granularity_stanza(sdo, stanza_features):
    granularity = "stanza"
    assert filter_features(sdo, 2, granularity) == stanza_features


def test_filter_features_granularity_line(sdo, line_features):
    granularity = "line"
    assert filter_features(sdo, 2, granularity) == line_features


def test_filter_features_granularity_word(plsdo, word_features):
    granularity = "word"
    assert filter_features(plsdo, 4, granularity) == word_features


def test_filter_features_granularity_syllable(plsdo, syllable_features):
    granularity = "syllable"
    output = filter_features(plsdo, 4, granularity)
    assert output == syllable_features


@pytest.fixture
def corpora_features():
    return json.loads((FIXTURES_DIR / "corpora_features.json").read_text())


@patch("averell.utils.filter_features", return_value=[])
def test_filter_corpus_features(mock_filter, corpora_features):
    granularity = "line"
    output = filter_corpus_features(corpora_features, 1, granularity)
    assert output == []
    assert mock_filter.called


def test_read_features(corpora_features):
    output = read_features(Path("tests") / "fixtures")
    assert output == corpora_features


def test_pretty_string():
    output = "This is\na split\nstring"
    assert output == pretty_string("This is a split string", 2)


@patch('averell.utils.CORPORA_SOURCES', _corpora_sources)
def test_get_ids():
    assert get_ids(["all"]) == [0, 1]
    assert get_ids(["1", "t2"]) == [0, 1]
    assert get_ids(["es"]) == [0]


@patch("builtins.open")
@patch("json.dump", return_value=True)
def test_write_json(mock_open, mock_dump, sdo):
    write_json(sdo, "sdo.json")
    assert mock_open.called
    assert mock_dump.called
