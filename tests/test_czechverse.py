import json
from unittest.mock import patch

import pytest

from averell.readers.czechverse import get_features
from averell.readers.czechverse import parse_json
from tests.test_utils import TESTS_DIR

CZVERSE_PATH = TESTS_DIR / "fixtures" / "czverse"


@pytest.fixture
def czverse():
    path = TESTS_DIR / "fixtures" / "czverse.json"
    return json.loads(path.read_text())


def test_parse_json(czverse):
    path = CZVERSE_PATH / "corpusCzechVerse-master" / "ccv" / "input_czverse.json"
    result = parse_json(path)
    assert list(result) == czverse


@patch('averell.readers.czechverse.parse_json', return_value={})
def test_get_features(mock_parse_json):
    assert [] == get_features(CZVERSE_PATH)
    assert mock_parse_json.called
