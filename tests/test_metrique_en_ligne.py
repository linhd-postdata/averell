import json
from unittest.mock import patch

import pytest

from averell.readers.metriqueenligne import get_features
from averell.readers.metriqueenligne import parse_json
from tests.test_utils import TESTS_DIR

MEL_PATH = TESTS_DIR / "fixtures" / "mel"


@pytest.fixture
def metriqueenligne():
    path = TESTS_DIR / "fixtures" / "metrique_en_ligne.json"
    return json.loads(path.read_text())


def test_parse_json(metriqueenligne):
    path = (MEL_PATH / "metrique-en-ligne-master" /
            "input_metrique_en_ligne.json")
    result = parse_json(path)
    assert list(result) == metriqueenligne


@patch('averell.readers.metriqueenligne.parse_json', return_value={})
def test_get_features(mock_parse_json):
    assert [] == get_features(MEL_PATH)
    assert mock_parse_json.called
