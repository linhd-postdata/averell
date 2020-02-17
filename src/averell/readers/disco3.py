import re
import xml.etree.ElementTree as ETree
from pathlib import Path

XML_PATH = Path("tei") / "all-periods-per-author"


# def parse_xml(xml_file):
#     """
#     Disco-3 corpus parser
#     :param xml_file: Path of the corpus file
#     :return:
#     """
#     tree = ETree.parse(xml_file)
#     root = tree.getroot()
#     line_group_list = root.findall(
#         ".//*{http://www.tei-c.org/ns/1.0}head/..[@type]/..{http://www.tei-c.org/ns/1.0}lg")
#
#     author = root.find(".//{http://www.tei-c.org/ns/1.0}author")
#     author = re.sub(r"[\n ]+", " ", author.text)
#
#     language = root.find(".//{http://www.tei-c.org/ns/1.0}language")
#     language = re.sub(r"[\n ]+", " ", language.text)
#
#     sonnet_list = []
#     id_list = []
#     is_ensemble = False
#     ensemble_dict = {}
#
#     for line_group in line_group_list:
#         if line_group.get("type") == "sonnet-sequence":
#             is_ensemble = True
#             ensemble_title = line_group.find(
#                 '{http://www.tei-c.org/ns/1.0}head')
#             ensemble_title = "".join(ensemble_title.itertext())
#             ensemble_id = line_group.get(
#                 "{http://www.w3.org/XML/1998/namespace}id")
#             ensemble_dict.update({
#                 'ensemble_id': ensemble_id,
#                 'ensemble_title': ensemble_title,
#             })
#             ensemble_alt_title = root.find(
#                 f".//*[@resource='disco:{ensemble_id}']"
#                 + "/{http://www.tei-c.org/ns/1.0}title[@property='dc:alternative']")
#             if ensemble_alt_title is not None:
#                 ensemble_alt_title = re.sub(r"[\n ]+", " ", "".join(
#                     ensemble_alt_title.itertext()))
#                 ensemble_dict.update({
#                     'ensemble_alt_title': ensemble_alt_title
#                 })
#             line_group.clear()
#         else:
#             work_dict = {}
#             if line_group.get("type"):
#                 sonnet_id = line_group.get(
#                     "{http://www.w3.org/XML/1998/namespace}id")
#                 work_dict.update({
#                     'poem_id': sonnet_id,
#                     'poem_type': line_group.get("type"),
#                     'author': author,
#                     'language': language,
#                 })
#                 id_list.append(work_dict["poem_id"])
#                 alt_title = root.find(
#                     f".//*[@resource='disco:{sonnet_id}']"
#                     + "/{http://www.tei-c.org/ns/1.0}title[@property='dc:alternative']")
#                 if alt_title is not None:
#                     alt_title = re.sub(
#                         r"[\n ]+", " ", "".join(alt_title.itertext()))
#                     work_dict.update({"poem_alt_title": alt_title})
#
#             line_number = 1
#             stanza_list = []
#             for stanza in line_group:
#                 stanza_dict = {}
#                 stanza_rhyme_pattern = []
#                 stanza_text = []
#                 if stanza.tag == "{http://www.tei-c.org/ns/1.0}head":
#                     work_dict.update({"poem_title": stanza.text, })
#                 else:
#                     stanza_dict.update({
#                         'stanza_number': stanza.attrib["n"],
#                         'stanza_type': stanza.attrib["type"],
#                     })
#                     line_list = []
#                     for line in stanza:
#                         line_dict = {}
#                         if line.get("met") is not None:
#                             line_text = re.sub(r"[\n ]+", " ",
#                                                "".join(line.itertext()))
#                             line_dict.update({
#                                 'line_number': str(line_number),
#                                 'line_text': line_text,
#                                 'metrical_pattern': line.attrib["met"],
#                                 'rhyme': line.attrib.get("rhyme", "None"),
#                             })
#
#                             stanza_text.append(line_text)
#                             if line_dict["rhyme"] != "None":
#                                 stanza_rhyme_pattern.append(
#                                     line.attrib["rhyme"])
#                             line_number += 1
#                             line_list.append(line_dict)
#
#                     if not stanza_rhyme_pattern:
#                         stanza_rhyme_pattern = "None"
#                     else:
#                         stanza_rhyme_pattern = "-".join(stanza_rhyme_pattern)
#                     stanza_dict.update({
#                         'rhyme_pattern': stanza_rhyme_pattern,
#                         'stanza_text': "\n".join(stanza_text),
#                         'lines': line_list,
#                     })
#                     stanza_list.append(stanza_dict)
#
#             work_dict.update({'stanzas': stanza_list})
#             sonnet_list.append(work_dict)
#     # End line groups
#     if is_ensemble:
#         id_list.sort()
#         for sonnet in sonnet_list:
#             sonnet.update(
#                 {"work_number": str(id_list.index(sonnet['poem_id']) + 1)})
#     for sonnet in sonnet_list:
#         sonnet_dict = {**ensemble_dict, **sonnet}
#         yield sonnet_dict

def parse_xml(xml_file):
    tree = ETree.parse(xml_file)
    root = tree.getroot()

    poem = {}
    stanza_list = []

    analysis_description = root.find(
        ".//{http://www.tei-c.org/ns/1.0}metDecl/{http://www.tei-c.org/ns/1.0}p").text
    title = root.find(
        ".//{http://www.tei-c.org/ns/1.0}head").text
    author = root.find(".//{http://www.tei-c.org/ns/1.0}author").text
    line_group_list = root.findall(".//*{http://www.tei-c.org/ns/1.0}lg")
    manually_checked = 'manual' in analysis_description
    alt_title = root.find(
        ".//*{http://www.tei-c.org/ns/1.0}bibl"
        "/{http://www.tei-c.org/ns/1.0}title[@property='dc:alternative']")
    poem.update({
        "manually_checked": manually_checked,
        "poem_title": title,
        "author": author,
    })
    if alt_title is not None:
        alt_title = re.sub(r"[\n ]+", " ", "".join(alt_title.itertext()))
        poem.update({"poem_alt_title": alt_title})
    line_number = 1
    for stanza_number, line_group in enumerate(line_group_list):
        line_list = []
        stanza_text = []
        for line in line_group:
            line_text = re.sub(r"[\n ]+", " ", "".join(line.itertext()))
            line_list.append({
                "line_number": line_number,
                "line_text": line_text,
                "metrical_pattern": line.get("met", "None")
            })
            stanza_text.append(line_text)
            line_number += 1
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

    :param path: path of the corpora folder
    """
    feature_list = []
    for filename in (Path(path)).rglob('*/per-sonnet/*.xml'):
        result = parse_xml(str(filename))
        feature_list.append(result)
    return feature_list
