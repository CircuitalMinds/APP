from pathlib import Path
from random import sample
from time import sleep
from . import Videos


def upload_files():
    files = Videos.waiting_files(maxsize=95.0)
    files[:] = sample(files, len(files) - 1)
    folders = Videos.available_folders()
    x, y = 0.0, 0.0
    for i in folders:
        vi = Videos(i)
        datasize = 9.5e2 - vi.totalsize
        x += datasize
        while datasize > 0.0 and files:
            sample_size = 0.0
            sample_data = []
            for file in files:
                if sample_size < 100.0 and datasize > 0.0:
                    sample_size += file["size"]
                    sample_data.append(file)
                    datasize -= file["size"]
                else:
                    break
            y += sample_size
            for fi in sample_data:
                files.remove(fi)
                fpath = Path(fi["path"])
                xpath = vi.folder.joinpath(f"videos/{fpath.name}")
                if fpath.exists() and not xpath.exists():
                    fpath.rename(str(xpath))
            sleep(5)
            vi.update_folder()
            sleep(5)