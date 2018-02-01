import time
import random
import socket
from . import utils


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 8080))
    aphorisms = list(utils.aphorisms)
    for aphorism in random.sample(aphorisms, 3):
        time.sleep(5)
        sock.sendall(aphorism)
        print(aphorism, utils.recv_until(sock, b"."))
    sock.close()


if __name__ == "__main__":
    client()
