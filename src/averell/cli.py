from pathlib import Path

import click
from tabulate import tabulate

from .core import export_corpora
from .core import get_corpora
from .utils import get_main_corpora_info


@click.group()
def main():
    """
    Simple CLI for querying corpora on Github
    """


@main.command()
@click.option('--corpora-folder', default=Path.cwd() / "corpora",
              help='Local folder where the corpora will be downloaded')
@click.argument('ids', nargs=-1, type=click.INT)
def download(ids, corpora_folder):
    """
    Download the corpus with IDS
    """
    indexes = [corpus_id - 1 for corpus_id in ids]
    corpora_features = get_corpora(indexes, corpora_folder)
    return corpora_features


@main.command()
@click.option('--granularity', help='Granularity')
@click.option('--corpora-folder', default="./corpora",
              help='Local folder where the corpora are located')
@click.option('--filename', default="",
              help='Result filename')
@click.argument('ids', nargs=-1, type=click.INT)
def export(ids, granularity, corpora_folder, filename):
    """
    Parse the corpus with IDs with the GRANULARITY into CORPORA-FOLDER
    """
    click.echo(f"Using corpora folder: '{corpora_folder}'")
    export_corpora(ids, granularity, corpora_folder, filename)


@main.command(name="list")
def list_command():
    """Show the CORPORA info
    """
    table = get_main_corpora_info()
    click.echo(tabulate(table, headers="keys", numalign="right"))


if __name__ == '__main__':
    main()
