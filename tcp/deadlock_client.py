import socket


def deadlock_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 8080))
    print("Client has been assigned socket name", sock.getsockname())
    sock.sendall(b"hello world!")
    data = b""
    # 不会进入该循环，因为 server 被阻塞了
    while True:
        reply = sock.recv(8)
        if not reply:
            break
        print(" Receive 8 bytes data: {!r}".format(reply))
        data += reply
    print("The server said {!r}".format(repr(data)))
    sock.close()


if __name__ == "__main__":
    deadlock_client()
