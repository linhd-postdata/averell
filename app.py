import copy
import json

from pathlib import Path
from zipfile import ZipFile

import gradio as gr
import pycountry

from averell.utils import get_ids, CORPORA_SOURCES
from averell.core import export_corpora_ui, get_corpora

PARAMS = {
    "granularity": "poem",
    "ouput_format": "JSON",
    "corpora_list": [
        'bibit', 'stichopt', 'disco2_1',
        'disco3', 'adso', 'adso100',
        'plc', 'gongo', 'ecpa',
        '4b4v', 'czverse', 'mel'
    ],
}

def get_available_languages(sources):
    available_languages = []
    for c in sources:
        lang = c["properties"]["language"]
        if lang not in available_languages:
            available_languages.append(lang)
    return available_languages

def filter_corpus_language(sources, lang):
    corpora_sources = copy.deepcopy(sources)
    filtered_corpora = [c for c in corpora_sources if c["properties"]["language"] == lang]
    return filtered_corpora

available_languages = get_available_languages(CORPORA_SOURCES)

with gr.Blocks() as app_averell:
    def export_corpora(output_path, output_format, output_granularity):
        corpora_list = PARAMS["corpora_list"]
        #print(corpora_list)
        output_path = output_path["label"]
        filename = f"tmp/{output_format}.zip"
        if output_granularity == "JSON":
            with ZipFile(filename, "w") as zfile:
                for corpus in corpora_list:
                    p = Path(f'{output_path}/{output_format}/{corpus}')
                    print(corpus)
                    for f in p.glob("**/*.json"):
                        #print(f)
                        zfile.write(f)
            return f"tmp/{output_format}.zip"
        else:
            json_l, filename = export_corpora_ui(get_ids(corpora_list),
                                                 "stanza",
                                                 "tmp/tmp_corp",
                                                 None,
                                                 False)
            with open(f"tmp/{filename}.json", 'w', encoding='utf-8') as f:
                json.dump(json_l, f, ensure_ascii=False, indent=4)
            return f"tmp/{filename}.json"

    def block_granularity(rad_format): 
        if rad_format == "TEI":
            PARAMS["ouput_format"] = rad_format
            return {rad_granularity: gr.update(value="poem", visible=False)}
        else:
            PARAMS["ouput_format"] = rad_format
            return {rad_granularity: gr.update(value="poem", visible=True)}

    def update_granularity(value):
        PARAMS["granularity"] = value
        true_l = [gr.Checkbox.update(value=True, visible=True)] 
        false_l = [gr.Checkbox.update(value=False, visible=False)]
        if value == "word":
            # 000011100110 + 110110
            corp_list = false_l*4 + true_l*3 + false_l*2 + true_l*2 + false_l
            lang_list = true_l*2 + false_l + true_l*2 + false_l
            return corp_list + lang_list
        elif value == "syllable":
            # 000011000000 + 100000
            corp_list = false_l*4 + true_l*2 + false_l*6
            lang_list = true_l + false_l*5
            return corp_list + lang_list
        else:
            #return None
            return [gr.Checkbox.update(value=True, visible=True)]*18

    def change_selection(value):
        return value

    def update_corpora_list(added, corpus):
        corpora_list = PARAMS["corpora_list"]
        if corpus in corpora_list and not added:
            corpora_list.remove(corpus)
        elif corpus not in corpora_list and added:
            corpora_list.append(corpus)

    app_title = gr.HTML("<h1>Averell</h1>")
    with gr.Row() as row:

        with gr.Column(scale=1) as c1:
            rad_format = gr.Radio(["TEI", "JSON"], label="Output", info="Choose output format", value="TEI", interactive=True)
            rad_granularity = gr.Radio(["poem", "stanza", "line", "word", "syllable"],
                                       label="Granularity",
                                       info="Choose output granularity",
                                       value="poem",
                                       interactive=True,
                                       visible=False,
                                       )
            corpus_checkboxes = []
            lang_checkboxes = []
            for lang in available_languages:
                language = pycountry.languages.get(alpha_2=lang).name
                with gr.Blocks() as corpora:
                    lang_chk = gr.Checkbox(True, label=language, interactive=True)
                    filtered_corpus = filter_corpus_language(CORPORA_SOURCES, lang)
                    for corpus in filtered_corpus:
                        classes = corpus["properties"]["granularity"]
                        classes.append("poem")
                        classes.append(lang)
                        chk = gr.Checkbox(True,
                                          label=corpus["name"],
                                          info=f'License: {corpus["properties"]["license"]} | Number of poems: {corpus["properties"]["doc_quantity"]}',
                                          interactive=True,
                                          elem_classes=classes,
                                          elem_id=corpus["properties"]["slug"],
                                          )
                        label = gr.Textbox(value=corpus["properties"]["slug"], visible=False)
                        lang_chk.change(change_selection, lang_chk, chk, show_progress=True)
                        chk.change(update_corpora_list, [chk, label], show_progress=True)
                        corpus_checkboxes.append(chk)
                    lang_checkboxes.append(lang_chk)
        with gr.Column(scale=1) as c2:

            rad_granularity.change(update_granularity, rad_granularity, [*corpus_checkboxes,*lang_checkboxes], show_progress=True)
            rad_format.change(block_granularity, rad_format, rad_granularity, api_name="output_format", show_progress=True)
            exp_btn = gr.Button("Export")
            folder_path = gr.Label(value="tmp/", visible=False)
            out_file = gr.File()
            exp_btn.click(export_corpora, [folder_path, rad_format, rad_granularity], out_file, api_name="export")

app_averell.launch(share=True)