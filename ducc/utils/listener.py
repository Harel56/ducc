import socket
from .connection import Connection


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.socket = None

    def __repr__(self):
        return f'Listener(port={self.port}, host={self.host!r}, backlog={self.backlog}, reuseaddr={self.reuseaddr})'

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception, error, traceback):
        self.stop()

    def start(self):
        s = socket.socket()
        if self.reuseaddr:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(self.backlog)
        self.socket = s

    def stop(self):
        if self.socket is not None:
            self.socket.close()

    def accept(self):
        return Connection(self.socket.accept()[0])

