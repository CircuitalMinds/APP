from libs.utils import getjson, base_path, timeout, save_json
folder_data = base_path.joinpath("application/history")


class Worker:
    jobs = dict()
    connected = False
    filepath = folder_data.joinpath("worker.json")

    @property
    def scheme(self):
        return dict(
            id=int,
            processes=dict,
            args=dict,
            status=bool,
            messages=dict,
            date=str
        )

    def update(self):
        data = getjson(self.filepath)
        self.jobs.update(data["jobs"])
        self.connected = data["connected"]

    def connect(self):
        self.update()
        self.connected = True
        save_json(
            self.filepath,
            dict(
                jobs=self.jobs,
                connected=self.connected
            )
        )

        def wait_func():
            self.update()
            if not self.jobs:
                print("waiting", self.connected)
            else:
                print(self.jobs)

        while self.connected:
            timeout(wait_func, 5)
        KeyboardInterrupt()


Worker().connect()





