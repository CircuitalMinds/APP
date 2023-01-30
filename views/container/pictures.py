from libs.shell import CLI
from .build import Container, getdate, Json
from .tools import getpath
from libs import root_path as base_path
from libs.utils import timeout


class Pictures(Container):
    root_path = getpath("home").joinpath("Pictures/containers")
    db_path = base_path.joinpath(
        f"db/container/pictures-files.json"
    )
    folders = list(i.name for i in root_path.iterdir() if i.is_dir())

    def __init__(self, folder):
        super().__init__(
            self.root_path, folder
        )
        self.info.content = []
        self.getdata()

    def getdata(self):
        self.info.content = []
        for yr in self.path.joinpath("photos").iterdir():
            if yr.is_dir():
                date = ["", "", yr.name.split("-")[0]]
                for month in list(yr.iterdir()):
                    date[1] = month.name
                    for file in month.iterdir():
                        date[0] = file.name.split("-")[0]
                        self.info.content.append(dict(
                            name=file.name,
                            size=file.stat().st_size * 1.0e-6,
                            path=str(file.relative_to(self.root_path)),
                            date="/".join(date)
                        ))
        self.info.total_size += sum(x["size"] for x in self.info.content)
        self.info.update()
        return self.info.data

    def isupdated(self, **timer):
        t = timer if timer else {"hours": 1}
        lastupdate = self.lastupdate.copy()
        date = getdate(self.db_path)
        for i in ("year", "month", "day"):
            if date[i] != lastupdate[i]:
                return False
        for i in t:
            if t[i] < abs(date[i] - lastupdate[i]):
                return False
        else:
            return True

    @staticmethod
    def get_worker(**timer):
        class Worker:
            @staticmethod
            def task():
                for i in Pictures.folders:
                    folder = Pictures(i)
                    if not folder.isupdated(**timer):
                        data = []
                        for v in Pictures.alldata().values():
                            data.extend(v["content"])
                        Json.save(Pictures.db_path, data)
                        print('Pictures Data Updated')
                        break

            def init(self):
                while True:
                    try:
                        timeout(self.task, 5)
                    except KeyboardInterrupt:
                        pass
        return Worker()

    @staticmethod
    def alldata():
        return {
            i: Pictures(i).info.data
            for i in Pictures.folders
        }

    def push(self):
        if self.info.ready_to_push:
            CLI.input(
                f"cd {self.root_path} && bash push {self.name}"
            )
