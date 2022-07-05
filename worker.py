from containers.task import Task, get_videos_metadata
from containers.build import Videos
from libs.finder import YouTube
from libs.file import Json
from libs import Chars


class Task:
    def __init__(self, f):
        self.f = f

    def run(self):
        self.f()


task = Task(get_videos_metadata(
    Videos.update_all(), YouTube().dataset, Json, Chars
))
task.run()
