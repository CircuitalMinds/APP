from flask import Blueprint, abort, jsonify
yt = Blueprint("yt", "yt_view")


@yt.route("/youtube/")
@yt.route("/youtube/<opt>/")
def youtube(opt=None):
    return jsonify(opt=opt) if opt else abort(404)
