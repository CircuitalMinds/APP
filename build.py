from flask import Flask
from flask_cors import CORS
from werkzeug.serving import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from conf import Cfg


def create_app(name="app", env="development"):
    cfg = Cfg(env)
    app = Flask(name, **cfg.get("folders"))
    app.env = cfg.get("env")
    app.config.update(
        cfg.get("config"),
        **dict(server=cfg.get("server"))
    )
    CORS(app)
    return app


class Server:
    host: str
    port: int
    opts: dict

    def __init__(self, app):
        self.app = app
        for k, v in self.app.config["server"].items():
            setattr(self, k, v)

    def run(self):
        run_simple(
            self.host,
            self.port,
            DispatcherMiddleware(self.app),
            **self.opts
        )
