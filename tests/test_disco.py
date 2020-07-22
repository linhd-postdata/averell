import json
from unittest.mock import patch

import pytest

from averell.readers.disco import get_features
from averell.readers.disco import parse_xml
from tests.test_utils import TESTS_DIR


@pytest.fixture
def disco():
    path = TESTS_DIR / "fixtures" / "disco.json"
    return json.loads(path.read_text())


def test_parse_xml(disco):
    path = TESTS_DIR / "fixtures" / "input_disco.xml"
    poem = parse_xml(str(path))
    assert poem == disco


@patch('averell.readers.disco.parse_xml')
def test_get_features(mock_parse_xml):
    path = TESTS_DIR / "fixtures" / "test"
    mock_parse_xml.return_value = {}
    assert [{}] == get_features(path)
