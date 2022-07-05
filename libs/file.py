from json import load, dumps
from pathlib import Path


def openfile(fpath: str):
    file = Path(fpath).open()
    if fpath.endswith(".json"):
        data = load(file)
        if type(data) == list:
            return dict(enumerate(data))
        else:
            return data
    else:
        return file.read()


def writefile(fpath: str, text=None, **data):
    file = Path(fpath).open("w")
    if fpath.endswith(".json"):
        file.write(
            dumps(data, **dict(indent=4, sort_keys=True, ensure_ascii=False)
        ))
    elif type(text) == str:
        file.write(text)


class Json(dict):

    def __init__(self, fpath):
        super(dict).__init__()
        self.path = Path(fpath)
        self.open()

    def open(self):
        self.clear()
        if self.path.exists():
            self.update(openfile(str(self.path)))
        else:
            self.write()
        return self

    def write(self):
        writefile(str(self.path), **self)

