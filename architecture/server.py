import socket

from . import utils


def create_srv_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 8080))
    sock.listen(5)
    print("Listening at {}".format(sock.getsockname()))
    return sock


def accept_connections_forever(sock):
    while True:
        sc, address = sock.accept()
        print("Accepted connection from {}".format(address))
        handle_conversation(sc, address)


def handle_conversation(sock, address):
    try:
        while True:
            handle_request(sock)
    except EOFError:
        print("Client socket to {} has closed".format(address))
    except Exception as e:
        print("Client {} error: {}".format(address, e))
    finally:
        sock.close()


def handle_request(sock):
    aphorism = utils.recv_until(sock, b"?")
    answer = utils.get_answer(aphorism)
    sock.sendall(answer)


if __name__ == "__main__":
    sock = create_srv_socket()
    accept_connections_forever(sock)
