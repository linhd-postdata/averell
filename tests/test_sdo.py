import json
from unittest.mock import patch

import pytest

from averell.readers.sdo import get_features
from averell.readers.sdo import parse_xml
from tests.test_utils import TESTS_DIR


@pytest.fixture
def sdo():
    path = TESTS_DIR / "fixtures" / "sdo.json"
    return json.loads(path.read_text())


def test_parse_xml(sdo):
    path = TESTS_DIR / "fixtures" / "input_sdo.xml"
    poem = parse_xml(str(path))
    assert poem == sdo


@patch('averell.readers.sdo.parse_xml')
def test_get_features(mock_parse_xml):
    path = TESTS_DIR / "fixtures" / "test"
    mock_parse_xml.return_value = {}
    assert [{}] == get_features(path)
