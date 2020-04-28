import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from averell.utils import download_corpora
from averell.utils import download_corpus
from averell.utils import filter_corpus_features
from averell.utils import filter_features
from averell.utils import get_line_features
from averell.utils import get_stanza_features
from averell.utils import get_syllable_features
from averell.utils import get_word_features
from averell.utils import pretty_string
from averell.utils import read_features

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


def test_get_stanza_features(stanza_features):
    features = json.loads((FIXTURES_DIR / "sdo.json").read_text())
    assert get_stanza_features(features) == stanza_features


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
def corpus_line():
    return json.loads((FIXTURES_DIR / "corpus_line.json").read_text())


@pytest.fixture
def corpus_features():
    return json.loads((FIXTURES_DIR / "corpus_features.json").read_text())


def test_filter_corpus_features(corpus_line, corpus_features):
    granularity = "line"
    features = corpus_features
    output = filter_corpus_features(features, 2, granularity)
    assert output == corpus_line


@pytest.fixture
def corpora_features():
    return json.loads((FIXTURES_DIR / "corpora_features.json").read_text())


def test_read_features(corpora_features):
    output = read_features(Path("tests") / "fixtures")
    assert output == corpora_features


def test_pretty_string():
    output = "This is\na split\nstring"
    assert output == pretty_string("This is a split string", 2)
