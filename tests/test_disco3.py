import json
from unittest.mock import patch

import pytest

from averell.readers.disco3 import get_features
from averell.readers.disco3 import parse_xml
from tests.test_utils import TESTS_DIR

DISCO3_PATH = (TESTS_DIR / "fixtures" / "disco3")


@pytest.fixture
def disco3():
    path = TESTS_DIR / "fixtures" / "disco3.json"
    return json.loads(path.read_text())


def test_parse_xml(disco3):
    path = (DISCO3_PATH / "disco-3" / "tei" / "19th" /
            "per-sonnet" / "input_disco3.xml")
    poem = parse_xml(path)
    assert poem == disco3


@patch('averell.readers.disco3.parse_xml', return_value={})
def test_get_features(mock_parse_xml):
    assert [{}] == get_features(DISCO3_PATH)
    assert mock_parse_xml.called
