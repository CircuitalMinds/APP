import threading, socket, os, time


def scanport(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        if s.connect_ex((target, port)) == 0:
            portlist.append(port)
            print(f"Port {port} is open." + "\t" * 10)

        print(f"Current port: {port}" + "\t", end="\r")
        s.close()        

    except:
        pass


if __name__ == "__main__":
    portlist, target, finish = [], "google.com", 0

    threads = [threading.Thread(target=scanport, kwargs={'port': i}) for i in range(80, 85)]
    threads[0].start
    threads[0].join
    
    for t in threads:
        t.start()
        time.sleep(1)
    [t.join() for t in threads]
    print(portlist)
