import xml.etree.ElementTree as ETree

from averell.utils import TEI_NAMESPACE as NS


def parse_xml(xml_file):
    """
    XML TEI poem parser for 'ADSO 100 poems' corpus.
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
    title = root.find(f".//{NS}head/{NS}title").text
    author = root.find(f".//{NS}author").text
    line_group_list = root.findall(f".//*{NS}lg")
    manually_checked = True
    poem.update({
        "manually_checked": manually_checked,
        "poem_title": title,
        "author": author
    })
    for stanza_number, line_group in enumerate(line_group_list):
        stanza_text = []
        line_list = []
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
            "stanza_text": "\n".join(stanza_text),
            "lines": line_list
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
        result = parse_xml(str(filename))
        feature_list.append(result)
    return feature_list
