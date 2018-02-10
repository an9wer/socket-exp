import socket


def recvall(sock, length):
    data = b""
    while len(data) < length:
        reply = sock.recv(length - len(data))
        if not reply:
            break
        data += reply
    return  data


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 8080))
    print("Client has been assigned socket name", sock.getsockname())
    send_msg = b"hello world!"
    import time; time.sleep(5)
    sock.sendall(send_msg)
    import time; time.sleep(5)
    data = recvall(sock, len(send_msg))
    print("The server said {!r}".format(repr(data)))
    sock.close()


if __name__ == "__main__":
    client()
