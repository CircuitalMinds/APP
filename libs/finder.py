from os import system
import wikipedia
from .request import Http
from .file import Json
from . import app_home


class YouTube:
    url = "https://www.youtube.com"
    folder = app_home.joinpath("libs/youtube")

    def __init__(self):
        self.dataset = dict()
        self.get_info()

    def get_info(self):
        self.update_info()
        folder = self.folder.joinpath("metadata")
        for f in folder.iterdir():
            self.dataset[f.name.split(".json")[0]] = Json(str(f))

    def register_id(self, *v_ids):
        file = self.folder.joinpath("downloads/ids.txt")
        ids = [x.split()[-1] for x in file.open().readlines()]
        size = len(ids)
        for v_id in v_ids:
            if v_id not in ids:
                ids.append(v_id)
        if size != len(ids):
            file.open("w").write("\n".join([
                f"youtube {x}" for x in ids]
            ))
        self.get_info()

    def update_info(self):
        for x in self.folder.joinpath("downloads/ids.txt").open().readlines():
            v_id = x.split()[-1]
            file = self.folder.joinpath(f"metadata/{v_id}.json")
            if not file.is_file():
                jsonfile = Json(str(file))
                jsonfile.update(**self.get_metadata(v_id))
                jsonfile.write()

    def search(self, v_title):
        return Http(self.url).html_parser("results", **dict(search_query=v_title))

    def watch(self, v_id):
        return Http(self.url).html_parser("watch", **dict(v=v_id))

    def get_ids(self, v_title):
        data = {v_title: []}
        try:
            for q in self.search(v_title).find('body').prettify().split('"videoId":"'):
                r = q.split('"')[0]
                if len(r) == 11 and r not in data[v_title]:
                    data[v_title].append(r)
            return data
        except UnicodeEncodeError:
            return data

    def get_metadata(self, v_id):
        metadata = {
            key: [] for key in ("name", "property", "itemprop")
        }
        data = self.watch(v_id).find('head').find_all('meta')
        for x in data:
            for y in metadata:
                if x.get(y):
                    metadata[y].append(x.attrs)
        return metadata

    @staticmethod
    def is_id(v_html):
        try:
            return '"status":"ERROR"' not in v_html.find("body").find("script").string
        except UnicodeEncodeError:
            return False

    def download(self, **data):
        for k, v in data.items():
            system(f"cd {self.folder} && bash ./download.sh {k} {v}")
        self.update_info()

    def run_tasks(self):
        file = self.folder.joinpath("tasks.json")
        tasks = Json(str(file))
        for i, v in enumerate(tasks["video"]):
            if v["status"] == "pending":
                self.download(**{"video_id": v["id"]})
                v["status"] = "done"
                tasks["video"][i] = v
        for i, p in enumerate(tasks["playlist"]):
            if p["status"] == "pending":
                self.download(**{"playlist_id": p["id"]})
                p["status"] = "done"
                tasks["playlist"][i] = p
        tasks.write()


class Wikipedia:

    def __init__(self, query):
        self.query = query
        relations = wikipedia.search(self.query)
        self.results = dict(
            relations=relations,
            summary=wikipedia.summary(relations[0]),
            page=wikipedia.page(relations[0])
        )


class Google:
    url = "https://www.google.com"

    def __init__(self, query):
        self.query = query
        self.source = Http(self.url).html_parser("search", q=query)
