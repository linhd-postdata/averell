import json
from unittest.mock import patch

import pytest

from averell.readers.stichotheque import get_features
from averell.readers.stichotheque import parse_xml
from tests.test_utils import TESTS_DIR

STICHO_PATH = TESTS_DIR / "fixtures" / "stichopt"


@pytest.fixture
def stichopt():
    path = TESTS_DIR / "fixtures" / "stichopt.json"
    return json.loads(path.read_text())


def test_parse_xml(stichopt):
    path = STICHO_PATH / "stichotheque-pt-master" / "xml" / "input_stichopt.xml"
    result = parse_xml(path)
    assert list(result) == stichopt


@patch('averell.readers.stichotheque.parse_xml', return_value={})
def test_get_features(mock_parse_xml):
    assert [] == get_features(STICHO_PATH)
    assert mock_parse_xml.called
