from bash import Sh
from multiprocessing import Pool, Process


class Boot:
    processes = []

    def add_process(self, func, *args):
        self.processes.append((func, args))

    def run(self, i):
        f, args = [self.processes[i][j] for j in (0, 1)]
        yi = f(*args)
        return yi

    def run_targets(self):
        n = len(self.processes)
        for i in range(n):
            p = Process(target=self.run, args=(i, ))
            p.start()
            p.join()

    def pool_process(self):
        n = len(self.processes)
        with Pool(n) as p:
            p.map(self.run, range(n))
