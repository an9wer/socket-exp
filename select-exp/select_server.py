import queue
import select
import socket


def server(timeout=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 8080))
    sock.listen(5)
    print("Listening at", sock.getsockname())
    
    # inputs is a list of sockets from which we expect to read
    # outputs is a list of sockets to which we expect to write
    inputs, outputs, message_queues = [sock], [], {}

    while True:
        print("Waiting for the next event")
        if timeout:
            # When the timeout expires, select() returns three empty lists. 
            readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
        else:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)

        # handle inputs
        for r in readable:

            if r is sock:
                sc, sockname = sock.accept()
                print("We have accepted a connection from {}".format(sockname))
                sc.setblocking(0)
                inputs.append(sc)
                message_queues[sc] = queue.Queue()

            else:
                data = r.recv(8)
                if data:
                    print(" Recived {!r} from {}".format(data, r.getpeername()))
                    message_queues[r].put(data)
                    # add output channel for response
                    if r not in outputs:
                        outputs.append(r)
                else:
                    print(" Recived nothing, closing {}".format(r.getpeername()))
                    if r in outputs:
                        outputs.remove(r)
                    inputs.remove(r)
                    r.close()
                    del message_queues[r]

        # handle outputs
        for w in writable:
            try:
                next_msg = message_queues[w].get_nowait()
            except queue.Empty:
                print(" Sending nothing")
                outputs.remove(w)
            else:
                print(" Sending {!r} to {}".format(next_msg, w.getpeername()))
                w.send(next_msg)

        # handle exceptional conditions
        for e in exceptional:
            print(" Exception condition on {}".format(e.getpeername()))
            inputs.remove(e)
            if e in outputs:
                outputs.remove(e)
            e.close()
            del message_queues[e]


if __name__ == "__main__":
    #server()
    server(2)
