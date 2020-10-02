import json
from unittest.mock import patch

import pytest

from averell.readers.sdo import get_features
from averell.readers.sdo import parse_xml
from tests.test_utils import TESTS_DIR

SDO_PATH = TESTS_DIR / "fixtures" / "adso"


@pytest.fixture
def sdo():
    path = TESTS_DIR / "fixtures" / "sdo.json"
    return json.loads(path.read_text())


def test_parse_xml(sdo):
    path = (SDO_PATH / "CorpusSonetosSigloDeOro-master" / "authorname" /
            "input_sdo.xml")
    poem = parse_xml(path)
    assert poem == sdo


@patch('averell.readers.sdo.parse_xml', return_value={})
def test_get_features(mock_parse_xml):
    assert [{}] == get_features(SDO_PATH)
    assert mock_parse_xml.called
