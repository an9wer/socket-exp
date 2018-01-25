import socket


MAX_BYTES = 65535


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_text = "hello world"
    send_data = bytes(send_text, "utf-8")
    sock.sendto(send_data, ("127.0.0.1", 8080))
    print("the OS assigned me the address {}".format(sock.getsockname()))

    # block until receiving some data
    recv_data, peer_address = sock.recvfrom(MAX_BYTES)
    recv_text = str(recv_data, "utf-8")
    print(recv_text, peer_address)


def delay_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # why use connection here?
    # ------------------------------------------------------------------------
    # firstly:
    # the connect() call lets the operating system know ahead of time the
    # remote address to which you want to send packets so that you can simply
    # supply data to the send() call and not have to repeat the server address
    # again.
    #
    # secondly:
    # once you have run connect(), the operating system will discard any
    # incoming packets to your port whose return address does not match the
    # address to which you have connected.
    sock.connect(("127.0.0.1", 8080))
    print("Client socket name is {}".format(sock.getsockname()))

    delay = 0.1
    send_text = "hello world"
    send_data = bytes(send_text, "utf-8")
    while True:
        sock.send(send_data)
        print("Waiting up to {} seconds for a reply".format(delay))
        sock.settimeout(delay)
        try:
            recv_data = sock.recv(MAX_BYTES)
        except socket.timeout:
            delay *= 2
            if delay > 2.0:
                raise RuntimeError("I think the server is down")
        else:
            break

    recv_text = str(send_data)
    print("The server says {!r}".format(recv_text))


if __name__ == "__main__":
    #client()
    delay_client()
