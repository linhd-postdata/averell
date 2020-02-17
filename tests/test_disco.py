import json
from pathlib import Path

import pytest

from averell.readers.disco import parse_xml


@pytest.fixture
def disco():
    return json.loads(Path("tests/fixtures/disco.json").read_text())


def test_parse_xml(disco):
    poem = parse_xml("tests/fixtures/input-disco.xml")
    assert poem == disco
