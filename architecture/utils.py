import time
import socket

aphorisms = {
    b"Beautiful is better than?": b"Ugly.",
    b"Explicit is better than?": b"Implicit.",
    b"Simple is better than?": b"Complex.",
}

def get_answer(aphorism):
    time.sleep(0.0)
    return aphorisms.get(aphorism, b"Error: unknown aphorism.")


def recv_until(sock, suffix):
    message = sock.recv(4096)
    if not message:
        raise EOFError("socket closed")
    while not message.endswith(suffix):
        data = sock.recv(4096)
        if not data:
            raise IOError("received {!r} then socket closed".format(message))
        message += data
    return message
