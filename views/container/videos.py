from libs import root_path, Path
from libs.utils import CLI, getjson, save_json, timeout
from .build import Container
giturl = "https://github.com/circuitalmynds"
home_path = Path.home()


class Videos(Container):
    containers_path = home_path.joinpath("Videos/containers")
    handler_path = home_path.joinpath("Videos/handler")
    ids = list(i.name for i in containers_path.iterdir() if i.is_dir())

    def __init__(self, folder_id):
        super().__init__(
            self.containers_path, folder_id
        )
        self.url_root = f"{giturl}/music_{folder_id}/blob/main/videos"
        self.info.content = []

    def getdata(self):
        self.info.content = []
        files = list(self.path.joinpath("videos").iterdir())
        for file in files:
            self.info.content.append(dict(
                name=file.name,
                id=file.name.split(".mp4")[0][-11:],
                size=file.stat().st_size * 1.0e-6,
                path=str(file),
                url=f"{self.url_root}/{file.name}?raw=true"
            ))
        self.info.totalsize += sum(i["size"] for i in self.info.content)
        self.info.data = dict(content=self.info.content, total_size=self.info.totalsize)
        return self.info.data

    def get_video_metadata(self, yt, video_id):
        metadata = yt.get_metadata(video_id)
        data = dict.fromkeys(["title", "description", "duration", "image", "keywords"], "")
        to_title = [
            ("name", "title", "twitter:title"),
            ("property", "og:title"),
            ("itemprop", "name")
        ]
        to_description = [
            ("name", "description", "twitter:description"),
            ("property", "og:description"),
            ("itemprop", "description")
        ]
        to_image = [
            ("name", "twitter:image"),
            ("property", "og:image")
        ]
        for m in to_title:
            meta = list(filter(lambda x: x[m[0]] in m[1:], metadata[m[0]]))
            if meta:
                data["title"] = meta[0]["content"]
                break
        for m in to_description:
            meta = list(filter(lambda x: x[m[0]] in m[1:], metadata[m[0]]))
            if meta:
                data["description"] = meta[0]["content"]
                break
        for m in to_image:
            meta = list(filter(lambda x: x[m[0]] in m[1:], metadata[m[0]]))
            if meta:
                data["image"] = meta[0]["content"]
                break
        keywords = list(filter(lambda x: x["name"] == "keywords", metadata["name"]))
        time = list(filter(lambda x: x["itemprop"] == "duration", metadata["itemprop"]))
        if time:
            t = time[0]["content"].split("PT")[-1]
            for q, p in [("M", ":"), ("S", "")]:
                t = t.replace(q, p)
            data["duration"] = t.replace(":", ":0") if len(t.split(":")[-1]) == 1 else t
        if keywords:
            data["keywords"] = keywords[0]["content"]
        return data


def get_waiting_handler():
    class Waiting:
        path = Path.home().joinpath("Videos/handler/waiting")
        containers_path = Path.home().joinpath("Videos/containers")
        files = [i for i in filter_by_size(path, lambda x: x < 95.0) if i["name"].endswith(".mp4")]
        ignores = filter_by_size(path, lambda x: x > 95.0)

        def __init__(self):
            self.move_ignores()

        def move_ignores(self):
            for file in self.ignores:
                fpath = Path(file["path"])
                fpath.rename(file["path"].replace("waiting", "rejected"))

        @staticmethod
        def move_file(file, to_path: str):
            fpath, dpath = Path(file["path"]), Path(to_path)
            filepath = dpath.joinpath(fpath.name)
            if all([fpath.is_file(), dpath.is_dir(), not filepath.is_file()]):
                print(f"moving file {str(fpath)} to {str(filepath)}")
                fpath.rename(str(filepath))

        def update_container(self, folder):
            cont = Videos(folder)
            if cont.info.ready_to_push:
                print(f"updating container {cont.name}")
                st = CLI.input(
                    f"cd {self.containers_path} && bash push {cont.name}", getout=True
                )
                if any([
                    st[1] != "Your branch is up to date with 'origin/main'.",
                    st[-1] != "Everything up-to-date"
                ]):
                    print("\n".join(CLI.input(f"cd {cont.path} && git push", getout=True)))
                else:
                    print("Everything up-to-date")

        def dispatch_files(self):
            for folder in Videos.folders:
                if self.files:
                    cont = Videos(folder)
                    free_space = 1.05e3 - cont.info.total_size
                    if free_space > 0.0 and cont.info.ready_to_push:
                        for file in self.files.copy():
                            size = file["size"]
                            if free_space - size > 0.0:
                                free_space -= size
                                timeout(
                                    lambda: self.move_file(
                                        file, cont.path.joinpath("videos")
                                    ), 1
                                )
                                self.files.remove(file)
                            else:
                                break
            Videos.update_all()
            for fn in Videos.folders:
                self.update_container(fn)
    return Waiting()


def get_rejected_handler():
    class Rejected:
        path = Path.home().joinpath("Videos/handler/rejected")
        files = filter_by_size(path, lambda x: x > 95.0)
        ignores = filter_by_size(path, lambda x: x < 95.0)

        def __init__(self):
            self.move_ignores()

        def move_ignores(self):
            for file in self.ignores:
                fpath = Path(file["path"])
                to_path = file["path"].replace("rejected", "waiting")
                if not Path(to_path).is_file():
                    fpath.rename(to_path)
    return Rejected()

