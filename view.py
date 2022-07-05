from pathlib import Path
from libs.file import Json
from flask import jsonify


def videos(app):
    videos_folder = Path.cwd().joinpath("containers/videos")
    files = videos_folder.joinpath("files.json")
    metadata = videos_folder.joinpath("dataset.json")

    @app.route("/videos/files/")
    def getfiles():
        return jsonify(Json(files))

    @app.route("/videos/metadata/")
    def getmeta():
        return jsonify(Json(metadata))
