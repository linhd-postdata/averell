import logging
from unittest.mock import patch

from click.testing import CliRunner

from averell.cli import download
from averell.cli import export
from averell.cli import list_command
from averell.cli import main

from .test_core import _corpora_sources


def test_main():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.exit_code == 0


def test_download():
    runner = CliRunner()
    result = runner.invoke(download, [])

    assert result.exit_code == 0


@patch('averell.core.download_corpora')
def test_download_2(mock_download, caplog):
    mock_download.return_value = []
    expected = "Downloaded Disco V3 corpus"
    runner = CliRunner()
    result = runner.invoke(download, ["2"])
    with caplog.at_level(logging.INFO):
        assert expected in caplog.text
    assert result.exit_code == 0


def test_export_no_ids(caplog):
    expected = "Using corpora folder: './corpora'\n"
    runner = CliRunner()
    result = runner.invoke(export, [])

    assert result.output == expected
    assert result.exit_code == 0


@patch('averell.core.CORPORA_SOURCES', _corpora_sources)
def test_export_not_downloaded(caplog):
    expected = "Using corpora folder: './corpora'\n"
    runner = CliRunner()
    result = runner.invoke(export, ["1", "--granularity", "line"])
    assert result.output == expected
    assert result.exit_code == 0


@patch('averell.utils.CORPORA_SOURCES', _corpora_sources)
def test_list():
    expected = "\n".join([
        '  id  name      size      docs    words  granularity    license',
        '----  --------  ------  ------  -------  -------------  ---------',
        '   1  testing   22M       4088   381539  stanza         CC-BY',
        '   2  testing2  22M       4088   381539  stanza         CC-BY\n',
        ])
    runner = CliRunner()
    result = runner.invoke(list_command, [])
    assert result.output == expected
    assert result.exit_code == 0
