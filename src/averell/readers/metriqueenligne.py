import json


def parse_json(json_file):
    """JSON poem parser for 'Metrique en ligne' corpus.
    We read the data and find elements like title, author, year, etc. Then
    we iterate over the poem text and we look for each stanza and line data.

    :param json_file: Path for the json file
    :return: Dict with the data obtained from the poem
    :rtype: dict
    """
    corpus = json.loads(json_file.read_text())
    for work in corpus:
        poem = {}
        title = work["title"]
        author = work["author"]
        year = work["date"]
        structure = work["structure"]
        manually_checked = False
        stanza_list = []
        line_number = 0
        for stanza_number, stanza in enumerate(work["text"]):
            line_list = []
            for line in stanza:
                line_text = line["verse"]
                line_length = line["metre"]
                rhyme = line["rhyme"]
                line_list.append({
                    "line_number": line_number + 1,
                    "line_text": line_text,
                    "metrical_pattern": None,
                    "line_length": line_length,
                    "rhyme": rhyme,
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
            "structure": structure,
            "year": year,
            "manually_checked": manually_checked,
            "stanzas": stanza_list
        })
        yield poem


def get_features(path):
    """ Function to find each poem in corpus file and parse it

    :param path: Corpus Path
    :return: List of poem dicts
    """
    corpus_file = path / "metrique_en_ligne.json"
    result = list(parse_json(corpus_file))
    return result
