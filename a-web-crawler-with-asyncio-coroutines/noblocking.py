"""
This fucntion not only wastes electricity, but it cannot efficiently await
events on multiple sockets. 
"""

import socket


def fetch(url):
    sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect(("xkcd.com", 80))
    except BlockingIOError as e:
        print(e)

    request = "GET {} HTTP/1.1\r\nHost: xkcd.com\r\n\r\n".format(url)
    encoded = request.encode("ascii")
    while True:
        try:
            sock.send(encoded)
            break
        except OSError as e:
            print(e)
    print("sent")
    sock.close()


if __name__ == "__main__":
    fetch("/")
