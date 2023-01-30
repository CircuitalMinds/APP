import asyncio
from os import kill, getpid
from signal import SIGINT
from subprocess import getoutput
import threading
import socket
from pathlib import Path
from os import walk
from os.path import getctime
from time import ctime
from json import load, dumps
from yaml import full_load
from csv import DictReader
from time import sleep
from .shell import CLI

jsonconfig = dict(
    indent=4,
    sort_keys=True,
    ensure_ascii=False
)


def parent_path(filepath):
    return Path(str(filepath)).parent


def not_found_error(func, path):
    value = None
    try:
        value = func()
    except FileNotFoundError:
        if not path.parent.is_dir():
            print(f"Directory {str(path.parent.absolute())} not found")
        else:
            print(f"File {str(path.name)} not found in {str(path.parent.absolute())}")
    return value


def get_host():
    return getoutput("hostname -I").strip()


def openfile(filepath):
    filepath = Path(filepath)
    return not_found_error(lambda: filepath.open(), filepath)


def writefile(filepath, data):
    filepath = Path(str(filepath))

    def writer():
        filepath.open("w").write(data)
    not_found_error(writer, filepath)


def getfilesize(filepath):
    filepath = Path(str(filepath))

    def stat():
        return filepath.stat().st_size * 1.0e-6
    return not_found_error(stat, filepath)


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


def iter_folder(fpath):
    data = {}
    ignore = ("info.json", "venv", "__pycache__", ".git")

    def getdata(from_root, dir_paths, file_paths):
        for i in from_root.split("/"):
            if i in ignore or i.startswith("."):
                return
        data[from_root.split(str(fpath.joinpath("application")))[-1]] = dict(
            dirs=[
                di for di in dir_paths
                if di not in ignore and not di.startswith(".")
            ],
            files=[
                fi for fi in file_paths
                if fi not in ignore and not fi.startswith(".")
            ],
        )
    for (root, dirs, files) in walk(fpath, topdown=True):
        getdata(root, dirs, files)
    return data


def get_copy(filepath, path, name=None):
    x_path = str(filepath)
    y_path = Path(path).joinpath(name) if name else path
    CLI.input(f"cp -r -u {x_path} {y_path}")


def dumper(datastr: str, **config):
    settings = jsonconfig.copy()
    settings.update(config)
    return dumps(datastr, **settings)


def getjson(filepath):
    return load(Path(str(filepath)).open())


def get_yaml(filepath):
    return full_load(Path(str(filepath)).open())


def save_json(filepath, data, **config):
    Path(str(filepath)).open("w").write(dumper(data, **config))


def opencsv(filepath):
    return [
        row for row in DictReader(
            Path(str(filepath)).open()
        )
    ]


def timeout(func, secs):
    sleep(secs)
    func()


def get_directory_struct(fpath):
    fpath = Path(str(fpath))
    filepath = fpath.joinpath("directory.json")
    ignore = (
        ".git", ".idea", "venv", "__pycache__"
    )
    dirs = []
    for i in fpath.iterdir():
        if i.name not in ignore and i.is_dir():
            dirs.append(i.name)
    CLI.input(
        f"tree -f --du -J {' '.join(dirs)} -o {str(filepath)}", getout=True
    )
    data = getjson(filepath)
    report = list(filter(lambda x: x.get("type") == "report", data))[0]
    report["size"] *= 1.0e-6
    print(report)
    return data


def pyrun(path, *opts):
    path = Path(str(path))
    goto = f"cd {str(path.parent)}"
    runscript = "python3 -m {name} {opts}".format(
        name=path.name.split(".py")[0],
        opts=" ".join([str(opt) for opt in opts])
    )
    CLI.input(f"{goto} && {runscript}")


def scanports(*ports, **kwargs):
    checklist = ports
    port_range = tuple(kwargs[i] for i in ("start_port", "end_port") if i in kwargs)
    if len(port_range) == 2:
        checklist += tuple(range(*port_range))
    portlist = []
    init_thread = threading.Thread

    def scan(port_number):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            if s.connect_ex((target, port_number)) == 0:
                portlist.append(port_number)
                print(f"Port {port_number} is open." + "\t" * 10)

            print(f"Current port: {port_number}" + "\t", end="\r")
            s.close()
        except ConnectionError:
            pass

    target = ""
    thd = [init_thread(target=scan, kwargs={'port_number': i}) for i in checklist]
    for t in thd:
        t.start()
        t.join()
    return portlist


def open_vlc(filepath):
    CLI.input(f"vlc -q {filepath}")


def async_loop(funcs, *args):
    fn = (lambda: func(*args[i]) for i, func in enumerate(funcs))
    asyncio.get_event_loop()

    async def outer():
        print('in outer')
        print('waiting for result 1')
        result1 = await phase1()
        print('waiting for result 2')
        result2 = await phase2(result1)
        return result1, result2

    async def phase1():
        print('in phase1')
        return 'phase1 result'

    async def phase2(arg):
        print('in phase2')
        return 'result2 derived from {}'.format(arg)

    asyncio.run(outer())
    return fn


def run_process(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except KeyboardInterrupt:
        pass


def get_processes():
    info = []
    data = CLI.input("lsof -i:8080", getout=True)
    keyvalues = data[0].lower().split()
    for x in data[1:]:
        y = dict()
        for k, v in zip(keyvalues, x.split()):
            y[k] = v
        info.append(y)
    return info


def kill_process(pid=None, clean=True):
    if pid:
        kill(int(pid), SIGINT)
    elif clean:
        for proc in get_processes():
            kill(proc["pid"], SIGINT)
    else:
        kill(getpid(), SIGINT)
