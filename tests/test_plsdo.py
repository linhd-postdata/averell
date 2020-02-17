import json
from pathlib import Path

import pytest

from averell.readers.plsdo import parse_xml


@pytest.fixture
def plsdo():
    return json.loads(Path("tests/fixtures/plsdo.json").read_text())


def test_parse_xml(plsdo):
    poem = parse_xml("tests/fixtures/input_plsdo.xml")
    assert poem == plsdo
