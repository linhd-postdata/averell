from pathlib import Path

import click

from .core import export_corpora
from .core import get_corpora
from .core import list_corpora


@click.group()
def main():
    """
    Simple CLI for querying corpora on Github
    """


@main.command()
@click.option('--output', default=Path.cwd() / "corpora",
              help='Folder to download')
@click.argument('ids', nargs=-1, type=click.INT)
def download(ids, output):
    """
    Download the corpus with IDS
    """
    corpora_features = get_corpora(ids, output)
    return corpora_features


@main.command()
@click.option('--granularity', help='Granularity')
@click.option('--corpora-folder', default="./corpora",
              help='Local folder where the corpora are located')
@click.argument('ids', nargs=-1, type=click.INT)
def export(ids, granularity, corpora_folder):
    """
    Parse the corpus with IDs with the GRANULARITY into CORPORA-FOLDER
    """
    export_corpora(ids, granularity, corpora_folder)


@main.command()
def list():
    """Show the CORPORA info
    """
    list_corpora()


if __name__ == '__main__':
    main()
