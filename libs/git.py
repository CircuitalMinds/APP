from os.path import join
from .utils import CLI, Path
import webbrowser
root_path = Path(__file__).parent.parent


class GitHub:
    url = "https://www.github.com"
    url_content = "https://raw.githubusercontent.com"
    repos = []

    def __init__(self, **data):
        if type(data.get("repos")) == list:
            self.repos = data["repos"]

    def search(self, **kwargs):
        q, user, name = [], kwargs.get("user"), kwargs.get("name")
        if user and name:
            for repo in self.repos:
                if (repo["user"].lower(), repo["name"]) == (user, name):
                    q.append(repo)
        if user and not name:
            for repo in self.repos:
                if repo["user"].lower() == user:
                    q.append(repo)
        if not user and name:
            for repo in self.repos:
                if repo["name"] == name:
                    q.append(repo)
        return q

    def download(self, repo):
        data = self.search(name=repo)
        if data:
            repo = data[0]
            webbrowser.open(join(
                self.url, repo["user"], repo["name"], "archive/refs/heads/main.zip"
            ))
        else:
            print(f"repository with name {repo} not found")

    def clone(self, repo):
        data = self.search(name=repo)
        if data:
            repo = data[0]
            path = root_path.joinpath(repo["folder"])
            CLI.runscript("git", "clone", str(path.parent), repo["user"], repo["name"], path.name)
        else:
            print(f"repository with name {repo} not found")

    def check(self, repo):
        data = self.search(name=repo)
        if data:
            repo = data[0]
            CLI.runscript("git", "check", str(root_path.joinpath(repo["folder"])))
        else:
            print(f"repository with name {repo} not found")

    def push(self, repo):
        data = self.search(name=repo)
        if data:
            repo = data[0]
            CLI.runscript("git", "push", str(root_path.joinpath(repo["folder"])), repo["user"], repo["name"])
        else:
            print(f"repository with name {repo} not found")
