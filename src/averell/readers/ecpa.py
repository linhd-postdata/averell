import json
import re
import xml.etree.ElementTree as ETree

from averell.utils import TEI_NAMESPACE as NS
from averell.utils import XML_NS

ECEP_NS = "{http://www.eighteenthcenturypoetry.org/ns}"


def get_poem_info(xml_file, lines_info, authors):
    """Poem parser for 'ECPA corpus'.
    We read the data and find elements like title, author, year, etc. Then
    we iterate over the poem text and we look for each stanza, line, word
    and syllable data.

    :param xml_file: Path for the poem xml file
    :param lines_info: Path for the lines json file
    :param authors: dict with authors info
    :return: Dict with the data obtained from the poem
    :rtype: dict
    """
    poem = {}
    tree = ETree.parse(xml_file)
    root = tree.getroot()
    manually_checked = False
    metadata = root.attrib
    title = root.find(f".//{NS}head[@type='main']")
    poem_id = metadata.get(f"{XML_NS}id")
    poem_info = authors[1].get(poem_id)
    if poem_info:
        title_text = poem_info.get("title")
    else:
        title_text = " ".join(word.text for word in title.findall(f"{NS}w"))
    author = root.find(f"{NS}link[@type='author']").get("target").split("#")[1]
    try:
        author_name = next(aut.get("name") for aut in authors[0].values() if
                           aut.get("author") == author)
    except StopIteration:
        author_name = author
    poem.update({
        "poem_title": title_text,
        "author": author_name,
    })
    alt_title = root.find(f".//{NS}head[@type='sub']")
    if alt_title:
        alt_title_text = re.sub(r"[\n ]+", " ",
                                "".join(alt_title.itertext())).strip()
        poem.update({"poem_alt_title": alt_title_text})

    line_group_list = root.findall(f".//{NS}lg")
    line_group_list2 = []
    for lg_number, lg in enumerate(line_group_list):
        if not lg.find(f".//{NS}lg"):
            if not lg.get("type") and not lg.get("met"):
                line_group_list2.append(lg)
            if lg.get("met"):
                line_group_list2.append(lg)
    stanza_list = []
    line_number = 0
    for stanza_number, line_group in enumerate(line_group_list2):
        stanza_type = None
        stanza_text = []
        line_list = []
        for n, line in enumerate(line_group.findall(f"{NS}l")):
            line_dict = {}
            line_id = line.attrib.get(f"{XML_NS}id")
            line_length = None
            met = None
            foot = None
            metre = None
            line_info = lines_info.get(line_id)
            if line_info is not None:
                if n == 0:
                    stanza_type = line_info.get("stanzas").get("id")
                syllab = line_info.get("syllab")
                line_length = int(syllab) if syllab else None
                met = line_info.get("met").strip("/") or None
                foot = line_info.get("foot").get("id")
                metre = line_info.get("footnum").get("id")
                real = line_info.get("real")
                if real:
                    manually_checked = True
                    met = real.strip("/")
                    foot = line_info.get("realfoot").get("id")
                    metre = line_info.get("realfootnum").get("id")
            line_dict.update({
                "metrical_pattern": met,
                "line_length": line_length,
                "foot": foot,
                "metre": metre,
            })
            word_list = []
            token_list = []
            for token in line:
                tag = token.tag
                if tag == f"{NS}w":
                    word_list.append({"word_text": token.text})
                if tag in [f"{NS}w", f"{NS}c", f"{NS}pc"]:
                    token_list.append(token.text or "")
            line_text = "".join(token_list).strip()
            line_dict.update({
                "line_number": line_number + 1,
                "line_text": "".join(line_text).strip(),
                "words": word_list,
            })
            line_list.append(line_dict)
            stanza_text.append(line_text)
            line_number += 1
        st = "\n".join(stanza_text)
        stanza_list.append({
            "stanza_number": stanza_number + 1,
            "stanza_type": stanza_type,
            "lines": line_list,
            "stanza_text": st,
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
    authors_file = path / "web" / "resources" / "models" / "authwork_mdp.json"
    authors = json.loads(authors_file.read_text())
    xml_files = path / "web" / "works"
    feature_list = []
    for filename in xml_files.rglob("*/*.xml"):
        folder = filename.parent
        lines_file = f"{filename.parts[-2]}_l.json"
        lines_path = folder / lines_file
        lines_info = json.loads(lines_path.read_text())
        result = get_poem_info(str(filename), lines_info, authors)
        feature_list.append(result)
    return feature_list
