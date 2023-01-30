from werkzeug.serving import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from libs import hostname
from build import app_server, app_dispatcher
conf = app_server.config["server"]


class Main:
    host = hostname
    port, settings = conf["port"], conf["settings"]
    url = f"http://{host}:{port}"

    @classmethod
    def run(cls):
        application = DispatcherMiddleware(
            app_server, {"/dispatcher": app_dispatcher}
        )
        run_simple(
            cls.host, cls.port, application, **cls.settings
        )


if __name__ == "__main__":
    Main.run()
