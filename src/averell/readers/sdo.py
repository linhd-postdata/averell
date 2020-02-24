import os
import xml.etree.ElementTree as ETree


def parse_xml(xml_file):
    """
    XML TEI poem parser for corpus 'Sonetos del siglo de oro'
    :param xml_file: path of xml file
    :return: poem dict
    """
    poem = {}
    stanza_list = []
    tree = ETree.parse(xml_file)
    root = tree.getroot()
    analysis_description = root.find(
        ".//{http://www.tei-c.org/ns/1.0}metDecl/{http://www.tei-c.org/ns/1.0}p").text
    title = root.find(
        ".//{http://www.tei-c.org/ns/1.0}head/{http://www.tei-c.org/ns/1.0}title").text
    author = root.find(".//{http://www.tei-c.org/ns/1.0}author").text
    line_group_list = root.findall(".//*{http://www.tei-c.org/ns/1.0}lg")
    manually_checked = 'manual' in analysis_description
    if title is not None:
        poem.update({"poem_title": title})
    else:
        poem.update({"poem_title": os.path.splitext(os.path.basename(xml_file))[0]})
    poem.update({
        "manually_checked": manually_checked,
        "author": author
    })
    for stanza_number, line_group in enumerate(line_group_list):
        line_list = []
        stanza_text = []
        for line in line_group:
            line_text = "".join(line.itertext())
            line_list.append({
                "line_number": str(line.attrib["n"]),
                "line_text": line_text,
                "metrical_pattern": line.attrib["met"]
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
    for filename in path.rglob('*.xml'):
        result = parse_xml(str(filename))
        feature_list.append(result)
    return feature_list
