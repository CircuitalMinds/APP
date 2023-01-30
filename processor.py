from os import system
from multiprocessing import Pool
from pathlib import Path
from string import ascii_lowercase
home_path = Path.home()
giturl = "https://github.com"
user = "circuitalmynds"


def gitclone(**kwargs):
    repo = kwargs.get("repo")
    path = kwargs.get("path")
    if repo and path:
        path = Path(str(path))
        if not path.is_dir():
            url = f"{giturl}/{user}/{repo}.git"
            system(
                f"git clone {url} {str(path)}"
            )
        else:
            print(f"{str(path)} already exists")


processes = [
    {
        "kwargs": {
            "repo": f"music_{letter}3",
            "path": f"{str(home_path)}/Videos/containers/{letter}3"
        },
        "func": gitclone
    }
    for letter in ascii_lowercase
]


def run_process(data):
    out, func = None, data.get("func")
    args, kwargs = data.get("args", ()), data.get("kwargs", {})
    if callable(func):
        out = func(*args, **kwargs)
    if out:
        print(out)
        return out


with Pool(len(processes)) as p:
    p.map(run_process, processes)
