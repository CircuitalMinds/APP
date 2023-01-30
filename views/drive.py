from flask import jsonify, redirect, url_for, send_file
from os import walk, remove
from os.path import join, isdir
from subprocess import getoutput
from zipfile import ZipFile
from werkzeug.utils import secure_filename


class Data:
    path = "data"
    datatypes = ["json", "yml", "txt"]
    files, dirs = [], []


class Documents:
    path = "documents"
    datatypes = ["html", "pdf", "md", "markdown", "ipynb"]
    files, dirs = [], []


class Pictures:
    path = "pictures"
    datatypes = ["jpg", "png", "svg", "gif", "jpeg"]
    files, dirs = [], []


class Videos:
    path = "videos"
    datatypes = ["mp4", "mp3", "wmv", "mkv"]
    files, dirs = [], []


class Scripts:
    path = "scripts"
    datatypes = ["py", "js", "css", "sqlite3", "sh"]
    files, dirs = [], []


class Drive:
    data = {}
    folders = {
        f.__name__.casefold(): f() for f in (Data, Documents, Pictures, Videos, Scripts)
    }

    def __init__(self, path, fdata, fjson):
        self.path = path
        self.fdata = fdata
        self.json_file = fjson(join(path, "directory.json"))
        self.update()

    def update(self):
        for name in self.folders:
            folder = self.folders[name]
            folder_data = self.fdata(join(self.path, folder.path))
            folder.files = folder_data["files"]
            folder.dirs = folder_data["dirs"]
            self.data[name] = folder_data
        self.json_file.data = self.data
        self.json_file.save()
        return

    def route(self, method, request_data):
        if method == "POST":
            files = request_data.files.getlist("files[]")
            for fi in files:
                self.upload(fi)
            return redirect(url_for("home"))
        else:
            file_data = self.get(request_data["filename"])
            if all([key in file_data for key in ("filename", "path")]):
                return send_file(file_data["path"], download_name=file_data["filename"])
            else:
                return jsonify(file_data)

    def get(self, filename):
        data = {}
        not_found = {"response": f"filename with name {filename} not found"}
        for i in self.folders:
            folder = self.__dict__[i]
            file_data = list(filter(lambda x: x["name"] == filename, folder.files))
            if file_data:
                data.update(file_data[0])
                return data
        return not_found

    def upload(self, file):
        name = file.__dict__["filename"]
        if name:
            filename = secure_filename(filename=name)
            datatype = filename.split('.')[-1]
            path = self.path
            for i in self.folders:
                folder = self.__dict__[i]
                if datatype in folder.datatypes:
                    path = folder.path
            file_path = join(path, filename)
            file.save(file_path)
            self.update()
            return {"response": f"{filename} uploaded to {file_path}"}
        else:
            return {"response": "No selected file"}


class Zip:

    @staticmethod
    def create(path):
        if isdir(path):
            zip_path = path + ".zip"
            with ZipFile(zip_path, 'w') as zipObj:
                for folderName, sub_folders, filenames in walk(path):
                    for filename in filenames:
                        filePath = join(folderName, filename)
                        zipObj.write(filePath)
            return {"filename": zip_path.split("/")[-1], "path": zip_path}
        else:
            return {"response": "folder not found"}

    @staticmethod
    def remove_zip(zip_path):
        remove(zip_path)
        return

    @staticmethod
    def get_info_zip(zip_path):
        name = zip_path.split('/')[-1]
        folder_path = zip_path.replace(f"/{name}", "")
        data = []
        str_data = getoutput(f"cd {folder_path} && python -m zipfile -l ./{name}").splitlines()[1:]
        for s in str_data:
            y = s.split()
            print(y)
            data.append({
                "filename": y[0],
                "date": " ".join([y[1].replace("-", "/"), y[2]]),
                "size": y[3]
            })
        print(data)
        return data
