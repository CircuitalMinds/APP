# -*- coding: utf-8 -*-
from libs.shell import CLI
from sys import argv
if __name__ == "__main__":
    opt = argv[1] if argv[1:] else None
    if opt in ("server", "api", "site"):
        CLI.input(f"bash make {opt}")
