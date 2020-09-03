import json
from unittest.mock import patch

import pytest

from averell.readers.ecpa import get_features
from averell.readers.ecpa import get_poem_info
from tests.test_utils import FIXTURES_DIR

ECPA = FIXTURES_DIR / "ecpa" / "web"


@pytest.fixture
def ecpa():
    path = FIXTURES_DIR / "ecpa.json"
    return json.loads(path.read_text())


def test_parse_xml(ecpa):
    path = ECPA / "works" / "input_ecpa" / "input_ecpa.xml"
    authors_file = ECPA / "resources" / "models" / "authwork_mdp.json"
    authors = json.loads(authors_file.read_text())
    lines_file = ECPA / "works" / "input_ecpa" / "input_ecpa_l.json"
    lines_info = json.loads(lines_file.read_text())
    poem = get_poem_info(str(path), lines_info, authors)
    assert poem == ecpa


@pytest.fixture
def ecpa_cov():
    path = FIXTURES_DIR / "ecpa2.json"
    return json.loads(path.read_text())


def test_parse_xml_cov(ecpa_cov):
    path = ECPA / "works" / "input_ecpa2" / "input_ecpa2.xml"
    authors_file = ECPA / "resources" / "models" / "authwork_mdp.json"
    authors = json.loads(authors_file.read_text())
    lines_file = ECPA / "works" / "input_ecpa2" / "input_ecpa2_l.json"
    lines_info = json.loads(lines_file.read_text())
    poem = get_poem_info(str(path), lines_info, authors)
    assert poem == ecpa_cov


@patch('averell.readers.ecpa.get_poem_info')
def test_get_features(mock_poem_info):
    path = FIXTURES_DIR / "ecpa"
    mock_poem_info.return_value = {}
    assert [{}, {}] == get_features(path)
