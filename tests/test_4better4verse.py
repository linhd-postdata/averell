import json
from unittest.mock import patch

import pytest

from averell.readers.forbetter4verse import get_features
from averell.readers.forbetter4verse import parse_xml
from tests.test_utils import FIXTURES_DIR

FORB4V_PATH = FIXTURES_DIR / "4b4v"


@pytest.fixture
def forbetter4verse():
    path = FIXTURES_DIR / "forbetter4verse.json"
    return json.loads(path.read_text())


def test_parse_xml(forbetter4verse):
    path = (FORB4V_PATH / "for_better_for_verse-master" / "poems" /
            "input_4better4verse.xml")
    poem = parse_xml(path)
    assert poem == forbetter4verse


@patch('averell.readers.forbetter4verse.parse_xml', return_value={})
def test_get_features(mock_poem_info):
    assert [{}] == get_features(FORB4V_PATH)
    assert mock_poem_info.called
