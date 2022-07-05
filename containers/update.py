from .build import Videos
from libs.finder import YouTube
from . import main_path, folder_pictures, folder_videos
from .utils import str_decode
from libs.file import Json
from json import dumps


class Update:

    @staticmethod
    def videos():
        alldata = []
        files, metadata = Videos.update_all(), YouTube().dataset

        def scheme(filename):
            dataset = Json(f"{folder_videos}/metadata/{filename}")
            dataset.update(dict(
                title="",
                description="",
                duration="",
                image="",
                keywords=""
            ))
            return dataset

        def content(y):
            return str_decode(y["content"])

        def getdata(xdata, ydata):
            for i in ydata["name"] if "name" in ydata else []:
                if i["name"] in ("title", "twitter:title") and not xdata["title"]:
                    xdata["title"] = content(i)
                if i["name"] in ("description", "twitter:description") and not xdata["description"]:
                    xdata["description"] = content(i)
                if i["name"] == "twitter:image":
                    xdata["image"] = content(i)
                if i["name"] == "keywords":
                    xdata["keywords"] = content(i)
            for i in ydata["property"] if "property" in ydata else []:
                if i["property"] == "og:title" and not xdata["title"]:
                    xdata["title"] = content(i)
                if i["property"] == "og:description" and not xdata["description"]:
                    xdata["description"] = content(i)
                if i["property"] == "og:image" and not xdata["image"]:
                    xdata["image"] = content(i)
            for i in ydata["itemprop"] if "itemprop" in ydata else []:
                if i["itemprop"] == "name" and not xdata["title"]:
                    xdata["title"] = content(i)
                if i["itemprop"] == "description" and not xdata["description"]:
                    xdata["description"] = content(i)
                if i["itemprop"] == "duration":
                    t = i["content"].split("PT")[-1].replace("M", ":").replace("S", "")
                    if len(t.split(":")[-1]) == 1:
                        t = t.replace(":", ":0")
                    xdata["duration"] = t
            alldata.append(xdata)
            return xdata

        for file in files:
            name = file["name"].split(".mp4")[0][-11:]
            meta = metadata[name]
            video_data = scheme(meta.path.name)
            video_data["url"] = file["url"]
            getdata(video_data, meta).write()
        folder_videos.joinpath("dataset.json").open("w").write(
            dumps(alldata, **dict(indent=4, sort_keys=True, ensure_ascii=False))
        )
