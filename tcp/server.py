import sys
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


def deadlock_server():
    """ the server's input buffer will be filled.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 8080))
    sock.listen(1)
    print("Listening at", sock.getsockname())
    while True:
        sc, sockname = sock.accept()
        print("Processing up to 1024 bytes at a time from", sockname)
        n = 0
        while True:
            data = sc.recv(1024)
            if not data:
                break
            data = bytes(str(data, "utf-8").upper(), "utf-8")
            sc.sendall(data)
            n += len(data)
            print("\r   %d bytes processed so far" % n, end=" ")
            sys.stdout.flush()
        print()
        sc.close()
        print("   Socket closed")


if __name__ == "__main__":
    #server()
    deadlock_server()
