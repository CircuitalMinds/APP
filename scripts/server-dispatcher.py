import asyncio


class Server(asyncio.Protocol):
    transport = None

    @staticmethod
    def run():
        return Server()

    def connection_made(self, transport):
        peer_name = transport.get_extra_info("peername")
        print("Connection from {}".format(peer_name))
        self.transport = transport

    def data_received(self, data):
        msg = data.decode()
        print(f"Data received:\n\t{msg}")
        print('Send: {!r}'.format(f"{msg} received"))
        self.transport.write(data)
        print('Close the client socket')
        self.transport.close()


def run():

    async def start():
        address = dict(host="192.168.50.100", port=8888)
        loop = asyncio.get_running_loop()
        server = await loop.create_server(Server.run, **address)
        async with server:
            await server.serve_forever()
    asyncio.run(start())


if __name__ == "__main__":
    run()
