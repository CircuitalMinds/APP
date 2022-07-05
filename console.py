from subprocess import getoutput


class Shell:
    fprint = False

    @staticmethod
    def input(command, *args):
        return f'{command} {"".join(list(args))}'

    @classmethod
    def run(cls, command, *args, **opts):
        if type(opts.get("fprint")) == bool:
            cls.fprint = opts["fprint"]
        cmd = cls.input(command, *args)
        out = getoutput(cmd).strip()
        if cls.fprint:
            print("\n\n".join([
                "Input:\n{}".format(cmd),
                "Output:\n{}".format(out)
            ]))
        return out
