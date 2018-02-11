import queue
import select
import socket


READ_ONLY = (select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR)
READ_WRITE = READ_ONLY | select.POLLOUT


def server(timeout=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 8080))
    sock.listen(5)
    print("Listening at", sock.getsockname())

    message_queues = {}

    poller = select.poll()
    poller.register(sock, READ_ONLY)

    fd_to_socket = {sock.fileno(): sock}

    while True:
        print("Waiting for the next event")
        if timeout:
            events =  poller.poll(timeout)
        else:
            events = poller.poll()

        for fd, flag in events:
            print(111, fd, flag)
            s = fd_to_socket[fd]

            if flag & (select.POLLIN | select.POLLPRI):

                if s is sock:
                    sc, sockname = s.accept()
                    print("We have accepted a connection from {}".format(sockname))
                    sc.setblocking(0)
                    fd_to_socket[sc.fileno()] = sc
                    poller.register(sc, READ_ONLY)

                    message_queues[sc] = queue.Queue()
                else:
                    data = s.recv(1024)
                    if data:
                        print(" Recived {!r} from {}".format(data, s.getpeername()))
                        message_queues[s].put(data)
                        # add output channel for response
                        poller.modify(s, READ_WRITE)
                    else:
                        print(" Recived nothing, closing {}".format(s.getpeername()))
                        poller.unregister(s)
                        s.close()
                        del message_queues[s]

            elif flag & select.POLLOUT:
                try:
                    next_msg = message_queues[s].get_nowait()
                except queue.Empty:
                    print(" Sending nothing")
                    poller.modify(s, READ_ONLY)
                else:
                    print(" Sending {!r} to {}".format(next_msg, s.getpeername()))
                    s.send(next_msg)

            elif flag & select.POLLERR:
                print(" Exception condition on {}".format(s.getpeername()))
                poller.unregister(s)
                s.close()
                del message_queues[s]


if __name__ == "__main__":
    # server()
    server(2000)    #ms
