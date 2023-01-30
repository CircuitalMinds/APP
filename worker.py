from libs.utils import getjson, save_json
from multiprocessing import Pool
from threading import Thread
import time
import threading
import socket


def get_update():
    filepath = env_path.joinpath("task.json")
    datafile = getjson(filepath)
    data["waiting"] = datafile["waiting"]
    data["assignments"] = datafile["assignments"]


def create_task(func, name):
    class Thd(Thread):
        def __init__(self):
            Thread.__init__(self)
            self.name = name
            self.func = func

        def run(self):
            print(f"\n{time.ctime(time.time())} - starting {self.name}\n")
            self.func()
            print(f"\n{time.ctime(time.time())} - exiting {self.name}\n")
    task = Thd()
    task.start()
    task.join()
    print(f"\n{time.ctime(time.time())} - task {name}-thread terminated\n")


def run_task(i):
    create_task(data["assignments"][i], i)


def main(*procs):
    data["assignments"].extend(list(procs))
    n = len(data["assignments"])
    pn = range(n)
    with Pool(n) as p:
        p.map(run_task, pn)


def init():
    get_update()
    data["waiting"] = True
    save_json(env_path.joinpath("task.json"), data)
    while data["waiting"]:
        try:
            print(data)
            time.sleep(3)
            get_update()
        except KeyboardInterrupt:
            data["waiting"] = False
            save_json(env_path.joinpath("task.json"), data)
            print(data)



if __name__ == "__main__":
    threads = [threading.Thread(target=scanport, kwargs=dict(port=i)) for i in ports]
    #threads[0].start()
    #threads[0].join()
    for t in threads:
        t.start()
    [t.join() for t in threads]
    print(ports)
