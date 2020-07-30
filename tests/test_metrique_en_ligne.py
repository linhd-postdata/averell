import json
from unittest.mock import patch

import pytest

from averell.readers.metriqueenligne import get_features
from averell.readers.metriqueenligne import parse_json
from tests.test_utils import TESTS_DIR


@pytest.fixture
def metriqueenligne():
    path = TESTS_DIR / "fixtures" / "metrique_en_ligne.json"
    return json.loads(path.read_text())


def test_parse_json(metriqueenligne):
    path = TESTS_DIR / "fixtures" / "input_metrique_en_ligne.json"
    result = parse_json(path)
    assert list(result) == metriqueenligne


@patch('averell.readers.metriqueenligne.parse_json')
def test_get_features(mock_parse_json):
    path = TESTS_DIR / "fixtures" / "test"
    mock_parse_json.return_value = {}
    assert [] == get_features(path)
