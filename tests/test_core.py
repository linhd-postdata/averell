import json
import logging
import tempfile
from unittest import mock

import pytest

from averell.core import export_corpora
from averell.core import get_corpora

from .test_utils import FIXTURES_DIR
from .test_utils import _corpora_sources


def test_get_corpora_index_not_in_range(caplog):
    corpus_indices = [500000]
    assert [] == get_corpora(corpus_indices)
    assert "Index number not in corpora list" in caplog.text


@mock.patch('averell.core.download_corpora')
def test_get_corpora(mock_download_corpora, caplog):
    mock_download_corpora.return_value = ["disco3.zip"]
    assert [[]] == get_corpora([1], output_folder=tempfile.mkdtemp())
    with caplog.at_level(logging.INFO):
        assert "Downloaded Disco V3 corpus" in caplog.text


@pytest.fixture
def corpus_features():
    return json.loads((FIXTURES_DIR / "corpora_stanza.json").read_text())


def test_export_corpora_folder_not_exists(caplog):
    assert [] == export_corpora([2, 3], "line", "kgalsjlkjsadfhk", "line", True)[0]
    assert "Corpora folder not found" in caplog.text


def test_export_corpora_granularity_none(caplog):
    assert [] == export_corpora([2, 3], None, FIXTURES_DIR, "foo")[0]
    assert "No GRANULARITY selected" in caplog.text


def test_export_corpora_no_ids(caplog):
    assert [] == export_corpora([], "line", FIXTURES_DIR, "foo")[0]
    assert "No CORPUS ID selected" in caplog.text


def test_export_corpora_id_not_in_list(caplog):
    assert [] == export_corpora([500000], "line", FIXTURES_DIR, "foo")[0]
    assert "ID not in corpora list" in caplog.text


@mock.patch('averell.core.CORPORA_SOURCES', _corpora_sources)
def test_export_corpora_id_not_downloaded(caplog):
    assert [] == export_corpora([1], "stanza", FIXTURES_DIR, "foo", True)[0]
    message = f'"testing2 (t2)" not found in "{FIXTURES_DIR}" folder'
    assert message in caplog.text


@mock.patch('averell.core.download_corpora')
@mock.patch('averell.core.CORPORA_SOURCES', _corpora_sources)
def test_export_corpora_granularity_not_in_list(mock_download, caplog):
    mock_download.return_value = []
    granularity = "kfajdgah"
    assert [] == export_corpora([0], granularity, FIXTURES_DIR, "foo")[0]
    assert f"'{granularity}' granularity not found on 'testing' properties" in caplog.text


def test_export_corpora_filename(caplog):
    assert "foo" == export_corpora([], "line", FIXTURES_DIR, "foo")[1]
