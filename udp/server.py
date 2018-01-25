import socket
import random


MAX_BYTES = 65535

def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 8080))
    print("Listening at {}".format(sock.getsockname()))

    while True:
        # block until receiving some data
        recv_data, peer_address = sock.recvfrom(MAX_BYTES)
        recv_text = str(recv_data, "utf-8")
        print("The client at {} says {!r}".format(peer_address, recv_text))

        send_text = "Your data was {} bytes long".format(len(recv_data))
        send_data = bytes(send_text, "utf-8")
        sock.sendto(send_data, peer_address)

def delay_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 8080))
    print("Listening at", sock.getsockname())
    while True:
        recv_data, peer_address = sock.recvfrom(MAX_BYTES)
        if random.random() < 0.5:
            print("Pretending to drop packet from {}".format(peer_address))
            continue
        recv_text = str(recv_data, "utf-8")
        print("The client at {} says {!r}".format(peer_address, recv_text))
        send_text = "Your data was {} bytes long".format(len(recv_data))
        send_data = bytes(send_text, "utf-8")
        sock.sendto(send_data, peer_address)


if __name__ == "__main__":
    #server()
    delay_server()
