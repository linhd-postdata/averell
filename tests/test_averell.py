from click.testing import CliRunner

from averell.cli import download
from averell.cli import export
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
