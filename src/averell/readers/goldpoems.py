import xml.etree.ElementTree as ETree


def parse_xml(xml_file):
    poem = {}
    stanza_list = []
    tree = ETree.parse(xml_file)
    root = tree.getroot()
    title = root.find(
        ".//{http://www.tei-c.org/ns/1.0}head/{http://www.tei-c.org/ns/1.0}title").text
    author = root.find(".//{http://www.tei-c.org/ns/1.0}author").text
    line_group_list = root.findall(".//*{http://www.tei-c.org/ns/1.0}lg")
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
    feature_list = []
    for filename in path.rglob('*.xml'):
        result = parse_xml(str(filename))
        feature_list.append(result)
    return feature_list
