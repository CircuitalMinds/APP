import socket
from threading import Thread
from inspect import signature
from libs.shell import CLI
import asyncio
from multiprocessing import Pool


def is_port_available(number):
    target = "192.168.50.100"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = s.connect_ex((target, number)) != 0
    s.close()
    return result


def assign_thread(func, name):
    class Thd(Thread):
        result = None

        def __init__(self):
            Thread.__init__(self)
            self.name = name
            self.func = func

        def call(self):
            pass

        def run(self):
            self.result = self.func()
    thd = Thd()

    def call():
        thd.start()
        thd.join()
        return thd.result
    thd.call = call
    return thd


class Task:
    processes = dict()
    data_required = ("name", "function", "args")

    def __init__(self, *procs):
        for i, p in enumerate(procs):
            self.processes[i] = dict()
            for key in self.data_required:
                self.processes[i][key] = p[key]

    def start(self):
        for p in self.processes.values():
            p["data"] = self.preprocess(p["function"], p["args"], getout=True)()

    @staticmethod
    def preprocess(func, *args, getout=False):
        def call():
            out = func(*args)
            if getout:
                return out
        return call


task = Task({"name": "test", "function": lambda a: a + 5, "args": 8})

task.start()

'''

with Pool(self.count) as proc:
    try:
        return proc.map(self.step, self.enum)
    except KeyboardInterrupt:
        print("[ JOB ] => Exiting Processes")

class Main:

    @staticmethod
    def setup():
        async def main():
            await build()
            await asyncio.sleep(1)
        return main

    @classmethod
    def run(cls):
        assign = cls.setup()

        async def processes():
            await asyncio.gather(assign())
            return 1
        print("[ Main ] => Turn On")
        asyncio.run(processes())
        print("[ Main ] => Shutdown")

'''
