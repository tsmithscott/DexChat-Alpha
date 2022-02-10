import socket
import threading


class Server:
    def __init__(self):
        self.PEERS = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((socket.gethostname(), 25000))

    def run(self):
        self.server.listen(5)
        while True:
            conn, addr = self.server.accept()
            self.PEERS.append((conn, addr))
            conn.send(f"Connected! ".encode())
            threading.Thread(target=self.receive, args=(conn, ), daemon=True).start()

    def receive(self, connection):
        while True:
            message = connection.recv(4096)
            print(message.decode())


class Client:
    def __init__(self, host, port):
        self.PEERS = []
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.connect((host, port))
        self.client.listen(5)

    def update(self, peers):
        self.PEERS = peers

    def send(self):
        while True:
            message = input("Message: ")

            self.client.send(message.encode())

