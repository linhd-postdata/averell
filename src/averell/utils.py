import os
import urllib.request
from zipfile import ZipFile

CORPORA_SOURCES = {
    1: "https://github.com/pruizf/disco/archive/master.zip",
    2: "https://github.com/pruizf/disco/archive/v3.zip",
    3: "https://github.com/bncolorado/CorpusSonetosSigloDeOro/archive/master.zip",
    4: "https://github.com/bncolorado/CorpusGeneralPoesiaLiricaCastellanaDelSigloDeOro/archive/master.zip",
    5: "https://github.com/dracor-org/spandracor/archive/master.zip",
}


def get_corpora(corpus_index_list=[*CORPORA_SOURCES], output_folder="corpora"):
    for index in corpus_index_list:
        file_name, _ = urllib.request.urlretrieve(CORPORA_SOURCES[index])
        with ZipFile(file_name, 'r') as zipObj:
            zipObj.extractall(output_folder)
        os.remove(file_name)
