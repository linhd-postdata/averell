from unittest.mock import patch

from click.testing import CliRunner

from averell.cli import download
from averell.cli import export
from averell.cli import list_command
from averell.cli import main


def test_main():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.exit_code == 0


def test_download():
    runner = CliRunner()
    result = runner.invoke(download, [])

    assert result.exit_code == 0


def test_export():
    runner = CliRunner()
    result = runner.invoke(export, [])

    assert result.exit_code == 0


_corpora_sources = [
        {'name': 'testing',
         'properties':
             {
                 'license': 'CC-BY',
                 'size': '22M',
                 'doc_quantity': 4088,
                 'word_quantity': 381539,
                 'granularity': ['stanza']
             }
         }
    ]


@patch('averell.utils.CORPORA_SOURCES', _corpora_sources)
def test_list():
    expected = "\n".join([
        '  id  name     size      docs    words  granularity    license',
        '----  -------  ------  ------  -------  -------------  ---------',
        '   1  testing  22M       4088   381539  stanza         CC-BY\n',
        ])
    runner = CliRunner()
    result = runner.invoke(list_command, [])
    assert result.output == expected
    assert result.exit_code == 0
