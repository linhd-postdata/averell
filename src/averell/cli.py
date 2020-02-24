from pathlib import Path

import click
from averell.core import get_corpora


@click.group()
def main():
    """
    Simple CLI for querying corpora on Github
    """


@main.command()
@click.option('--output', default=Path.cwd() / "corpora", help='Folder to download')
@click.option('--granularity', default=None, help='Granularity')
@click.argument('ids', nargs=-1)
def download(ids, granularity, output):
    """
    Download the corpus with IDS
    """
    numbers = [int(x) for x in ids]
    # print(numbers, output)
    corpora_features = get_corpora(numbers, granularity, output)
    return corpora_features


if __name__ == '__main__':
    main()
