import socket


def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 8080))
    sock.listen(1)
    print("Listening at", sock.getsockname())
    while True:
        # sock is a listening socket, which can use accept()
        # sc is a connected socket, which can use send(), recv()
        sc, sockname = sock.accept()
        print("We have accepted a connection from", sockname)
        print(" Socket name:", sc.getsockname())
        print(" Socket peer:", sc.getpeername())
        message = sc.recv(16)
        print(" Incomming message:", repr(message))
        sc.sendall(b"Farewell, client")
        sc.close()
        print(" Reply sent, socket closed")


if __name__ == "__main__":
    server()
