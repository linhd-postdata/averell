import json
from pathlib import Path
from unittest.mock import patch

import pytest
from tests.test_utils import TESTS_DIR

from averell.readers.goldpoems import get_features
from averell.readers.goldpoems import parse_xml


@pytest.fixture
def goldpoems():
    return json.loads(Path("tests/fixtures/goldpoems.json").read_text())


def test_parse_xml(goldpoems):
    poem = parse_xml("tests/fixtures/input_goldpoems.xml")
    assert poem == goldpoems


@patch('averell.readers.goldpoems.parse_xml')
def test_get_features(mock_parse_xml):
    path = TESTS_DIR / "fixtures" / "test"
    mock_parse_xml.return_value = {}
    assert [{}] == get_features(path)
