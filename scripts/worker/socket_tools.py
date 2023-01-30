import socket
import sys


def basic_socket(host, port):
    # specify Host and Port
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # With the help of bind() function
        # binding host and port
        soc.bind((host, port))
    except socket.error as massage:
        # if any error occurs then with the
        # help of sys.exit() exit from the program
        print('Bind failed. Error Code : '
              + str(massage[0]) + ' Message '
              + massage[1])
        sys.exit()
    # print if Socket binding operation completed
    print('Socket binding operation completed')
    # With the help of listening () function
    # starts listening
    soc.listen(9)
    conn, address = soc.accept()
    # print the address of connection
    print('Connected with ' + address[0] + ':'
          + str(address[1]))


def get_socket(host, port):
    # importing required modules
    import socket
    import datetime
    # initializing socket
    s = socket.socket()
    # binding port and host
    s.bind((host, port))
    # waiting for a client to connect
    s.listen(5)
    while True:
        # accept connection
        c, addr = s.accept()
        print('got connection from addr', addr)
        date = datetime.datetime.now()
        d = str(date)
        # sending data type should be string and encode before sending
        c.send(d.encode())
        c.close()


def connecting(host, port):
    s = socket.socket()
    # connect to host
    s.connect((host, port))
    # recv message and decode here 1024 is buffer size.
    print (s.recv(1024).decode())
    s.close()


def scanner(target, ports):
    import threading
    from queue import Queue
    import time
    import socket
    # a print_lock is used to prevent "double"
    # modification of shared variables this is
    # used so that while one thread is using a
    # variable others cannot access it Once it
    # is done, the thread releases the print_lock.
    # In order to use it, we want to specify a
    # print_lock per thing you wish to print_lock.
    print_lock = threading.Lock()
    # ip = socket.gethostbyname(target)
    def portscan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con = s.connect((target, port))
            with print_lock:
                print('port is open', port)
            con.close()
        except:
            print('port is close', port)
    # The threader thread pulls a worker
    # from a queue and processes it
    def threader():
        while True:
            # gets a worker from the queue
            worker = q.get()
            # Run the example job with the available
            # worker in queue (thread)
            portscan(worker)
            # completed with the job
            q.task_done()
    # Creating the queue and threader
    q = Queue()
    # number of threads are we going to allow for
    for x in range(4):
        t = threading.Thread(target=threader)
        # classifying as a daemon, so they it will
        # die when the main dies
        t.daemon = True
        # begins, must come after daemon definition
        t.start()
    start = time.time()
    # 10 jobs assigned.
    for worker in ports:
        q.put(worker)
    # wait till the thread terminates.
    q.join()