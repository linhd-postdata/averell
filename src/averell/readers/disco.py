import re
import xml.etree.ElementTree as ETree
from pathlib import Path


def parse_xml(xml_file):
    """
    XML TEI poem parser for 'disco' corpus
    :param xml_file: path of xml file
    :return: poem dict
    """
    tree = ETree.parse(xml_file)
    root = tree.getroot()

    poem = {}
    stanza_list = []

    analysis_description = root.find(
        ".//{http://www.tei-c.org/ns/1.0}metDecl/{http://www.tei-c.org/ns/1.0}p").text
    title = root.find(
        ".//{http://www.tei-c.org/ns/1.0}front/{http://www.tei-c.org/ns/1.0}head").text
    author = root.find(".//{http://www.tei-c.org/ns/1.0}author").text
    line_group_list = root.findall(".//*{http://www.tei-c.org/ns/1.0}lg")
    manually_checked = 'manual' in analysis_description
    alt_title = root.find(
        ".//*{http://www.tei-c.org/ns/1.0}bibl"
        "/{http://www.tei-c.org/ns/1.0}title[@property='dc:alternative']").text

    poem.update({
        "manually_checked": manually_checked,
        "poem_title": title,
        "author": author,
        "poem_alt_title": alt_title,
    })
    for stanza_number, line_group in enumerate(line_group_list):
        line_list = []
        stanza_text = []
        for line in line_group:
            line_text = "".join(line.itertext())
            line_list.append({
                "line_number": str(line.attrib["n"]),
                "line_text": line_text,
                "metrical_pattern": line.get("met", "None")
            })
            stanza_text.append(line_text)
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
    Function to parse all corpus poems
    :param path: Corpus path
    :return: list of poem dicts
    """
    feature_list = []
    for filename in (Path(path)).rglob('*/per-sonnet/*.xml'):
        result = parse_xml(str(filename))
        feature_list.append(result)
    return feature_list
