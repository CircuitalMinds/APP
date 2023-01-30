# -*- coding: utf-8 -*-
from werkzeug.exceptions import HTTPException
from libs import root_path
from libs.utils import getjson
from flask import Flask, json
from flask_cors import CORS
from views.main import main
from views.dispatcher import dispatcher
from views.container import container


def getenv(name):
    return getjson(root_path.joinpath(f"config/environ/{name}.json"))


def getresponse(info, **params):
    response = info.get_response()
    response.data = json.dumps(
        params if params else {
            i: getattr(info, i, None)
            for i in ("code", "name", "description")
        }
    )
    response.content_type = "application/json"
    return response


def create_app(name):
    env = getenv("application")
    app = Flask(
        import_name=f"app-{name}",
        static_folder=env["static_folder"],
        template_folder=env["template_folder"]
    )
    app.config.update(env["config"], server=env["server"])
    CORS(app)
    return app


app_server = create_app("server")


@app_server.errorhandler(HTTPException)
def handle_exception(error):
    return getresponse(error)


app_server.register_blueprint(main)
app_server.register_blueprint(container)

app_dispatcher = create_app("dispatcher")
app_dispatcher.register_blueprint(dispatcher)
