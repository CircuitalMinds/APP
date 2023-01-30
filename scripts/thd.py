from multiprocessing import Pool
from threading import Thread
import time


def counter(name, delay, n):
    while n:
        time.sleep(delay)
        print(f'{name, time.ctime(time.time()), n}')
        n -= 1


def init_counter(i):
    end_value = 2

    class Thd(Thread):
        def __init__(self, name, end_value):
            Thread.__init__(self)
            self.name = name
            self.end_value = end_value

        def run(self):
            print("Starting: " + self.name + "\n")
            counter(self.name, 1, self.end_value)
            print("Exiting: " + self.name + "\n")

    t = Thd(f"Thread {i}", end_value)
    t.start()
    t.join()
    print(f"Exiting Main Thread {i}")



n = 4

with Pool(n) as p:
    p.map(init_counter, range(n))

