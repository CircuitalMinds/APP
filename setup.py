from pathlib import Path
from libs.utils import CLI


def copy_dir(path, to_path):
    path = Path(str(path))
    to_path = Path(str(to_path))
    if path.is_dir() and to_path.exists():
        for xpath in path.iterdir():
            CLI.input(f"cp -r -u ./{xpath} ./{to_path}")
    elif path.exists():
        CLI.input(f"cp -r -u ./{path} ./{to_path}")
    else:
        print(f"{path}: No such file or directory")


def rename_dir(path, new_path):
    path = Path(str(path))
    new_path = Path(str(new_path))
    if path.exists():
        if not new_path.exists():
            path.rename(str(new_path))
        else:
            dirtype = "directory" if new_path.is_dir() else "file"
            name = new_path.name
            parent = new_path.parent
            print(f"{dirtype} with name {name} already exists in {parent}")
    else:
        print(f"{path}: No such file or directory")


def directory_filter(path, **kwargs):
    path, filtered = Path(str(path)), []
    cont = list(path.iterdir())
    funcs = []
    datatype = kwargs.get("datatype")
    minsize, maxsize = (kwargs.get(i) for i in ("minsize", "maxsize"))
    if minsize:
        funcs.append(lambda x:  minsize < x.stat().st_size * 1.0e-6)
    if maxsize:
        funcs.append(lambda x: x.stat().st_size * 1.0e-6 < maxsize)
    if datatype == "file":
        funcs.append(lambda x: x.is_file())
    if datatype == "dir":
        funcs.append(lambda x: x. is_dir())
    if "keywords" in kwargs:
        funcs.append(lambda x: any([w.lower() in str(x).lower() for w in kwargs["keywords"]]))
    for i in ("startswith", "endswith"):
        if i in kwargs:
            funcs.append(lambda x: getattr(str(x), i)(kwargs[i]))
    for xi in cont:
        is_target = True
        for fi in funcs:
            if not fi(xi):
                is_target = False
                break
        if is_target:
            yi = str(xi)
            filtered.append(yi)
            print(yi)
    print(len(filtered))

