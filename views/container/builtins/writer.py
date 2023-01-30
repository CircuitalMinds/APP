from pathlib import Path
from .main import getdate
from libs.utils import save_json
cpath = Path(__file__).parent


def envfile(path):
    path = Path(str(path))
    file = path.joinpath(".env")
    if path.exists() and not file.is_file():
        data = "\n".join([
            f"last-update={getdate()}",
            "allow-push=false"
        ])
        file.open("w").write(data)


def get_videos_script(path, repo_name):
    path = Path(path)
    file = path.joinpath("getdata.py")
    if path.exists():
        file.open("w").write("""from pathlib import Path
from json import load, dumps
jsonconfig = dict(
    indent=4,
    sort_keys=True,
    ensure_ascii=False
)
path = Path(__file__).parent
giturl = "https://github.com/circuitalmynds/<REPO-NAME>"
folder_content = path.joinpath("videos")
info = path.joinpath("info.json")


def getinfo():
    return load(info.open())


def save_info(data):
    info.open("w").write(dumps(
        data, **jsonconfig
    ))


def getfiles():
    urlfile, totalsize, content = f"{giturl}/blob/main/videos", 0.0, []
    files = list(
        fi for fi in folder_content.iterdir()
        if fi.name != ".nothing" and fi.name.endswith(".mp4")
    )
    for file in files:
        filename = file.name
        size, file_id = file.stat().st_size * 1.0e-6, filename.split(".mp4")[0][-11:]
        content.append(dict(
            name=filename,
            id=file_id,
            size=size,
            path=str(file),
            url=f"{urlfile}/{filename}?raw=true"
        ))
        totalsize += size
    return dict(
        content=content,
        total_size=totalsize,
        available_space=totalsize < 9.5e2
    )


if __name__ == "__main__":
    save_info(getfiles())
    print(getinfo())

""".replace("<REPO-NAME>", repo_name))


def main_script(path):
    path = Path(str(path))
    file = path.joinpath("main.py")
    if path.exists():
        data = cpath.joinpath("main.py").open().read()
        file.open("w").write(data)


def push_script(path, content_folder, username, repo_name):
    path = Path(str(path))
    if path.exists():
        path.joinpath("push").open("w").write('\n'.join([
            '#!/bin/bash\n\n',
            'allow_push=$( python3 -m main get allow-push )',
            'git_user=alanmatzumiya',
            f'username={username}',
            f'repo={repo_name}\n\n',
            'echo *__pycache__ > .gitignore',
            f'find ./{content_folder}* -size +95M | cat >> .gitignore',
            'if $allow_push; then\n',
            '\tpython3 -m getdata',
            '\tpython3 -m main set allow-push false\n',
            '\tgit add .',
            '\tgit commit -m "autocommit"',
            '\tgit push https://$git_user:"$( head "$HOME"/secret )"@github.com/$username/$repo.git\n',
            'fi'
        ]))
    else:
        print(f"{str(path)} not exists")


def write_files(path, repo_name):
    path = Path(str(path))
    if path.exists():
        username, folder = None, None
        if "Videos/containers" in str(path):
            username = "circuitalmynds"
            folder = path.joinpath("videos")
            get_videos_script(path, repo_name)
        elif "Pictures/containers" in str(path):
            username = "alanmatzumiya"
            folder = path.joinpath("photos")
        if not folder.exists():
            folder.mkdir()
            folder.joinpath(".nothing").open("w").write("")
            save_json(
                path.joinpath("info.json"),
                dict(
                    available_space=True,
                    content=[],
                    total_size=0.0
                )
            )
        for func in (envfile, main_script):
            func(path)
        push_script(path, folder.name, username, repo_name)
