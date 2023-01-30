from flask import Blueprint, jsonify
dispatcher = Blueprint("dispatcher", __name__)


@dispatcher.route("/")
def get_worker():
    return jsonify(response="dispatcher-route")
