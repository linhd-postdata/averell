import os
import xml.etree.ElementTree as ETree

from averell.utils import TEI_NAMESPACE as NS


def parse_xml(xml_file):
    """
    XML TEI poem parser for 'Sonetos Siglo de Oro' corpus.
    We read the data and find elements like title, author, etc with XPath
    expressions.
    Then, we iterate over the poem text and we look for each stanza and line
    data.
    :param xml_file: Path for the xml file
    :return: Poem python dict with the data obtained
    """
    poem = {}
    stanza_list = []
    tree = ETree.parse(xml_file)
    root = tree.getroot()
    analysis_description = root.find(f".//{NS}metDecl/{NS}p").text
    title = root.find(f".//{NS}head/{NS}title").text
    author = root.find(f".//{NS}author").text
    line_group_list = root.findall(f".//*{NS}lg")
    manually_checked = 'manual' in analysis_description
    if title is None:
        title = os.path.splitext(os.path.basename(xml_file))[0]
    corpus_name = xml_file.parts[-4]
    if "adso100" in str(xml_file):
        corpus_name = xml_file.parts[-3]
    poem.update({
        "poem_title": title,
        "corpus": corpus_name,
        "manually_checked": manually_checked,
        "author": author
    })
    line_number = 0
    for stanza_number, line_group in enumerate(line_group_list):
        line_list = []
        stanza_text = []
        for line in line_group:
            line_text = "".join(line.itertext()).strip().split("\n")[0].strip()
            line_list.append({
                "line_number": line_number + 1,
                "n": line.get("n"),
                "line_text": line_text,
                "metrical_pattern": line.attrib["met"]
            })
            stanza_text.append(line_text)
            line_number += 1
        stanza_list.append({
            "stanza_number": stanza_number + 1,
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
    feature_list = []
    for filename in path.rglob('*.xml'):
        result = parse_xml(filename)
        feature_list.append(result)
    return feature_list
