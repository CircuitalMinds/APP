from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.serving import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from libs.utils import get_host, base_path, dumper
import asyncio


class Route:

    @staticmethod
    def home(app):
        @app.route("/")
        def home():
            Sender.run(
                "{request: /}"
            )
            return jsonify(response=200)


class App:
    name = "app"
    folders = dict(
        template_folder=str(base_path.joinpath("templates")),
        static_folder=str(base_path.joinpath("static"))
    )

    @classmethod
    def init(cls):
        return cls.create(cls)

    def create(self):
        app = Flask(
            self.name,  **self.folders
        )
        CORS(app)
        Route.home(app)
        return app


class Server:
    host = get_host()
    port = 8000
    opts = dict(
        use_reloader=True, use_debugger=True, use_evalex=True
    )

    @classmethod
    def run(cls):
        application = DispatcherMiddleware(App.init())
        run_simple(
            cls.host, cls.port,  application, **cls.opts
        )


class Receiver(asyncio.Protocol):
    transport = None

    @staticmethod
    def run():
        def emit():
            return Receiver()

        async def start():
            address = dict(host=Server.host, port=8888)
            loop = asyncio.get_running_loop()
            server = await loop.create_server(emit, **address)
            async with server:
                await server.serve_forever()
        asyncio.run(start())

    def connection_made(self, transport):
        peer_name = transport.get_extra_info("peername")
        print("=== RECEIVER ===")
        print("Connection from {}".format(peer_name))
        print("=============")
        self.transport = transport

    def data_received(self, data):
        datastr = data.decode()
        parsed = dumper(datastr)
        print("=== RECEIVER ===")
        print(f"Data received:\n\t{datastr}")
        print("=============")
        self.transport.write(b'{"response": 200}')
        self.transport.close()


class Sender(asyncio.Protocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    @staticmethod
    def run(msg):

        async def start():
            loop = asyncio.get_running_loop()
            on_con_lost = loop.create_future()
            address = dict(host=Server.host, port=8888)
            transport, protocol = await loop.create_connection(
                lambda: Sender(msg, on_con_lost), **address
            )
            try:
                await on_con_lost
            finally:
                transport.close()
        asyncio.run(start())

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print("=== SENDER ===")
        print(f"Data sent:\n\t{format(self.message)}")
        print("============")

    def data_received(self, data):
        print("=== SENDER ===")
        print(f"Data received:\n\t{format(data.decode())}")
        print("============")

    def connection_lost(self, exc):
        print("=== SENDER ===")
        print('The server closed the connection')
        self.on_con_lost.set_result(True)
        print("============")
