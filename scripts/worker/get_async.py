import asyncio
loop = asyncio.get_event_loop()


def init():
    while True:
        async def outer():
            print('in outer')
            print('waiting for result 1')
            result1 = await phase1()
            print('waiting for result 2')
            result2 = await phase2(result1)
            return result1, result2

        async def phase1():
            print('in phase1')
            return 'phase1 result'

        async def phase2(arg):
            print('in phase2')
            return 'result2 derived from {}'.format(arg)

        asyncio.run(outer())


try:
    init()
except KeyboardInterrupt:
    print("stop")
