import json
from unittest.mock import patch

import pytest

from averell.readers.gongocorpus import get_features
from averell.readers.gongocorpus import parse_json
from tests.test_utils import TESTS_DIR

GONGO_PATH = TESTS_DIR / "fixtures" / "gongo"


@pytest.fixture
def gongocorpus():
    path = TESTS_DIR / "fixtures" / "gongocorpus.json"
    return json.loads(path.read_text())


def test_parse_json(gongocorpus):
    path = (GONGO_PATH / "gongocorpus-master" /
            "corpus_json" / "segura" / "input_gongocorpus.json")
    poem = parse_json(path)
    assert poem == gongocorpus


@patch('averell.readers.gongocorpus.parse_json')
def test_get_features(mock_parse_json):
    path = GONGO_PATH
    mock_parse_json.return_value = {}
    assert [{}] == get_features(path)
    assert mock_parse_json.called
