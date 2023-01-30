import asyncio


def runcmd():

    async def getout():
        command = input("Input: ")
        out = None
        try:
            out = await asyncio.create_subprocess_shell(
                f"echo $( {command} )",
                shell=True
            )
            await out.communicate()
        except asyncio.CancelledError:
            out.terminate()
            print("canceled")

    async def cmd():
        try:
            await asyncio.wait_for(getout(), 60)
        except asyncio.TimeoutError:
            print("timeout")
    while True:
        try:
            asyncio.run(cmd())
        except KeyboardInterrupt:
            pass
