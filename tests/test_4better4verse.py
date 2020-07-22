import json
from unittest.mock import patch

import pytest

from averell.readers.forbetter4verse import get_features
from averell.readers.forbetter4verse import parse_xml
from tests.test_utils import FIXTURES_DIR

poems = FIXTURES_DIR / "poems"


@pytest.fixture
def forbetter4verse():
    path = FIXTURES_DIR / "forbetter4verse.json"
    return json.loads(path.read_text())


def test_parse_xml(forbetter4verse):
    path = poems / "input_4better4verse.xml"
    poem = parse_xml(str(path))
    assert poem == forbetter4verse


@patch('averell.readers.forbetter4verse.parse_xml')
def test_get_features(mock_poem_info):
    mock_poem_info.return_value = {}
    assert [{}] == get_features(FIXTURES_DIR)
