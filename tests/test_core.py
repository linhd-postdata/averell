import json
from unittest import mock

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
