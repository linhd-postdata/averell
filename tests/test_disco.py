import json
from unittest.mock import patch

import pytest

from averell.readers.disco import get_features
from averell.readers.disco import parse_xml
from tests.test_utils import TESTS_DIR

DISCO_PATH = (TESTS_DIR / "fixtures" / "disco2_1")


@pytest.fixture
def disco():
    path = TESTS_DIR / "fixtures" / "disco.json"
    return json.loads(path.read_text())


def test_parse_xml(disco):
    path = (DISCO_PATH / "disco-2.1" / "tei" / "19th" /
            "per-sonnet" / "input_disco.xml")
    poem = parse_xml(path)
    assert poem == disco


@patch('averell.readers.disco.parse_xml', return_value={})
def test_get_features(mock_parse_xml):
    assert [{}] == get_features(DISCO_PATH)
    assert mock_parse_xml.called
