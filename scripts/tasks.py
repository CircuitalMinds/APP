import asyncio


class Task:
    jobs = ()

    @staticmethod
    def create(data):
        func, name, args, kwargs = (
            data[0], data[1],
            data[2] if data[2:] else (),
            data[3] if data[3:] else {}
        )

        async def job():
            out = func(*args, **kwargs)
            await asyncio.sleep(2)
            print(f"job {name} finished")
            return out
        return job

    def add(self, step, *steps):
        self.jobs = (
            self.create(n) for n in (step, ) + steps
        )

    def start(self):
        async def main():
            data = await asyncio.gather(*[
                f() for f in self.jobs
            ])
            return data
        return asyncio.run(main())

