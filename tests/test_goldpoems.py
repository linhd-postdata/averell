import json
from pathlib import Path

import pytest

from averell.readers.goldpoems import parse_xml


@pytest.fixture
def goldpoems():
    return json.loads(Path("tests/fixtures/goldpoems.json").read_text())


def test_parse_xml(goldpoems):
    poem = parse_xml("tests/fixtures/input-goldpoems.xml")
    assert poem == goldpoems
