import re
import xml.etree.ElementTree as ETree
from pathlib import Path

XML_PATH = Path("tei") / "all-periods-per-author"


def parse_xml(xml_file):
    """
    XML TEI poem parser for 'disco 3' corpus.
    We read the data and find elements like title, author, etc with XPath
    expressions.
    Then, we iterate over the poem text and we look for each stanza and line
    data.
    :param xml_file: Path for the xml file
    :return: Poem python dict with the data obtained
    """
    ns = "{http://www.tei-c.org/ns/1.0}"
    tree = ETree.parse(xml_file)
    root = tree.getroot()

    poem = {}
    stanza_list = []

    analysis_description = root.find(f".//{ns}metDecl/{ns}p").text
    title = root.find(f".//{ns}head").text
    author = root.find(f".//{ns}author").text
    line_group_list = root.findall(f".//*{ns}lg")
    manually_checked = 'manual' in analysis_description
    alt_title = root.find(f".//*{ns}bibl/{ns}title[@property='dc:alternative']")
    poem.update({
        "manually_checked": manually_checked,
        "poem_title": title,
        "author": author,
    })
    if alt_title is not None:
        alt_title = re.sub(r"[\n ]+", " ", "".join(alt_title.itertext()))
        poem.update({"poem_alt_title": alt_title})
    line_number = 1
    for stanza_number, line_group in enumerate(line_group_list):
        line_list = []
        stanza_text = []
        for line in line_group:
            line_text = re.sub(r"[\n ]+", " ", "".join(line.itertext()))
            line_list.append({
                "line_number": line_number,
                "line_text": line_text,
                "metrical_pattern": line.get("met", "None")
            })
            stanza_text.append(line_text)
            line_number += 1
        stanza_list.append({
            "stanza_number": str(stanza_number + 1),
            "stanza_type": line_group.attrib["type"],
            "lines": line_list,
            "stanza_text": "\n".join(stanza_text),
        })
    poem.update({"stanzas": stanza_list})
    return poem


def get_features(path):
    """
    Function to find each poem file and parse it
    :param path: Corpus Path
    :return: List of poem dicts
    """
    xml_files = Path("*") / "per-sonnet" / "*.xml"
    feature_list = []
    for filename in (Path(path)).rglob(str(xml_files)):
        result = parse_xml(str(filename))
        feature_list.append(result)
    return feature_list
