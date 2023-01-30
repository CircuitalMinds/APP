from flask import Blueprint, jsonify, abort, redirect, url_for
from libs.utils import getjson, save_json, CLI
from libs import root_path, Path
from .builtins.writer import write_files
container = Blueprint("container", __name__)
datafile = root_path.joinpath("config/environ/config.json")
route_names = ("videos", "pictures")


class Videos:
    path = Path(getjson(datafile)["local-container"]["videos"])
    ids = list(i.name for i in path.joinpath("containers").iterdir() if i.is_dir())

    def __init__(self, cont_id):
        self.id = cont_id
        self.url_root = f"https://github.com/circuitalmynds/music_{cont_id}/blob/main/videos"
        self.folder = self.path.joinpath(f"containers/{cont_id}")
        self.content = []
        self.totalsize = 0.0
        self.available_space = True
        self.data = {}

    def getdata(self):
        return

    @staticmethod
    def waiting_files(maxsize=None):
        folder = Videos.path.joinpath("handler")
        files = folder.joinpath("waiting").iterdir()
        data = []
        for file in files:
            filename = file.name
            size = file.stat().st_size * 1.0e-6
            allowed_size = size < (maxsize if maxsize else (size + 1))
            if filename.endswith(".mp4") and allowed_size:
                data.append(dict(
                    name=filename,
                    id=filename.split(".mp4")[0][-11:],
                    size=size,
                    path=str(file)
                ))
            else:
                file.rename(str(
                    folder.joinpath(f"rejected/{filename}")
                ))
        return data

    @staticmethod
    def available_folders():
        return sorted(
            i for i in Videos.ids
            if getjson(Videos.path.joinpath(
                f"containers/{i}/info.json"
            ))["available_space"]
        )

    @staticmethod
    def data_ids():
        path = Videos.path.joinpath("containers")
        ids = []
        folders = Videos.ids
        for fi in folders:
            folder = path.joinpath(fi, "videos")
            for vi in [i for i in folder.iterdir() if i.name != ".nothing"]:
                filename = vi.name
                if filename.endswith(".mp4"):
                    file_id = filename.split(".mp4")[0][-11:]
                    if file_id not in ids:
                        ids.append(file_id)
                    else:
                        vi.rename(Videos.path.joinpath("handler/repeated", filename))
        return ids

    def update_folder(self):
        write_files(self.folder, f"music_{self.id}")
        CLI.input(" && ".join([
                f"cd {str(self.folder)}", "python3 -m main set allow-push true"
            ]))
        CLI.input(" && ".join([
                f"cd {str(self.folder)}", "python3 -m main push"
            ]))

    @staticmethod
    def update_folders():

        def push(folder_path):
            CLI.input(" && ".join([
                f"cd {str(folder_path)}", "python3 -m main set allow-push true"
            ]))
            CLI.input(" && ".join([
                f"cd {str(folder_path)}", "python3 -m main push"
            ]))
        for i in Videos.ids:
            folder = Videos.path.joinpath(f"containers/{i}")
            write_files(folder, f"music_{i}")
            Videos(i)
            push(folder)


class Pictures:
    path = Path(getjson(datafile)["local-container"]["pictures"])
    ids = list(i.name for i in path.joinpath("containers").iterdir() if i.is_dir())

    @staticmethod
    def update_folders():
        def push(folder_path):
            print(" && ".join([
                f"cd {str(folder_path)}", "python3 -m main set allow-push true"
            ]))
            print(" && ".join([
                f"cd {str(folder_path)}", "python3 -m main push"
            ]))
        for i in Pictures.ids:
            cont = Pictures.path.joinpath(f"containers/{i}")
            write_files(cont, f"pictures_{i}")
            push(cont)


'''
    class WaitingFiles:
            path = Path.home().joinpath("Videos/handler/waiting")
            containers_path = Path.home().joinpath("Videos/containers")
            files = [i for i in filter_by_size(path, lambda x: x < 95.0) if i["name"].endswith(".mp4")]
            ignores = filter_by_size(path, lambda x: x > 95.0)

            def __init__(self):
                self.move_ignores()

            def move_ignores(self):
                for file in self.ignores:
                    fpath = Path(file["path"])
                    fpath.rename(file["path"].replace("waiting", "rejected"))

            @staticmethod
            def move_file(file, to_path: str):
                fpath, dpath = Path(file["path"]), Path(to_path)
                filepath = dpath.joinpath(fpath.name)
                if all([fpath.is_file(), dpath.is_dir(), not filepath.is_file()]):
                    print(f"moving file {str(fpath)} to {str(filepath)}")
                    fpath.rename(str(filepath))

            def update_container(self, folder):
                cont = Videos(folder)
                if cont.info.ready_to_push:
                    print(f"updating container {cont.name}")
                    st = CLI.input(
                        f"cd {self.containers_path} && bash push {cont.name}", getout=True
                    )
                    if any([
                        st[1] != "Your branch is up to date with 'origin/main'.",
                        st[-1] != "Everything up-to-date"
                    ]):
                        print("\n".join(CLI.input(f"cd {cont.path} && git push", getout=True)))
                    else:
                        print("Everything up-to-date")

            def dispatch_files(self):
                for folder in Videos.folders:
                    if self.files:
                        cont = Videos(folder)
                        free_space = 1.05e3 - cont.info.total_size
                        if free_space > 0.0 and cont.info.ready_to_push:
                            for file in self.files.copy():
                                size = file["size"]
                                if free_space - size > 0.0:
                                    free_space -= size
                                    timeout(
                                        lambda: self.move_file(
                                            file, cont.path.joinpath("videos")
                                        ), 1
                                    )
                                    self.files.remove(file)
                                else:
                                    break
                Videos.update_all()
                for fn in Videos.folders:
                    self.update_container(fn)

    class RejectedFiles:
            path = Path.home().joinpath("Videos/handler/rejected")
            files = filter_by_size(path, lambda x: x > 95.0)
            ignores = filter_by_size(path, lambda x: x < 95.0)

            def __init__(self):
                self.move_ignores()

            def move_ignores(self):
                for file in self.ignores:
                    fpath = Path(file["path"])
                    to_path = file["path"].replace("rejected", "waiting")
                    if not Path(to_path).is_file():
                        fpath.rename(to_path)
'''


@container.route("/container/")
@container.route("/container/<name>/")
def container_root(name=None):
    if name in route_names:
        return redirect(url_for(f"{name}_view"))
    else:
        abort(404)


@container.route("/container/videos/")
@container.route("/container/videos/<cont_id>/")
def videos_view(cont_id=None):
    if cont_id in Videos.ids:
        return jsonify(Videos(cont_id).data)
    else:
        return jsonify(ids=Videos.ids)


@container.route("/container/pictures/")
@container.route("/container/pictures/<cont_id>/")
def pictures_view(cont_id=None):
    data = getjson(datafile)
    path = Path(data["local-container"]["pictures"])
    folders = [i.name for i in path.joinpath("containers").iterdir() if i.is_dir()]
    if cont_id in folders:
        return jsonify(getjson(path.joinpath(f"containers/{cont_id}/info.json")))
    else:
        return jsonify(ids=folders)


