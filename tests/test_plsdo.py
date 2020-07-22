import json
from unittest import mock
from unittest.mock import patch

import pytest

from averell.readers.plsdo import CommentedTreeBuilder
from averell.readers.plsdo import get_features
from averell.readers.plsdo import parse_xml
from tests.test_utils import TESTS_DIR


@pytest.fixture
def plsdo():
    path = TESTS_DIR / "fixtures" / "plsdo.json"
    return json.loads(path.read_text())


def test_parse_xml(plsdo):
    path = TESTS_DIR / "fixtures" / "input_plsdo.xml"
    poem = parse_xml(str(path))
    assert poem == plsdo


def test_commented_tree_builder_class():
    data = mock.MagicMock()
    commented_tree = CommentedTreeBuilder()
    commented_tree.comment(data)
    assert True


@patch('averell.readers.plsdo.parse_xml')
def test_get_features(mock_parse_xml):
    path = TESTS_DIR / "fixtures" / "test"
    mock_parse_xml.return_value = {}
    assert [{}] == get_features(path)
