import threading

from . import server


def start_threads(listener, workers=2):
    for i in range(workers):
        threading.Thread(
            target=server.accept_connections_forever, args=(listener,)).start()


if __name__ == "__main__":
    listener = server.create_srv_socket()
    start_threads(listener)
