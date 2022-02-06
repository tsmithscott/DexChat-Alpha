import socket
import threading
from random import randint

import requests


class NodeServer:
    def __init__(self, handler):
        self.handler = handler
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_i = "127.0.0.1"
        self.host_e = requests.get("https://api.ipify.org").text
        self.port = randint(49152, 65535)
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen(5)

    def save_connection(self, sock, address):
        self.handler.add_peer((sock, address))

    @staticmethod
    def receive_message(self, cnx, address):
        while True:
            try:
                message = cnx.recv(1024).decode()
                print(message)
            except OSError:
                break

    # def get_address(self):
    #     return self.host_e, self.port
    #
    # def get_socket(self):
    #     return self.sock, self.get_address()

