from libs.utils import getdate, save_json, CLI
from pathlib import Path
from os.path import join
from multiprocessing import Pool
env = CLI.env["app-env"]
processes = []


def run_process(i):
    processes[i]()


class Info:

    def __init__(self, path):
        self.path = Path(str(path)).joinpath("info.json")
        self.available_space = True
        self.totalsize = 0.0
        self.content = []
        self.ready_to_push = True
        self.data = dict()
        self.lastupdate = getdate(path, formatted=True)

    def update(self):
        if self.content:
            self.checkout()
            self.data = dict(
                content=self.content,
                total_size=self.totalsize,
                available_space=self.available_space,
                ready_to_push=self.ready_to_push,
                lastupdate=getdate(formatted=True)
            )
            save_json(self.path, self.data, ensure_ascii=True)

    def checkout(self):
        if not self.content:
            self.ready_to_push = False
            return
        self.totalsize = 0.0
        for i in self.content:
            size = i.get("size")
            self.totalsize += size
            if size > 95.0 and i.get("filename"):
                self.ready_to_push = False
            if self.totalsize > 9.5e2:
                self.available_space = False
            if self.totalsize > 1.05e3:
                self.ready_to_push = False


class Container:

    def __init__(self, root, name):
        self.path = Path(root).joinpath(name)
        self.name = self.path.name
        self.info = Info(self.path)


class Videos(Container):
    root = Path.home().joinpath("Videos/containers")
    ids = [i for i in root.iterdir() if i.is_dir()]

    def __init__(self, folder):
        super().__init__(self.root, folder)
        self.url_root = join(
            env["GIT-URL"], "circuitalmynds",
            f"music_{folder}", "blob/main/videos"
        )

    def getdata(self):
        self.info.content.clear()
        files = get_files(self.path.joinpath("videos"))
        for i in files:
            if i["filename"].endswith(".mp4"):
                i["id"] = i.get("filename").split(".mp4")[0][-11:]
                i["url"] = f'{self.url_root}/{i["filename"]}?raw=true'
                self.info.content.append(i)
        self.info.update()
        return self.info.data

    @staticmethod
    def update_all():
        processes.clear()

        def add_process(arg):
            def func():
                CLI.input(f"cd {Videos.root} && bash push {arg}")
            processes.append(func)

        alldata = dict()
        for ident in Videos.ids:
            cont = Videos(ident)
            alldata[ident] = cont.getdata()
            if alldata[ident]["ready_to_push"]:
                add_process(cont.name)
        with Pool(len(processes)) as p:
            try:
                p.map(run_process, range(len(processes)))
            except KeyboardInterrupt:
                print("Exiting Processes")
        return alldata


class Pictures(Container):
    root = Path.home().joinpath("Pictures/containers")
    ids = [i for i in root.iterdir() if i.is_dir()]

    def __init__(self, folder):
        super().__init__(self.root, folder)
        self.url_root = join(
            env["GIT-URL"], "alanmatzumiya",
            f"pictures_{folder}", "blob/main/photos"
        )

    def getdata(self):
        self.info.content.clear()
        root_folder = self.path.joinpath("photos")
        for yr in (i for i in root_folder.iterdir() if i.name != ".nothing"):
            ydata = dict()
            size = 0.0
            for month in yr.iterdir():
                ydata[month.name] = get_files(month)
                for yi in ydata[month.name]:
                    size += yi["size"]
                    yi["url"] = yi["path"].replace(
                        str(root_folder), self.url_root
                    ) + "?raw=true"
            if ydata:
                ydata["size"] = size
                self.info.content.append(ydata)
        self.info.update()
        return self.info.data