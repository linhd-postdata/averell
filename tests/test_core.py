import json
import logging
from unittest import mock

import pytest

from averell.core import export_corpora
from averell.core import get_corpora
from tests.test_utils import FIXTURES_DIR


def test_get_corpora_index_not_in_range(caplog):
    corpus_indices = [500000]
    assert [] == get_corpora(corpus_indices)
    assert "Index number not in corpora list" in caplog.text


@mock.patch('averell.core.download_corpora')
def test_get_corpora(mock_download_corpora, caplog):
    mock_download_corpora.return_value = ["disco3.zip"]
    assert [[]] == get_corpora([1])
    with caplog.at_level(logging.INFO):
        assert "Downloaded Disco V3 corpus" in caplog.text


@pytest.fixture
def corpus_features():
    return json.loads((FIXTURES_DIR / "corpora_stanza.json").read_text())


def test_export_corpora_folder_not_exists(caplog):
    assert [] == export_corpora([2, 3], "line", "kgalsjlkjsadfhk", "line")
    assert "Corpora folder not found" in caplog.text


def test_export_corpora_granularity_none(caplog):
    assert [] == export_corpora([2, 3], None, FIXTURES_DIR, "foo")
    assert "No GRANULARITY selected" in caplog.text


def test_export_corpora_no_ids(caplog):
    assert [] == export_corpora([], "line", FIXTURES_DIR, "foo")
    assert "No CORPUS ID selected" in caplog.text


def test_export_corpora_id_not_in_list(caplog):
    assert [] == export_corpora([500000], "line", FIXTURES_DIR, "foo")
    assert "ID not in corpora list" in caplog.text


_corpora_sources = [
    {'name': 'testing',
     'properties':
         {
             'license': 'CC-BY',
             'size': '22M',
             'doc_quantity': 4088,
             'word_quantity': 381539,
             'granularity': ['stanza'],
             'folder_name': 'averell'
         }
     },
    {'name': 'testing2',
     'properties':
         {
             'license': 'CC-BY',
             'size': '22M',
             'doc_quantity': 4088,
             'word_quantity': 381539,
             'granularity': ['stanza'],
             'folder_name': 'not-folder'
         }
     }
]


@mock.patch('averell.core.CORPORA_SOURCES', _corpora_sources)
def test_export_corpora_id_not_downloaded(caplog):
    assert [] == export_corpora([2], "stanza", FIXTURES_DIR, "foo")
    assert f'"testing2" not found in "{FIXTURES_DIR}" folder' in caplog.text


@mock.patch('averell.core.CORPORA_SOURCES', _corpora_sources)
def test_export_corpora_granularity_not_in_list(caplog):
    granularity = "kfajdgah"
    assert [] == export_corpora([1], granularity, FIXTURES_DIR, "foo")
    assert f"'{granularity}' granularity not found on 'testing' properties" in caplog.text
