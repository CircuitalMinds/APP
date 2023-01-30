from subprocess import getoutput
from json import load
from os import listdir, environ
from os.path import join


class Command:
    data = []

    def get_line(self):
        line = " && ".join(self.data)
        self.new_line()
        return line

    def set_line(self, *commands):
        self.data.extend(commands)

    def new_line(self):
        self.data.clear()


class Sh(Command):
    path = join(
        "/", *__file__.split("/")[:-1]
    )

    def __init__(self, *commands):
        self.scripts = {
            i.replace(".sh", ""): join(self.path, i)
            for i in listdir(self.path)
        }
        self.set_line(*commands)

    @staticmethod
    def prompt(line):
        out = getoutput(line)
        print(out)
        return out

    @staticmethod
    def login():
        return load(open(join(
            environ.get('HOME'), "credentials.json"
        ))).get("desktop")

    def run_script(self, name):
        script = self.scripts.get(name)
        if script:
            self.set_line(f"bash {script}")
            return self.prompt(self.get_line())

    def run_command(self, *commands):
        self.set_line(*commands)
        self.prompt(self.get_line())

    def __call__(self, line):
        return self.prompt(line)


Sh().run_script("test")