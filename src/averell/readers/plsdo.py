import re
import xml.etree.ElementTree as ETree
from xml.etree.ElementTree import TreeBuilder
from xml.etree.ElementTree import XMLParser


def parse_xml(xml_file):
    custom_treebuilder = TreeBuilder(insert_comments=True)
    custom_xmlparser = XMLParser(target=custom_treebuilder)
    poem = {}
    tree = ETree.parse(xml_file, parser=custom_xmlparser)
    root = tree.getroot()
    stanza_list = []
    analysis_description = "".join(root.find(".//*{*}metDecl/{*}p").itertext())
    line_group_list = root.findall(".//{*}lg")
    title = root.find(".//{*}bibl/{*}title").text
    author = root.find(".//{*}bibl/{*}author").text

    manually_checked = 'manual' in analysis_description

    for stanza_number, line_group in enumerate(line_group_list):
        line_list = []
        poem_type = line_group.attrib["type"]
        for line in line_group:
            syllable_list = []
            poem_lines = []
            metrical_pattern = re.sub(r"[0-9]+", "+",
                                      line.attrib["met"].replace("|", ""))
            line_text = line[0].text
            poem_lines.append(
                {"line_text": line_text, "metrical_pattern": metrical_pattern})
            for word in line.findall(".//{*}w"):
                has_synalepha = False
                if re.match(r"[aeiouáéíóú]", word.text[-1]):
                    has_synalepha = True
                syllables = [*filter(bool, word.text.split("|"))]
                if has_synalepha:
                    syllable_list.append({
                                             "syllables": syllables,
                                             "has_synalepha": has_synalepha
                                         })
                else:
                    syllable_list.append({"syllables": syllables})
            line_list.append({
                                 "line_number": str(line.attrib["n"]),
                                 "text": line_text,
                                 "metrical_pattern": metrical_pattern,
                                 "words": syllable_list
                             })
        stanza_list.append({
                               "stanza_number": str(stanza_number + 1),
                               "type": poem_type, "lines": line_list
                           })
        poem.update({
                        "title": title, "author": author,
                        "manually_checked": manually_checked,
                        "stanzas": stanza_list
                    })
    return poem


def get_features(path):
    for filename in path.rglob('*.xml'):
        parse_xml(str(filename))

