import json
from pathlib import Path
from unittest.mock import patch

import pytest
from tests.test_utils import TESTS_DIR

from averell.readers.disco3 import get_features
from averell.readers.disco3 import parse_xml


@pytest.fixture
def disco3():
    return json.loads(Path("tests/fixtures/disco3.json").read_text())


def test_parse_xml(disco3):
    poem = parse_xml("tests/fixtures/input_disco3.xml")
    assert poem == disco3


@patch('averell.readers.disco3.parse_xml')
def test_get_features(mock_parse_xml):
    path = TESTS_DIR / "fixtures" / "test"
    mock_parse_xml.return_value = {}
    assert [{}] == get_features(path)
