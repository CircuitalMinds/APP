from flask import Blueprint, render_template, request, jsonify, redirect
from os import kill, getpid
from signal import SIGINT
main = Blueprint("main",  __name__)


@main.route("/")
def home():
    return jsonify(path="/", pathname="home")


@main.route("/login/", methods=["POST"])
def login():
    userdata = request.form.to_dict()
    email = userdata.get("email")
    password = userdata.get("password")
    if email == "admin" and password == "admin":
        return jsonify(authorized=True)
    else:
        return jsonify(authorized=False)


@main.route("/send-json/", methods=["GET", "POST"],)
def json_view():
    headers = request.headers
    if headers.get("Content-Type") == "application/json":
        return request.json
    else:
        datajson = dict()
        for q in request.query_string.decode("utf-8").split("&"):
            t = q.split("=")
            if len(t) == 2:
                datajson[t[0]] = t[-1]
        return jsonify(datajson)


@main.route("/admin/")
@main.route("/admin/<tool>/")
def admin(tool=None):
    opts = ["shutdown"]
    if tool:
        if tool in opts:
            return redirect(f"/admin/{tool}/")
        else:
            return jsonify(dict(response=f"admin tool with name {tool} not found"))
    else:
        return jsonify(response="admin tools")


@main.route("/admin/shutdown/")
def shutdown():
    kill(getpid(), SIGINT)
    resp = dict(response="server was disconnected successfully")
    return jsonify(resp)
