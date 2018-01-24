import socket


def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 8080))
    print("Listening at {}".format(sock.getsockname()))

    while True:
        # block until receiving some data
        recv_data, peer_address = sock.recvfrom(2)
        recv_text = str(recv_data, "utf-8")
        print("The client at {} says {!r}".format(peer_address, recv_text))

        send_text = "Your data was {} bytes long".format(len(recv_data))
        send_data = bytes(send_text, "utf-8")
        sock.sendto(send_data, peer_address)


if __name__ == "__main__":
    server()
