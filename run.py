from os import system
from multiprocessing import Pool


def api():
    system("cd api && bash run")


def app():
    system("bash run")


def site():
    system("cd site && python3 -m run build")


def worker(*processes):

    def run(process):
        process.run()

    with Pool(len(processes)) as p:
        p.map(run, processes)


if __name__ == '__main__':
    from sys import argv
    opts = dict({i.__name__: i for i in [api, app, site]})
    if len(argv) > 1:
        if argv[1] in opts:
            opts[argv[1]]()
