from flask import render_template
from build import create_app, Server
from view import videos
app = create_app()
server = Server(app)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template(
        "index.html",
        site=app.config["site"]
    )


videos(app)
server.run()
