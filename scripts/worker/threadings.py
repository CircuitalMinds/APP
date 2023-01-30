from multiprocessing import Process
import os

worker = [
    {"id": 1, "steps": [f"step {step} starting" for step in range(2)], "name": "tester1"},
    {"id": 2, "steps": [f"step {step} starting" for step in range(2)], "name": "tester2"},
    {"id": 3, "steps": [f"step {step} starting" for step in range(2)], "name": "tester3"},
]


def init_process(i):
    job = worker[i]
    print(job)
    print(job['id'])
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    for s in job['steps']:
        print(s)
    print(f'job {job["name"]} terminated')


if __name__ == '__main__':
    from time import time
    t0 = time()
    for i in range(len(worker)):
        init_process(i)
    print(time() - t0)
    t0 = time()
    for i in range(len(worker)):
        p = Process(target=init_process, args=(i,))
        p.start()

    print(time() - t0)