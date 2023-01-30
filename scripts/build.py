from flask import render_template
from flask_cors import CORS
from .tools import getmethods, getresponse, request_data, response_json
from libs.utils import base_path, get_host
from werkzeug.exceptions import HTTPException
from .logger import History
from . import config
mode = config.env
server = dict(
    development=dict(
        host=get_host(), port=8080, debug=True
    ),
    production=dict(
        host="circuitalminds.herokuapp.com", port=80, debug=False
    )
)[mode]


class Template:
    base = "index.html"
    data = dict(
        site=f"http://{get_host()}"
        if mode == "development" else
        "https://circuitalminds.github.io",
        view=None
    )

    def __init__(self, **data):
        self.data.update(data)

    def render(self):
        return render_template(self.base, **self.data)


class Route:
    mapping = dict(
        container=dict(
            pictures="/container/pictures/",
            videos="/container/videos/"
        ),
        drive=dict(
            storage=dict(
                documents="/drive/storage/documents/",
                pictures="/drive/storage/pictures/",
                videos="/drive/storage/videos/"
            ),
            trash="/drive/trash/"
        ),
        jupyter=dict(
            notebooks=dict(
                intro="/jupyter/notebooks/intro/",
                engineering="/jupyter/notebooks/engineering/",
                data_science="/jupyter/notebooks/data-science/"
            ),
            dataset="/jupyter/dataset/"
        ),
        user=dict(
            auth="/user/auth/",
            login="/user/login/",
            register="/user/register/"
        ),
        youtube=dict(
            search="/youtube/search/",
            watch="/youtube/watch/",
            download="/youtube/download/"
        )
    )

    @staticmethod
    def defaults(app):

        @app.route("/send-json/", **getmethods())
        def json_view():
            req = request_data()
            content_type = req["headers"].get("Content-Type")
            if content_type == "application/json":
                return req["json"]
            else:
                return "Content-Type not supported!"

        @app.errorhandler(HTTPException)
        def handle_exception(error):
            return getresponse(error)

        @app.route("/")
        def home():
            return response_json(response=200)


class App:
    name = "app"
    path = base_path
    env = mode
    template_folder = "./application/templates"
    static_folder = "./application/static"
    config = dict(
        secret_key="circuitalminds",
        session_type="filesystem"
    )

    @property
    def folders(self):
        return dict(
            template_folder=getattr(self, "template_folder"),
            static_folder=getattr(self, "static_folder")
        )

    @staticmethod
    def run(app):
        History()
        app.run(threaded=True, **server)

    def setconf(self, app):
        app.env = self.env
        app.config.update(self.config)
        CORS(app)
        app.Template = Template
        Route.defaults(app)
        app.init = lambda: self.run(app)
