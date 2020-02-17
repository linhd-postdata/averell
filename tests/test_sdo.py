import json
from pathlib import Path

import pytest

from averell.readers.sdo import parse_xml


@pytest.fixture
def sdo():
    return json.loads(Path("tests/fixtures/sdo.json").read_text())


def test_parse_xml(sdo):
    poem = parse_xml("tests/fixtures/input-sdo.xml")
    assert poem == sdo
