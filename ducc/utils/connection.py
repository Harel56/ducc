import socket
import struct


class Connection:
    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        return '<Connection from %s:%d to %s:%d>' % (*self.local_name(), *self.peer())

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.close()
        
    @classmethod
    def connect(cls, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        return cls(sock)

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, size):
        data = b''
        while len(data) < size:
            buf = self.socket.recv(size - len(data))
            if not buf:
                raise Exception()
            data = data + buf
        return data

    def send_message(self, data):
        self.send(struct.pack('I', len(data)) + data)

    def receive_message(self):
        return self.receive(int.from_bytes(self.receive(4), 'little'))

    def close(self):
        self.socket.close()

    def local_name(self):
        """
        local_name() -> address info

        Return the address of the local endpoint.  For IP sockets, the address
        info is a pair (hostaddr, port).
        """
        return self.socket.getsockname()

    def peer(self):
        """
        peer() -> address info

        Return the address of the remote endpoint.  For IP sockets, the address
        info is a pair (hostaddr, port).
        """
        return self.socket.getpeername()
