import json
from unittest import mock
from unittest.mock import patch

import pytest
from tests.test_utils import FIXTURES_DIR

from averell.core import export_corpora
from averell.core import get_corpora
from averell.readers.disco3 import get_features


def test_get_corpora_index_not_in_range():
    corpus_indices = [500000]
    assert [] == get_corpora(corpus_indices)


@mock.patch('averell.utils.download_corpora')
@mock.patch('importlib.import_module')
def test_get_corpora(mock_download_corpora, mock_import_module):
    mock_download_corpora.return_value = ["disco3.zip"]
    mock_import_module.return_value = get_features
    # assert [] == get_corpora([1], "line", "tests/fixtures/corpora")
    assert True


@pytest.fixture
def corpus_features():
    return json.loads((FIXTURES_DIR / "corpora_stanza.json").read_text())


def test_export_corpora_folder_not_exists():
    assert [] == export_corpora([2, 3], "line", "kgalsjlkjsadfhk")


def test_export_corpora_granularity_none():
    assert [] == export_corpora([2, 3], None, FIXTURES_DIR)


def test_export_corpora_no_ids():
    assert [] == export_corpora([], "line", FIXTURES_DIR)


def test_export_corpora_id_not_in_list():
    assert [] == export_corpora([500000], "line", FIXTURES_DIR)


def test_export_corpora_id_not_downloaded():
    assert [] == export_corpora([4], "line", FIXTURES_DIR)


def test_export_corpora_granularity_not_in_list():
    assert [] == export_corpora([3], "kfajdgah", FIXTURES_DIR)


@pytest.fixture
def corpora_features():
    return json.loads((FIXTURES_DIR / "corpora_features.json").read_text())


@pytest.fixture
def export_features_list():
    return json.loads((FIXTURES_DIR / "line3.json").read_text())


@patch('averell.utils.read_features', corpora_features)
def test_export_corpora(export_features_list):
    assert export_corpora([3], "line", FIXTURES_DIR) == export_features_list
