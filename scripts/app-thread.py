from threading import Thread
from flask import Flask
from werkzeug.serving import make_server
import logging
import asyncio
from time import sleep


class Processor:

    def __init__(self):
        self.tasks = []
        self.loop = asyncio.get_event_loop()

    def add_task(self, f, t):
        self.tasks.append(self.loop.create_task(self.timer(f, t)))

    def delete_task(self, index):
        self.tasks.pop(index)

    def run(self):
        self.loop.run_until_complete(asyncio.wait(self.tasks))
        self.loop.close()

    async def timer(self, f, tn):
        while tn > 0:
            tn = await self.offset(tn)
            f()

    @staticmethod
    async def offset(tn):
        print(tn)
        sleep(1)
        tn -= 1
        return tn


class ServerThread(Thread):

    def __init__(self, app):
        Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        logging.info('starting server')
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


def start_server():
    app = Flask('myapp')
    # App routes defined here
    server = ServerThread(app)
    server.start()
    logging.info('server started')
    server.shutdown()

