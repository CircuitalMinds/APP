from os import system
from flask import request, send_file
from werkzeug.utils import secure_filename
from pathlib import Path
from json import dumps
home = Path.home()


class Container:
    class Info(dict):

        def __init__(self, obj):
            super(dict, self).__init__()
            self.path = obj.path.joinpath("info.json")
            self.update(dict({i: getattr(obj, i, None) for i in (
                "available_space", "total_size", "content"
            )}))
            self.update(dict(ready_to_push=True))
            if self.get("total_size") > 1.05e3:
                self.update(dict(ready_to_push=False))
            elif any([file["size"] > 53.0 for file in self.get("content")]):
                self.update(dict(ready_to_push=False))

        def save(self):
            self.path.open("w").write(dumps(
                self, indent=4, sort_keys=True, ensure_ascii=False
            ))

    def __init__(self, root, name):
        self.name = name
        self.path = home.joinpath(root, self.name)
        self.total_size = 0.0
        self.available_space = True

    def save_file(self, folder):
        if self.path.joinpath(folder).is_dir():
            files = request.files.getlist('files[]')
            for file in files:
                file.save(self.path.joinpath(
                    folder, secure_filename(file.filename)
                ))

    def getfile(self, filepath):
        file = self.path.joinpath(filepath)
        return send_file(
            file.absolute(), download_name=file.name.strip()
        )


class Videos(Container):
    folders = list(i.name for i in home.joinpath("Videos/containers").iterdir())

    def __init__(self, folder):
        super().__init__(
            "Videos/containers", folder
        )
        self.url_root = f"https://github.com/circuitalmynds/music_{folder}/blob/main/videos"
        self.content = []
        self.getdata()
        self.available_space = self.total_size < 9.5e2
        self.info = self.Info(self)

    def getdata(self):
        files = list(self.path.joinpath("videos").iterdir())
        for file in files:
            self.content.append(dict(
                name=file.name,
                size=file.stat().st_size * 1.024e-6,
                path=str(file.relative_to(home.joinpath(
                    "Videos/containers"
                ))),
                url=f"{self.url_root}/{file.name}?raw=true"
            ))
        self.total_size += sum(i["size"] for i in self.content)

    def push(self):
        if self.info.get("ready_to_push"):
            system(" && ".join([
                f'cd {home.joinpath("Videos")}',
                f'bash push {self.name}'
            ]))

    @staticmethod
    def update_all():
        data = []
        for i in Videos.folders:
            v = Videos(i)
            v.info.save()
            v.push()
            data.extend(v.content)
        Path.cwd().joinpath("containers/videos/files.json").open("w").write(
            dumps(
                data, indent=4, sort_keys=True, ensure_ascii=False
            )
        )
        return data


class Pictures(Container):
    folders = list(i.name for i in home.joinpath("Pictures/containers").iterdir())

    def __init__(self, folder):
        super(Pictures, self).__init__(
            "Pictures/containers", folder
        )
        self.content = dict()
        self.getdata()
        self.available_space = self.total_size < 9.5e2
        self.info = self.Info(self)

    def getdata(self):
        self.content.clear()
        yrs = list(i for i in self.path.joinpath("photos").iterdir() if i.is_dir())
        for yr in yrs:
            self.content[yr.name] = dict()
            months = list(yr.iterdir())
            for month in months:
                self.content[yr.name][month.name] = []
                for file in month.iterdir():
                    self.content[yr.name][month.name].append(dict(
                        name=file.name,
                        size=file.stat().st_size * 1.024e-6,
                        path=str(file.relative_to(home.joinpath("Pictures/containers")))
                    ))
                self.total_size += sum(
                    i["size"] for i in self.content[yr.name][month.name]
                )

    @staticmethod
    def update_all():
        data = []
        for i in Pictures.folders:
            pics = Pictures(i)
            pics.info.save()
            for y in pics.content:
                for m in pics.content[y]:
                    data.extend(pics.content[y][m])
        Path.cwd().joinpath("containers/pictures/files.json").open("w").write(
            dumps(
                data, indent=4, sort_keys=True, ensure_ascii=False
            )
        )
        return data
