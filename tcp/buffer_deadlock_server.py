import sys
import socket


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
    deadlock_server()
