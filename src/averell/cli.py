from pathlib import Path

import click
from tabulate import tabulate

from .core import export_corpora
from .core import get_corpora
from .utils import get_ids
from .utils import get_main_corpora_info


@click.group()
def main():
    """
    Averell is a simple CLI for managing poetic corpora
    """


@main.command()
@click.option('--corpora-folder', default=Path.cwd() / "corpora",
              help='Local folder where the corpora will be downloaded')
@click.argument('ids', nargs=-1)
def download(ids, corpora_folder):
    """
    Download the corpus with IDS. IDS can be numeric identifiers in the
    "averell list" output, corpus shortcodes (shown between parenthesis),
    the speciall literal "all" to download all corpora, or two-letter ISO
    language codes to download avaliable corpora in a specific language.

    For example, the command "averell download 1 bibit fr" will download
    DISCO V2.1, the Biblioteca Italiana poetry corpus, and all corpora
    tagged with the French languge tag.
    """
    corpora_features = get_corpora(get_ids(ids), corpora_folder)
    return corpora_features


@main.command()
@click.option('--granularity', help='Granularity', default='line')
@click.option('--corpora-folder', default="./corpora",
              help='Local folder where the corpora are located')
@click.option('--filename', default="",
              help='Result filename')
@click.option('--no-download', default=False, is_flag=True, type=click.BOOL,
              help='Avoid downloading a corpus if missing')
@click.argument('ids', nargs=-1)
def export(ids, granularity, corpora_folder, filename, no_download):
    """
    Parse the corpus with IDs with the GRANULARITY into CORPORA-FOLDER.
    IDS can be numeric identifiers in the
    "averell list" output, corpus shortcodes (shown between parenthesis),
    the speciall literal "all" to export all corpora, or two-letter ISO
    language codes to export avaliable corpora in a specific language.

    For example, the command "averell export 1 bibit fr" will export
    DISCO V2.1, the Biblioteca Italiana poetry corpus, and all corpora
    tagged with the French languge tag in a single file spliting poems
    line by line.

    By default, "averell export" will download a corpus if not present
    in CORPORA-FOLDER.
    """
    click.echo(f"Using corpora folder: '{corpora_folder}'")
    export_corpora(
        get_ids(ids), granularity, corpora_folder, filename, no_download
    )


@main.command(name="list")
@click.option('--rst', default=False, is_flag=True, type=click.BOOL,
              help='Prints the corpora list in reStructuredText format')
def list_command(rst):
    """Show the CORPORA info
    """
    table = get_main_corpora_info()
    if not rst:
        table_format = "simple"
    else:
        table_format = "rst"
    click.echo(tabulate(
        table, headers="keys", numalign="right", tablefmt=table_format
    ))


if __name__ == '__main__':
    main()
