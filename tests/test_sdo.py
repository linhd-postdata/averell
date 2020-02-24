import json
from pathlib import Path
from unittest.mock import patch

import pytest

from averell.readers.sdo import get_features
from averell.readers.sdo import parse_xml

from tests.test_utils import TESTS_DIR


@pytest.fixture
def sdo():
    return json.loads(Path("tests/fixtures/sdo.json").read_text())


def test_parse_xml(sdo):
    poem = parse_xml("tests/fixtures/input_sdo.xml")
    assert poem == sdo


@patch('averell.readers.sdo.parse_xml')
def test_get_features(mock_parse_xml):
    path = TESTS_DIR / "fixtures" / "test"
    mock_parse_xml.return_value = {}
    assert [{}] == get_features(path)

