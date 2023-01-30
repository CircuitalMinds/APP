from pathlib import Path
from libs.request import Http
from libs.shell import CLI
yt_path = Path(__file__).parent


class YouTube:
    url = "https://www.youtube.com"
    downloads, metadata = (
        yt_path.joinpath(i)
        for i in ("downloads", "metadata")
    )
    dataset = dict()

    @staticmethod
    def download_video(**data):
        key, value = None, None
        for i in ("video_title", "video_id", "playlist_id"):
            if i in data:
                key, value = i, data.get(i)
                break
        CLI.input(
            f"cd {yt_path} && bash download '{key}' '{value}'"
        )

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
        keys = ("name", "property", "itemprop")
        metadata = {key: [] for key in keys}
        data = self.watch(v_id).find('head').find_all('meta')
        for x in data:
            for y in metadata:
                if x.get(y):
                    metadata[y].append(x.attrs)
        return metadata

    @staticmethod
    def is_id(v_html):
        if Http.is_html(v_html):
            try:
                return '"status":"ERROR"' not in v_html.find("body").find("script").string
            except UnicodeEncodeError:
                return False
        else:
            return False

