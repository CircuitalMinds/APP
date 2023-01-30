from pathlib import Path
from libs.utils import opencsv, save_json
path = Path(__file__).parent


def get_playlist_data():
    data = []
    datafile = opencsv(path.joinpath("playlist.csv"))
    for i in datafile:
        if len(i["Playlist Id"]) == 11:
            data.append(i["Playlist Id"])
    save_json(path.joinpath("playlist.json"), data)
    return data


def get_library_data():
    data = []
    datafile = opencsv(path.joinpath("library.csv"))
    for v in datafile:
        x = {
            "url": v["Song URL"].replace("https://music", "https://www"),
            "title": v["Song Title"],
            "album": v["Album Title"],
            "artist": v["Artist Names"]
        }
        x["id"] = x.get("url").split("/watch?v=")[-1][:11]
        data.append(x)
    save_json(path.joinpath("library.json"), data)
    return data


def get_metadata_files():
    return [
        {"id": i.name.split(".json")[0][-11:], "file": i}
        for i in path.joinpath("metadata").iterdir()
    ]


def get_download_files():
    return [
        {"id": i.name.split(".mp4")[0][-11:], "file": i}
        for i in path.joinpath("downloads").iterdir()
        if i.name.endswith(".mp4")
    ]
