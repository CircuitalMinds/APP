from os.path import join
from requests import get, post
from bs4 import BeautifulSoup


class Http:
    data = dict()

    def __init__(self, url):
        self.url = url

    @staticmethod
    def url_parse(url, path, **data):
        q = join(url, path[1:] if path.startswith("/") else path)
        if data:
            return q + "?" + "&".join([
                f"{k}={v}" for k, v in data.items()
            ])
        else:
            return q

    def html_parser(self, path="/", **data):
        return BeautifulSoup(
            self.get(path, datatype="text", **data), "html.parser"
        )

    def get(self, path="/", datatype="", **data):
        r = get(self.url_parse(self.url, path, **data))
        if datatype == "json":
            return r.json()
        elif datatype == "text":
            return r.text
        else:
            return r

    def post(self, path="/", datatype="", **data):
        r = post(self.url_parse(self.url, path), data)
        if datatype == "json":
            return r.json()
        elif datatype == "text":
            return r.text
        else:
            return r
