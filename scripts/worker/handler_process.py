from multiprocessing import Pool
from subprocess import getoutput as output


def do_processes(ID):
    print(f"{ID} starting")
    return output(f"python -c 'print({ID if ID else 'int(input())'} ** 2)'")


if __name__ == '__main__':
    n = 3
    with Pool(n) as p:
        data = p.map(do_processes, (1, None, 5))
    print(data)

r'''


def repo_data(name):
    ignores = from_root("dataset", "gitignore.txt")
    reqs = from_root("dataset", "reqs.txt")


class Repo:

    def __init__(self, name):



    def write_reqs(self, repo):
        repo_path = from_root(repo)
        File(self.reqs).copy(repo_path, "requirements.txt")    

    def get_branch(self, repo):
        return run_prompt(
            f'cd {from_root(repo)}', "git branch"
        ).split()[-1]


    def is_updated(self, repo):
        return run_prompt(
                f'cd {from_root(repo)}', "git status"
        ).splitlines()[-1] == "nothing to commit, working tree clean"    


    def push(repo):
        run_script("git", "push", from_root(repo))


    def clone(repo, branch="main"):
        git_url = f"https://github.com/CircuitalMinds/{repo}.git"
        run_script("git", "clone", from_root(repo), branch, git_url)

from modules import Dir, Console, Obj
from modules.dirs import save_file
from modules.console import Bash, get_args
from time import sleep
cmd = Bash()


class GitHub:
    url = "https://github.com/CircuitalMinds"
    repos = [
        "circuitalminds.github.io", "API", "APP", "static",
        "templates", "jupyter", "notebooks", "saponis"
    ]
    containers = dict()
    containers["videos"] = {
        "path": Dir.path.join(Dir.home, "Videos", "containers"),
        "url": "https://github.com/circuitalmynds"
    }
    containers["videos"]["folders"] = Dir.ls("Videos/containers")
    containers["videos"]["condition"] = lambda size: size < 1.05e3
    containers["videos"]["info"] = lambda x: Obj(Dir.path.join(
        Dir.home, "Videos", "containers", x, "info.json"
    )).data
    containers["pictures"] = {"path": Dir.path.join(Dir.home, "Pictures", "containers")}
    containers["pictures"]["folders"] = Dir.ls("Pictures/containers")
    gitignore = {
        "filename": ".gitignore",
        "text": "\n".join([
            ".env", "*environment", "*__pycache__", "*sass-cache"
        ])
    }

    def push_container(self, name, folder):
        container = self.containers.get(name)
        if not container:
            return
        if folder not in container["folders"]:
            return
        info = container["info"](folder)
        if container["condition"](info["total_size"]):
            cmd.git(
                "push", container["path"], folder,
                "main", Dir.path.join(container["url"], folder + ".git")
            )
        return

    def push(self, repo):
        if repo in self.repos:
            if not self.is_updated(repo):
                cmd.git(
                    "push", Dir.path.join(Dir.home, "GitHub"), repo,
                    "main", Dir.path.join(self.url, repo + ".git")
                )
        return

    def clone(self, repo):
        if repo in self.repos:
            cmd.git(
                "clone", Dir.path.join(Dir.home, "GitHub"), repo,
                "main", Dir.path.join(self.url, repo + ".git")
            )
        return

    def get_branch(self, repo):
        if repo in self.repos:
            return Console.run(
                f'cd {Dir.path.join(Dir.home, "GitHub", repo)}',
                "git branch"
            ).split()[-1]
        else:
            return ""

    def is_updated(self, repo):
        if repo in self.repos:
            return Console.run(
                f'cd {Dir.path.join(Dir.home, "GitHub", repo)}',
                "git status"
            ).splitlines()[-1] == "nothing to commit, working tree clean"
        else:
            return False

    def write_ignores(self, repo):
        if repo in self.repos:
            save_file(
                Dir.path.join(
                    Dir.home, "GitHub", repo, self.gitignore["filename"]
                ),
                self.gitignore["text"]
            )
        return


class Update:
    def __init__(self):
        self.git = GitHub()
        args = get_args()
        if len(args) >= 2:
            if args[0] == "repos":
                if args[0] == "repos":
                    self.push_repos(
                        ("static", "templates", "api", "site") if "*" == args[1] else args[1:]
                    )
            elif args[0] == "containers":
                container = self.git.containers.get(args[1])
                if container:
                    self.push_containers(args[1], container["folders"])

    def push_repos(self, repos):
        for name in repos:
            try:
                print(f"{name}: pushing")
                self.__getattribute__(name)()
                print(f"{name}: updated")
                sleep(2)
            except AttributeError:
                pass
        return

    def push_containers(self, name, repos):
        for i in repos:
            print(f"{i}: pushing")
            self.git.push_container(name, i)
            print(f"{i}: updated")
            sleep(2)
        return

    def api(self):
        self.git.write_ignores("API")
        save_file(
            Dir.path.join(Dir.home, "GitHub", "API", "requirements.txt"),            
            "\n".join("""
                flask
                flask-cors
                flask_sqlalchemy
                gunicorn
                requests
                Werkzeug
                PyYAML
                numba
                mpmath
                imageio
                imageio-ffmpeg
                matplotlib
                bs4
                numpy
                scipy
                wikipedia""")
        )
        Dir.copy_folders(
            Dir.path.join("App", "api"),
            Dir.path.join("GitHub", "API")
        )
        Dir.copy_files(
            Dir.path.join("App", "api"),
            Dir.path.join("GitHub", "API")
        )
        obj = Obj(Dir.path.join(Dir.home, "GitHub", "API", "settings.json"))
        obj.data.update({"server": {
            "debug": False,
            "host": "https://circuitalminds.heroku.com",
            "port": 80
        }})
        obj.save()
        self.git.push("API")
        return

    def site(self):
        self.git.write_ignores("circuitalminds.github.io")
        Dir.copy_folders(
            Dir.path.join("App", "site"),
            Dir.path.join("GitHub", "circuitalminds.github.io"),
            *[".sass-cache", "_site"]
        )
        Dir.copy_files(
            Dir.path.join("App", "site"),
            Dir.path.join("GitHub", "circuitalminds.github.io"),
            *["_config.yml"]
        )
        Console.run(
            "cp " + Dir.path.join(
                Dir.root, "_config.yml"
            ) + " " + Dir.path.join(
                Dir.home, "GitHub", "circuitalminds.github.io", "_config.yml"
            )
        )
        self.git.push("circuitalminds.github.io")
        return

    def static(self):
        self.git.write_ignores("static")
        Dir.copy_folders(
            Dir.path.join("App", "static"),
            Dir.path.join("GitHub", "static")
        )
        self.git.push("static")
        return

    def templates(self):
        self.git.write_ignores("templates")
        Dir.copy_folders(
            Dir.path.join("App", "templates"),
            Dir.path.join("GitHub", "templates")
        )
        Dir.copy_files(
            Dir.path.join("App", "templates"),
            Dir.path.join("GitHub", "templates")
        )
        self.git.push("templates")
        return


if __name__ == '__main__':
    Update()
'''