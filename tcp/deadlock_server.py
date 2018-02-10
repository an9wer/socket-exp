import socket


def deadlock_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 8080))
    sock.listen(1)
    print("Listening at", sock.getsockname())
    while True:
        # sock is a listening socket, which can use accept()
        # sc is a connected socket, which can use send(), recv()
        sc, sockname = sock.accept()
        print("We have accepted a connection from", sockname)
        data = b""
        while True:
            # 这里 recv() 完 client 传来的最后一个数据后，会一直阻塞
            # 因为 client 中 sendall() 之后没有 close(), 只有在
            # client close() 之后 recv() 才不会阻塞，得到空字符串 ""
            # 之后的 if not message 语句才会生效
            #
            # 也就是说socket 一端的 recv() 和另一端的 close() 必须
            # 配合好，否则很容易造成死锁
            #
            # 有一种比较好的方案是类似 HTTP 中 Content-Length，指明
            # 发送端发送的数据长度，然后接收端根据这个长度来 recv() 数据
            message = sc.recv(8)
            if not message:
                break
            print(" Receive 8 byte data: {!r}".format(message))
            data += message
        print("The client said {!r}".format(repr(data)))
        sc.sendall(b"Farewell, client")
        sc.close()


if __name__ == "__main__":
    deadlock_server()
