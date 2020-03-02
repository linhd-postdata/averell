import xml.etree.ElementTree as ETree
from pathlib import Path

from averell.utils import TEI_NAMESPACE as NS


def parse_xml(xml_file):
    """
    XML TEI poem parser for 'disco' corpus.
    We read the data and find elements like title, author, etc with XPath
    expressions.
    Then, we iterate over the poem text and we look for each stanza and line
    data.
    :param xml_file: Path for the xml file
    :return: Poem python dict with the data obtained
    """
    tree = ETree.parse(xml_file)
    root = tree.getroot()

    poem = {}
    stanza_list = []

    analysis_description = root.find(f".//{NS}metDecl/{NS}p").text
    title = root.find(f".//{NS}front/{NS}head").text
    author = root.find(f".//{NS}author").text
    line_group_list = root.findall(f".//*{NS}lg")
    manually_checked = 'manual' in analysis_description
    alt_title = root.find(
        f".//*{NS}bibl/{NS}title[@property='dc:alternative']").text

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
