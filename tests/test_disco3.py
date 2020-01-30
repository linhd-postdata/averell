import json
from pathlib import Path

import pytest

from averell.readers.disco3 import parse_xml


@pytest.fixture
def disco3():
    return json.loads(Path("tests/fixtures/disco3.json").read_text())


def test_parse_xml(disco3):
    poem = parse_xml("tests/fixtures/input-disco-3.xml")
    assert [*poem] == disco3
