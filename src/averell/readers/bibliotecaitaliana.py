import json

from averell.utils import uncompress_corpus


def parse_json(json_file) -> dict:
    """JSON poem parser for 'Biblioteca italiana' poetry corpus.
    We read the data and find elements like title, author, year, etc. Then
    we iterate over the poem text and we look for each stanza and line data.

    :param json_file: Path for the corpus json file
    :return: Dict with the data obtained from the poem
    """
    corpus = json.loads(json_file.read_text())
    corpus_name = json_file.parts[-2]
    for work in corpus:
        poem = {}
        title = f"{work['collection']} - {work['title']}"
        author = work["author"]
        manually_checked = work["manually_checked"]
        stanza_list = []
        line_number = 0
        for stanza_number, stanza in enumerate(work["text"]):
            line_list = []
            for line in stanza:
                metrical_pattern = line.get("metrical_pattern")
                line_length = len(
                    metrical_pattern) if metrical_pattern is not None else None
                word_list = [{"word_text": word} for word in
                             line["verse"].split()]
                line_list.append({
                    "line_number": line_number + 1,
                    "line_text": line["verse"],
                    "metrical_pattern": metrical_pattern,
                    "line_length": line_length,
                    "words": word_list,
                })
                line_number += 1
            stanza_text = "\n".join([line["line_text"] for line in line_list])
            stanza_list.append({
                "stanza_number": stanza_number + 1,
                "stanza_type": None,
                "lines": line_list,
                "stanza_text": stanza_text,
            })
        poem.update({
            "poem_title": title,
            "author": author,
            "manually_checked": manually_checked,
            "stanzas": stanza_list,
            "corpus": corpus_name,
        })
        yield poem


def get_features(path) -> list:
    """ Function to find each poem in corpus file and parse it

    :param path: Corpus Path
    :return: List of poem dicts
    """
    corpus_zip = path / "biblioteca_italiana-master" / "biblitaliana.zip"
    if corpus_zip.exists():
        uncompress_corpus(corpus_zip, path)
    corpus_file = path / "biblitaliana.json"
    result = list(parse_json(corpus_file))
    return result
