import json
from unittest.mock import patch

import pytest

from averell.readers.bibliotecaitaliana import get_features
from averell.readers.bibliotecaitaliana import parse_json
from tests.test_utils import TESTS_DIR

BIBIT_PATH = TESTS_DIR / "fixtures" / "bibit"


@pytest.fixture
def biblitaliana():
    path = TESTS_DIR / "fixtures" / "bibliotecaitaliana.json"
    return json.loads(path.read_text())


def test_parse_xml(biblitaliana):
    path = BIBIT_PATH / "input_bibliotecaitaliana.json"
    result = parse_json(path)
    assert list(result) == biblitaliana


@patch('averell.readers.bibliotecaitaliana.parse_json', return_value={})
@patch('averell.readers.bibliotecaitaliana.uncompress_corpus')
def test_get_features(mock_parse_json, mock_uncompress):
    assert [] == get_features(BIBIT_PATH)
    assert mock_parse_json.called
