import xml.etree.ElementTree as ETree


def parse_xml(xml_file):
    poem = {}
    stanza_list = []
    tree = ETree.parse(xml_file)
    root = tree.getroot()
    analysis_description = root.find(".//{*}metDecl/{*}p").text
    title = root.find(".//{*}head/{*}title").text
    author = root.find(".//{*}author").text
    line_group_list = root.findall(".//*{*}lg")
    manually_checked = 'manual' in analysis_description
    poem.update({
                    "manually_checked": manually_checked, "title": title,
                    "author": author
                })
    for stanza_number, line_group in enumerate(line_group_list):
        line_list = []
        for line in line_group:
            line_list.append({
                                 "line_number": str(line.attrib["n"]),
                                 "text": "".join(line.itertext()),
                                 "metrical_pattern": line.attrib["met"]
                             })
        stanza_list.append({
                               "stanza_number": str(stanza_number + 1),
                               "type": line_group.attrib["type"],
                               "lines": line_list
                           })
        poem.update({"stanzas": stanza_list})
    return poem


def get_features(path):
    for filename in path.rglob('*.xml'):
        parse_xml(str(filename))
