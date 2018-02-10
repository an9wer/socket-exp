import socket


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # TCP connect() is different from UPD's, it'll raise 'Connection refused'
    # error when the server is not running. but if the firewall is opened in
    # server side, the connection will hang up.
    sock.connect(("127.0.0.1", 8080))
    print("Client has been assigned socket name", sock.getsockname())
    sock.sendall(b"hello world")
    reply = sock.recv(16)
    print("The server said", repr(reply))
    sock.close()


if __name__ == "__main__":
    client()
