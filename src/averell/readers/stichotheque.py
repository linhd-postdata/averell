import xml.etree.ElementTree as ETree

from averell.utils import TEI_NAMESPACE as NS

AOIDOS_NS = "{https://aoidos.ufsc.br/ns/1.0}"


def parse_xml(xml_file):
    """
    XML TEI poem parser for 'Stichotheque' corpus. In this corpus, we have a list
    of poems by author.
    We read the data and find elements like title, author, etc with XPath
    expressions.
    Then, we iterate over the poem text and we look for each stanza and line
    data.
    :param xml_file: Path for the xml file
    :return: Poem python dict with the data obtained
    """
    tree = ETree.parse(xml_file)
    root = tree.getroot()
    corpus_name = xml_file.parts[-4]
    manually_checked = False
    alt_title = root.find(f"{NS}teiHeader/{NS}fileDesc/{NS}titleStmt/{NS}title")
    text = root.find(f"{NS}text")
    author = text.get(f"{AOIDOS_NS}poet")
    poem_list = text.find(f"{NS}body").findall(f"{NS}div")
    for p_index, poem in enumerate(poem_list):
        if poem.get("type") != "poem" or poem.get(f"{AOIDOS_NS}unit") == "children":
            continue
        poem_dict = {}
        head = poem.find(f"{NS}head")
        title = head.text if head is not None else f"{alt_title.text}-{p_index}"
        stanza_list = []
        line_number = 0
        line_group_list = poem.findall(f"{NS}lg")
        for stanza_number, line_group in enumerate(line_group_list):
            line_list = []
            stanza_text = []
            for line in line_group.findall(f"{NS}l"):
                choice = line.find(f"{NS}choice")
                if choice is not None:
                    # keep only the original text
                    choice.remove(choice.find(f"{NS}seg"))
                line_meter = line.get(f"{AOIDOS_NS}meter")
                if line_meter is not None and line_meter != "ignore":
                    meter = line_meter
                else:
                    meter = poem.get(f"{AOIDOS_NS}meter")
                line_text = "".join(line.itertext()).strip()
                line_list.append({
                    "line_number": line_number + 1,
                    "line_text": line_text,
                    "line_length": meter,
                })
                stanza_text.append(line_text)
                line_number += 1
            stanza_list.append({
                "stanza_type": None,
                "stanza_number": stanza_number + 1,
                "lines": line_list,
                "stanza_text": "\n".join(stanza_text),
            })
        if len(stanza_list) > 0:
            poem_dict.update({
                "poem_title": title,
                "corpus": corpus_name,
                "manually_checked": manually_checked,
                "author": author,
                "stanzas": stanza_list
            })
            yield poem_dict


def get_features(path):
    """
    Function to find each poem file and parse it
    :param path: Corpus Path
    :return: List of poem dicts
    """
    feature_list = []
    path = path / "stichotheque-pt-master" / "xml"
    for filename in path.rglob('*.xml'):
        result = list(parse_xml(filename))
        feature_list.extend(result)
    return feature_list
