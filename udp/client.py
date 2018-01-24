import socket


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_text = "hello world"
    send_data = bytes(send_text, "utf-8")
    sock.sendto(send_data, ("127.0.0.1", 8080))
    print("the OS assigned me the address {}".format(sock.getsockname()))

    # block until receiving some data
    recv_data, peer_address = sock.recvfrom(100)
    recv_text = str(recv_data, "utf-8")
    print(recv_text, peer_address)


if __name__ == "__main__":
    client()
