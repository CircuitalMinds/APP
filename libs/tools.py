from libs.shell import CLI
from os.path import getctime, join
from time import ctime
from pathlib import Path
from sys import argv


def getargs(**opts):
    first, expected = (opts.get(opt) for opt in ("first", "expected"))
    data = [i for i in argv[1:] if i in expected] if expected else argv[1:]
    if not data:
        return
    else:
        return data[0] if first else data


if arg := getargs(
    first=True,
    expected=["install", "app", "site"]
):
    CLI.input("clear")
    if arg == "site":
        pass
    else:
        pass



def filterlist(data, **opts):
    funcs, filtered = (), []
    skips, keywords, func = (opts.get(i) for i in ("skips", "keywords", "func"))
    if skips:
        func += (lambda i: i not in skips, )
    if keywords:
        funcs += (lambda i: i in keywords, )
    if func:
        funcs += (func, )
    return list(filter(
        lambda i: all([f(i) for f in funcs]), data
    ))


def getdate(filepath=None):
    data = []
    if filepath:
        data.extend(ctime(getctime(Path(str(filepath)))).split())
    else:
        data.extend(ctime().split())
    date = filterlist(data, func=lambda e: e != "")
    t = date[3].split(":")
    return dict(
        day=int(date[2]), month=date[1], year=int(date[4]),
        hours=int(t[0]), minutes=int(t[1]), seconds=int(t[2])
    )



def filesearch(dpath, **opts):
    files, filters = [], []
    if opts.get("keywords"):
        words = [s.lower() for s in opts.get("keywords")]
        filters.append(filterlist(
            lambda word: word in words, words
        ))

    if opts.get("ext"):
        filters.append(lambda file: file.endswith(opts.get("ext")))
    if opts.get("by_size"):
        files.extend(list(filter(
            lambda file: all(g(file) for g in filters),
            CLI.input(f"find {str(dpath)} -size {opts.get('by_size')}", getout=True)
        )))
    else:
        files.extend(filter(
            lambda file: all(g(file) for g in filters),
            [str(i) for i in Path(str(dpath)).iterdir()]

        ))
    return files



def check_folder_size(folder, limit):
    folder_name = join(*str(folder).split("/")[-2:])
    infopath = Path.home().joinpath("App/checkout/videos.json")
    info = getjson(infopath)
    files, totalsize = [], 0.0
    data = list(filter(
        lambda x: x.endswith(".mp4"),
        CLI.input(f"find {str(folder)} -size {limit}", getout=True)
    ))
    for i in data:
        file = Path(i)
        path, size = str(file), getfilesize(file)
        files.append(dict(path=path, size=size))
        totalsize += size
    info[folder_name] = dict(files=files, totalsize=totalsize)
    save_json(infopath, info)

