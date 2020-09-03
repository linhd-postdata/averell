import re
import xml.etree.ElementTree as ETree

from averell.utils import TEI_NAMESPACE as NS


class CommentedTreeBuilder(ETree.TreeBuilder):
    def comment(self, data):
        self.start(ETree.Comment, {})
        self.data(data)
        self.end(ETree.Comment)


def parse_xml(xml_file):
    """
    XML TEI poem parser for 'Poesía Lírica Castellana Siglo de Oro' corpus.
    We read the data and find elements like title, author, etc with XPath
    expressions.
    Then, we iterate over the poem text and we look for each stanza, line, word
    and syllable data.
    :param xml_file: Path for the xml file
    :return: Poem python dict with the data obtained
    """
    custom_xmlparser = ETree.XMLParser(target=CommentedTreeBuilder())
    poem = {}
    tree = ETree.parse(xml_file, parser=custom_xmlparser)
    root = tree.getroot()
    stanza_list = []
    analysis_description = "".join(
        root.find(f".//*{NS}metDecl/{NS}p").itertext())
    line_group_list = root.findall(f".//{NS}lg")
    title = root.find(f".//{NS}bibl/{NS}title").text
    author = root.find(f".//{NS}bibl/{NS}author").text

    manually_checked = 'manual' in analysis_description

    for stanza_number, line_group in enumerate(line_group_list):
        line_list = []
        poem_type = line_group.attrib["type"]
        stanza_text = []
        for line in line_group:
            word_list = []
            poem_lines = []
            metrical_pattern = re.sub(
                r"[0-9]+", "+", line.attrib["met"].replace("|", ""))
            line_text = line[0].text
            poem_lines.append(
                {"line_text": line_text, "metrical_pattern": metrical_pattern})
            stanza_text.append(line_text)
            for word in line.findall(f".//{NS}w"):
                word_dict = {}
                has_synalepha = False
                if re.match(r"[aeiouáéíóú]", word.text[-1]):
                    has_synalepha = True
                syllables = [*filter(bool, word.text.split("|"))]
                word_dict.update({
                    "word_text": "".join(syllables),
                    "syllables": syllables
                })
                if has_synalepha:
                    word_dict.update({"has_synalepha": True})
                word_list.append(word_dict)
            line_list.append({
                "line_number": str(line.attrib["n"]),
                "line_text": line_text,
                "metrical_pattern": metrical_pattern,
                "words": word_list
            })
        stanza_list.append({
            "stanza_number": str(stanza_number + 1),
            "stanza_type": poem_type, "lines": line_list,
            "stanza_text": "\n".join(stanza_text),
        })
    poem.update({
        "poem_title": title,
        "author": author,
        "manually_checked": manually_checked,
        "stanzas": stanza_list
    })
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
