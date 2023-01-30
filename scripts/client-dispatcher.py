import asyncio


class Client(asyncio.Protocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    @staticmethod
    def run(msg, lostdata):
        def f():
            return Client(msg, lostdata)
        return f

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)


def run():

    async def start():
        loop = asyncio.get_running_loop()
        on_con_lost = loop.create_future()
        address = dict(host="192.168.50.100", port=8888)
        message = 'Hello!'
        transport, protocol = await loop.create_connection(
            Client.run(message, on_con_lost), **address
        )
        try:
            await on_con_lost
        finally:
            transport.close()
    asyncio.run(start())


if __name__ == "__main__":
    run()
