from multiprocessing import Pool
from os import system
from json import load
from pathlib import Path
app_home = Path.cwd()
settings = load(app_home.joinpath("settings.json").open())
processes = []


def run_task(i):
    process = processes[i]
    func, arg = process["func"], process.get("arg")
    if arg:
        func(arg)
    else:
        func()


def start_processes():
    with Pool(len(processes)) as p:
        p.map(run_task, range(len(processes)))


def getdata(*keys, values=settings):
    for key in keys:
        try:
            values = values.get(key)
        except AttributeError:
            pass
    return values


def gitclone(repo: dict):
    system(
        f'bash gitclone {getdata("git", "url")}/{repo["name"]} {repo["path"]}'
    )


class Build:

    @classmethod
    def init(cls):
        tasks = ("install", "folders")
        for task in tasks:
            getattr(cls, task)()
        start_processes()

    @staticmethod
    def folders():
        for repo in getdata("git", "repos"):
            path = app_home.joinpath(repo["path"])
            if not path.is_dir():
                processes.append({"func": gitclone, "arg": repo})

    @staticmethod
    def install():
        processes.append({"func": system, "arg": "bash install"})


if __name__ == "__main__":
    Build.init()
