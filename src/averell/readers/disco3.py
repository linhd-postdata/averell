from pathlib import Path

XML_PATH = Path("tei") / "all-periods-per-author"


def get_features(path):
    for filename in (Path(path) / XML_PATH).rglob('*.xml'):
        print(filename)
        return True
