from pathlib import Path

import click
from tabulate import tabulate

from averell.core import create_corpus
from averell.core import export_corpora
from averell.core import get_corpora

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


@main.command()
@click.option('--granularity', help='Granularity', default=None)
@click.option('--corpora-folder', default="./corpora",
              help='Local folder where the corpora are located')
@click.option('--filename', default="",
              help='Result filename')
@click.option('--fileformat', default="json", help="Format of the result file/s",
              type=click.Choice(['json', 'rdf'], case_sensitive=False))
@click.option('--output-type', default="train",
              type=click.Choice(['standard', 'train']),
              help='"Standard" for keep structured JSON, '
                   '"train" for jsonlines like format')
@click.option('--unique-file', default=False, is_flag=True, type=click.BOOL,
              help='Export the averell return to unique file, '
                   'instead of one file per poem of the corpus')
@click.argument('ids', nargs=-1)
def create(ids, granularity, corpora_folder, filename, fileformat, output_type,
           unique_file):
    """Build a new corpus based on the corpus with IDs into CORPORA_FOLDER with
    FILEFORMAT file format (rdf | json).
    If GRANULARITY is provided, this new corpus includes all the information of
    the poems of the selected corpora at the granularity level selected,
    otherwise, it includes all available poems information.
    IDs can be numeric identifiers in the corpora list, corpus shortcodes
    (shown between parenthesis), the speciall literal "all" to export all
    corpora, or two-letter ISO language codes to export avaliable corpora in a
    specific language.

    For example, the command
    `averell create 1 bibit fr --granularity line --corpora-folder my_corpora --format rdf --filename disco_bibit_fr_lines`
    will generate a new RDF file compliant with ONTOPOETRY Postdata Ontology
    containing DISCO V2.1, the Biblioteca Italiana poetry corpus, and all corpora
    tagged with the French language tag splitting poems line by line.
    """
    create_corpus(ids, granularity, corpora_folder, filename, fileformat,
                  output_type, unique_file)


if __name__ == '__main__':
    main()
