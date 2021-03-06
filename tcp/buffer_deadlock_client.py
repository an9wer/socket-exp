import sys
import socket


def deadlock_client(bytecount):
    """ the client's input buffer will be filled.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bytecount = (bytecount + 15) // 16 * 16
    message = b"captialize this!"
    print("Sending", bytecount, "bytes of data, in chunks of 16 bytes")
    sock.connect(("127.0.0.1", 8080))
    sentcount = 0
    while sentcount < bytecount:
        sock.sendall(message)
        sentcount += len(message)
        print("\r   %d bytes sent" % sentcount, end=" ")
        sys.stdout.flush()

    print()
    sock.shutdown(socket.SHUT_WR)

    print("Receving all the data the server sends back")

    received = 0
    while True:
        data = sock.recv(42)
        if not received:
            print("   The first data received says", repr(data))
        if not data:
            break
        received += len(data)
        print("\r   %d bytes received" % received, end=" ")

    print()
    sock.close()


if __name__ == "__main__":
    # deadlock_client()
    deadlock_client(1073741824)
