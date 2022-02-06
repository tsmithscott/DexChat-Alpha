import socket
import threading
from random import randint

import requests


class NodeServer:
    def __init__(self, handler):
        self.handler = handler
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', 25574))
        self.server.listen(5)

    def accept(self):
        while True:
            peer, address = self.server.accept()
            self.handler.add_peer((peer, address))
            print(f"[{address} Connected]")
            peer.send(bytes(f"[{address} Connected]"))
