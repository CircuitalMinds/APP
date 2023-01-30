from libs.shell import CLI
import asyncio
from multiprocessing import Pool


class Process:

    def __init__(self, func, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.params = kwargs.get("params") or {}
        self.id = kwargs.get("id") or name
        self.func = func

    def call(self):
        if self.args and self.params:
            self.func(*self.args, **self.params)
        elif self.args:
            self.func(*self.args)
        else:
            self.func()

    def message(self, status):
        print("".join([
            "[ PROCESS ]  => (",
            f"\n\t[ id={self.id} ];",
            f"\n\t[ name={self.name} ];",
            f"\n\t[ status={status} ];",
            "\n);\n"
        ]))

    def run(self):
        self.message("running")
        self.message("finished")
        self.call()


class Job:

    def __init__(self, proc, *procs):
        self.processes = (proc, ) + procs
        self.count = len(self.processes)
        self.enum = range(self.count)

    def step(self, i):
        return self.processes[i].run()

    def init(self):
        print("[ JOB ] => Initializing Processes")
        with Pool(self.count) as proc:
            try:
                return proc.map(self.step, self.enum)
            except KeyboardInterrupt:
                print("[ JOB ] => Exiting Processes")


def build_site():
    CLI.input("bash make site")


def build_app():
    print("[ Application ] => Starting Build")
    print("[ Application ] => Running Successfully")
    CLI.input("bash make app")


async def build():
    Job(
        Process(build_app, "Application", id=1),
        Process(build_site, "Site", id=2)
    ).init()


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


if __name__ == "__main__":
    print("Processing ... ")
    CLI.do_sleep(1)
    CLI.clear()
    Main.run()
