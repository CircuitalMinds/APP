from werkzeug.middleware.shared_data import SharedDataMiddleware
from multiprocessing import Pool
from os.path import join, dirname
from werkzeug.wrappers import Request, Response


@Request.application
def application(request):
    return Response("Hello, World!")


def run(process):
    process.run()


def main(receiver, server):
    processes = [receiver, server]
    with Pool(len(processes)) as p:
        try:
            p.map(run, processes)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    from werkzeug.serving import run_simple
    app = SharedDataMiddleware(application, {
        '/static': join(dirname(__file__), 'static')
    })
    run_simple("localhost", 5000, application)
