import json


def parse_json(json_file) -> dict:
    """JSON poem parser for 'Czech Verse' poetry corpus.
    We read the data and find elements like title, author, year, etc. Then
    we iterate over the poem text and we look for each stanza and line data.

    :param json_file: Path for the corpus json file
    :return: Dict with the data obtained from the poem
    """
    corpus = json.loads(json_file.read_text())
    corpus_name = json_file.parts[-4]
    for work in corpus:
        poem = {}
        title = work["biblio"]["p_title"]
        if title is None:
            title = work["poem_id"]
        author = work["p_author"]["identity"]
        year = work["biblio"]["year"]
        manually_checked = True
        stanza_list = []
        line_number = 0
        for stanza_number, stanza in enumerate(work["body"]):
            line_list = []
            for line in stanza:
                metrical_pattern = line.get("stress")
                rhyme = line.get("rhyme")
                line_length = len(
                    metrical_pattern) if metrical_pattern is not None else None
                word_list = [{"word_text": word["token"]} for word in
                             line["words"]]
                line_list.append({
                    "line_number": line_number + 1,
                    "line_text": line["text"],
                    "metrical_pattern": metrical_pattern,
                    "line_length": line_length,
                    "rhyme": rhyme,
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
            "year": year
        })
        yield poem


def get_features(path) -> list:
    """ Function to find each poem in corpus folder and parse it

    :param path: Corpus Path
    :return: List of poem dicts
    """
    feature_list = []
    json_folder = path / "corpusCzechVerse-master" / "ccv"
    for filename in json_folder.rglob("*.json"):
        result = list(parse_json(filename))
        feature_list.extend(result)
    return feature_list
