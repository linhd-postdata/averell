import json


def parse_json(json_file):
    """JSON poem parser for 'Gongocorpus'.
    We read the data and find elements like title, author, year, etc. Then
    we iterate over the poem text and we look for each stanza, line, word
    and syllable data.

    :param json_file: Path for the json file
    :return: Dict with the data obtained from the poem
    :rtype: dict
    """
    corpus_poem = json.loads(json_file.read_text())
    poem = {}
    title = corpus_poem["incipit"]
    author = corpus_poem["author"]
    year = corpus_poem["year"]
    authorship = corpus_poem["authorship"]
    manually_checked = False
    scanned_poem = corpus_poem["scanned_poem"]
    poem_text = corpus_poem["text"]
    stanza_list = []
    line_number = 0
    for stanza_number, stanza in enumerate(poem_text.split("\n\n")):
        stanza_text = "".join(stanza)
        line_list = []
        for line_text in stanza.split("\n"):
            scanned_line = scanned_poem[line_number]
            rythym_info = scanned_line["rhythm"]
            metrical_pattern = rythym_info["stress"]
            line_length = rythym_info["length"]
            word_list = []
            for token in scanned_line["tokens"]:
                if "word" in token:
                    word = token["word"]
                    stress_position = token["stress_position"]
                    syllables_text = [syl["syllable"] for syl in word]
                    word_text = "".join(syllables_text)
                    has_synalepha = [True for syl in word
                                     if "has_synalepha" in syl]
                    word_dict = {
                        "word_text": word_text,
                        "stress_position": stress_position,
                        "syllables": syllables_text
                    }
                    if True in has_synalepha:
                        word_dict.update({
                            "has_synalepha": True,
                        })
                    word_list.append(word_dict)
            line_list.append({
                "line_number": line_number + 1,
                "line_text": line_text,
                "metrical_pattern": metrical_pattern,
                "line_length": line_length,
                "words": word_list,
            })
            line_number += 1
        stanza_list.append({
            "stanza_number": stanza_number + 1,
            "stanza_type": "",
            "lines": line_list,
            "stanza_text": stanza_text,
        })
    poem.update({
        "poem_title": title,
        "author": author,
        "authorship": authorship,
        "year": year,
        "manually_checked": manually_checked,
        "stanzas": stanza_list
    })
    return poem


def get_features(path):
    """ Function to find each poem file and parse it

    :param path: Corpus Path
    :return: List of poem dicts
    """
    feature_list = []
    json_files = path / "corpus_json"
    for filename in json_files.rglob("*.json"):
        result = parse_json(filename)
        feature_list.append(result)
    return feature_list
