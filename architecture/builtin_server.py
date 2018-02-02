from socketserver import BaseRequestHandler, TCPServer, ThreadingMixIn

from . import server


class Handler(BaseRequestHandler):
    def handle(self):
        server.handle_conversation(self.request, self.client_address)


class Server(ThreadingMixIn, TCPServer):
    allow_reuse_address = 1


if __name__ == "__main__":
    s = Server(("127.0.0.1", 8080), Handler)
    print(s.server_address)
    s.serve_forever()
