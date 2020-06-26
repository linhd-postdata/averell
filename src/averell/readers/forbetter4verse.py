import re

from lxml import etree

from averell.utils import TEI_NAMESPACE as NS


def parse_xml(xml_file):
    """Poem parser for 'For better for verse' corpus.
    We read the data and find elements like title, author, year, etc. Then
    we iterate over the poem text and we look for each stanza and  line data.

    :param xml_file: Path for the poem xml file
    :return: Dict with the data obtained from the poem
    :rtype: dict
    """
    poem = {}
    tree = etree.parse(xml_file)
    root = tree.getroot()
    nsmap = root.nsmap
    tei_url = NS.replace("{", "").replace("}", "")
    if not any(ns == tei_url for ns in nsmap.values()):
        # no TEI declaration in input file, cannot parse file
        return
    manually_checked = False
    title = root.find(f".//{NS}title").text
    author = root.find(f".//{NS}author")
    author_text = "unknown"
    if author is not None:
        author_text = author.text
    date = root.find(f".//{NS}date")
    year = None
    if date is not None:
        year = root.find(f".//{NS}date").text
    poem.update({
        "poem_title": title,
        "author": author_text,
        "year": year
    })
    line_group_list = root.findall(f".//{NS}lg")
    stanza_list = []
    line_number = 0
    for stanza_number, line_group in enumerate(line_group_list):
        stanza_type = line_group.get("type")
        line_list = []
        stanza_text = []
        for line in line_group.findall(f"{NS}l"):
            line_dict = {}
            line_length = None
            met = line.get("met")
            foot = None
            metre = None
            real = line.get("real")
            if real is not None:
                # "manually_checked" is a poem feature, so if one line
                # has real attrib the poem will be manually_checked=True
                manually_checked = True
                met = real
            seg_list = [re.sub(r"[\n ]+", " ", seg.xpath("string()")) for seg in
                        line.findall(f"{NS}seg")]
            line_text = "".join(seg_list)
            line_dict.update({
                "line_number": line_number + 1,
                "line_text": line_text,
                "metrical_pattern": met,
                "line_length": line_length,
                "foot": foot,
                "metre": metre,
            })
            line_list.append(line_dict)
            stanza_text.append(line_text)
            line_number += 1
        stanza_list.append({
            "stanza_number": stanza_number + 1,
            "stanza_type": stanza_type,
            "lines": line_list,
            "stanza_text": "\n".join(stanza_text),
        })
    poem.update({
        "manually_checked": manually_checked,
        "stanzas": stanza_list
    })
    return poem


def get_features(path):
    """Function to find each poem file and parse it

    :param path: Corpus Path
    :return: List of poem dicts
    :rtype: list
    """
    xml_folders = [path / "poems", path / "poems2"]
    feature_list = []
    for folder in xml_folders:
        # exclude example xml files
        for filename in folder.glob("[!Poet - ]*.xml"):
            result = parse_xml(str(filename))
            if result is not None:
                feature_list.append(result)
    return feature_list
