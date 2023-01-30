from modules import FileObj, from_root, timer


class Worker:
    data = {}
    file_path = from_root("dataset", "workers.json")

    def __init__(self, **data):
        self.set(**data)

    @staticmethod
    def connect():
        info = FileObj(Worker.file_path)
        info.clear()
        info.update(**{"main": {"status": "connected"}})
        data = {"id": str(info.len), "status": "waiting"}
        info.update(**{data["id"]: {"status": data["status"]}})
        try:
            while True:
                for i in info.keys:
                    if i != "main":
                        print(f"id_{i}: ", info.get(i))
                timer(5)
                info = FileObj(Worker.file_path)
        except KeyboardInterrupt:
            info.clear()
            info.update(**{"main": {"status": "disconnected"}})
            print(info.data)

    def get(self, key):
        return self.data.get(key)

    def set(self, **data):
        self.data.update(data)

    def close(self):
        info = FileObj(self.file_path)
        info.pop(self.get("id"))
        info.update()


if __name__ == "__main__":
    Worker.connect()
