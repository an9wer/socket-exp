import socket
import selectors


selector = selectors.DefaultSelector()
keep_running = True

outgoing = [b"hello world!", b"I'm an9wer."]
bytes_sent, bytes_received = 0, 0


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 8080))
sock.setblocking(0)

selector.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE)

while keep_running:
    print("Waiting for I/O")
    for key, mask in selector.select(timeout=1):
        sc = key.fileobj
        address = sc.getpeername()
        print(" server({})".format(address))

        if mask & selectors.EVENT_READ:
            print(" ready to read")
            data = sc.recv(4)
            if data:
                print(" received {!r}".format(data))
                bytes_received += len(data)

            keep_running = not (bytes_received == bytes_sent)
            if not keep_running:
                import time; time.sleep(5)

        if mask & selectors.EVENT_WRITE:
            print(" ready to write")
            if not outgoing:
                print(" sending nothing")
                selector.modify(sc, selectors.EVENT_READ)
            else:
                next_msg = outgoing.pop()
                print(" sending {!r}".format(next_msg))
                sc.sendall(next_msg)
                bytes_sent += len(next_msg)

print("shutting down")
selector.unregister(sc)
sc.close()
selector.close()
