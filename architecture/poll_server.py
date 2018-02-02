import select

from . import utils
from . import server


def all_events_forever(poll_obj):
    """ event loop
    """
    while True:
        for fd, event in poll_obj.poll():
            yield fd, event


def serve(listener):
    sockets = {listener.fileno(): listener}
    addresses = {}
    bytes_received = {}
    bytes_to_send = {}

    poll_obj = select.poll()
    poll_obj.register(listener, select.POLLIN)

    for fd, event in all_events_forever(poll_obj):
        sock = sockets[fd]

        # Socket closed: remove it from our data structures.

        if event & (select.POLLHUP | select.POLLERR | select.POLLNVAL):
            address = addresses.pop(sock)
            rb = bytes_received.pop(sock, b"")
            sb = bytes_to_send.pop(sock, b"")
            if rb:
                print("Client {} sent {} but then closed".format(address, rb))
            elif sb:
                print("Client {} closed before we sent {}".format(address, sb))
            else:
                print("Client {} closed socket normally".format(address))
            poll_obj.unregister(fd)
            del sockets[fd]

        # New socket: add it to our data structures.

        elif sock is listener:
            sock, address = sock.accept()
            print("Accepted connection from {}".format(address))
            sock.setblocking(False)         # force socket.timeout if we blunder
            sockets[sock.fileno()] = sock
            addresses[sock] = address
            poll_obj.register(sock, select.POLLIN)

        # Incoming data: keep receiving until we see the suffix.

        elif event & select.POLLIN:
            more_data = sock.recv(4096)
            if not more_data:
                sock.close()
                continue
            data = bytes_received.pop(sock, b"") + more_data
            if data.endswith(b"?"):
                bytes_to_send[sock] = utils.get_answer(data)
                poll_obj.modify(sock, select.POLLOUT)
            else:
                bytes_received[sock] = data

        # Socket ready to send: keep sending until all bytes are delivered.

        elif event & select.POLLOUT:
            data = bytes_to_send.pop(sock)
            n = sock.send(data)
            if n < len(data):
                bytes_to_send[sock] = data[n:]
            else:
                poll_obj.modify(sock, select.POLLIN)


if __name__ == "__main__":
    listener = server.create_srv_socket()
    serve(listener)
