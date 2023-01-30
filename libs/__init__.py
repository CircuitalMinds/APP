from libs.utils import get_host
from pathlib import Path
root_path = Path(__file__).parent.parent
home_path = Path.home()
hostname = get_host()


def notes():
    textfile = home_path.joinpath("Desktop/notes.txt")
    if textfile.is_file():
        print(textfile.open().read())
