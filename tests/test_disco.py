import json
from pathlib import Path
from unittest.mock import patch

import pytest
from tests.test_utils import TESTS_DIR

from averell.readers.disco import get_features
from averell.readers.disco import parse_xml


@pytest.fixture
def disco():
    return json.loads(Path("tests/fixtures/disco.json").read_text())


def test_parse_xml(disco):
    poem = parse_xml("tests/fixtures/input_disco.xml")
    assert poem == disco


@patch('averell.readers.disco.parse_xml')
def test_get_features(mock_parse_xml):
    path = TESTS_DIR / "fixtures" / "test"
    mock_parse_xml.return_value = {}
    assert [{}] == get_features(path)
