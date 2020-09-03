import json
from unittest.mock import patch

import pytest

from averell.readers.goldpoems import get_features
from averell.readers.goldpoems import parse_xml
from tests.test_utils import TESTS_DIR


@pytest.fixture
def goldpoems():
    path = TESTS_DIR / "fixtures" / "goldpoems.json"
    return json.loads(path.read_text())


def test_parse_xml(goldpoems):
    path = TESTS_DIR / "fixtures" / "input_goldpoems.xml"
    poem = parse_xml(str(path))
    assert poem == goldpoems


@patch('averell.readers.goldpoems.parse_xml')
def test_get_features(mock_parse_xml):
    path = TESTS_DIR / "fixtures" / "test"
    mock_parse_xml.return_value = {}
    assert [{}] == get_features(path)
