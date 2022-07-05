from console import Shell
Host = Shell.run("hostname", "-I")
defaults = dict(
    env="development",
    folders=dict(
        template_folder="./templates",
        static_folder="./static"
    ),
    server=dict(
        host=Host,
        port=8000,
        debug=True
    ),
    config=dict(
        SQLALCHEMY_BINDS=dict(),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        secret_key="circuitalminds",
        session_type="filesystem",
        site=f"http://{Host}"
    )
)
production = dict(
    server=dict(
        host="circuitalminds.herokuapp.com",
        port=80,
        debug=False
    ),
    site="https://circuitalminds.github.io"
)


class Cfg:

    def __init__(self, env):
        self.appdata, self.server = dict(), dict()
        if env in ("development", "production"):
            self.appdata["env"] = env
        else:
            self.appdata["env"] = "development"
        for i in ("folders", "server", "config"):
            self.appdata[i] = defaults[i]
        self.appdata["server"]["opts"] = dict({
            i: env == "development" for i in (
                "use_reloader",
                "use_debugger",
                "use_evalex"
            )
        })

    def get(self, key):
        return self.appdata.get(key)
