import socket
import threading
from random import randint

import requests


class NodeClient:
    def __init__(self, handler):
        self.handler = handler
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def send(self):
        while True:
            self.client.send(input().encode())

    def listen(self):
        while True:
            message = self.client.recv(1024).decode()
            print(message)

    def connect(self, address):
        try:
            self.client.connect(address)
            print("Connected successfully")
        except OSError as error:
            print(error)
