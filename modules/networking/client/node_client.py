import socket
from random import randint
from uuid import uuid4


class NodeClient:
    def __init__(self, host, port, handler):
        self.address = socket.gethostbyname(str(socket.gethostname))
        self.server = host, port


