import socket
import selectors


selector = selectors.DefaultSelector()
keep_running = True


def read(sc, mask):
    global keep_running
    client_address = sc.getpeername()
    print(" read({})".format(client_address))
    data = sc.recv(1024)
    if data:
        print(" recvied {!r}".format(data))
        sc.sendall(data)
    else:
        print(" closing")
        selector.unregister(sc)
        sc.close()
        keep_running = False


def accept(sock, mask):
    sc, addr = sock.accept()
    print(" accept({})".format(addr))
    sc.setblocking(False)
    selector.register(sc, selectors.EVENT_READ, read)


def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 8080))
    sock.listen(5)

    selector.register(sock, selectors.EVENT_READ, accept)

    while keep_running:
        print("Waiting for I/O")
        for key, mask in selector.select(timeout=1):
            callback = key.data
            callback(key.fileobj, mask)

    print("shutting down")
    selector.close()


if __name__ == "__main__":
    server()
