"""
By default, socket operations are blocking: when the thread calls a method like
connect or recv, it pauses until the operation completes.
"""

import socket


def fetch(url):
    sock = socket.socket()
    sock.connect(("kxcd.com", 80))
    request = "GET {} HTTP/1.1\r\nHost: xkcd.com\r\n\r\n".format(url)
    sock.send(request.encode("ascii"))
    response = b""
    chunk = sock.recv(4096)
    # it'll block here. because it'll never receive close sign from server side.
    while chunk:
        response += chunk
        chunk = sock.recv(4096)
        print(chunk)
    # the following code will never be executed.
    print(response)
    sock.close()
    

if __name__ == "__main__":
    fetch("/")
