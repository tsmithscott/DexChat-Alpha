import socket
import select
import sys
import threading


class Server:
    def __init__(self, ip_addr: str, port: int):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.peers = []

        try:
            self.server.bind((ip_addr, port))
            self.server.listen(50)
        except RuntimeError as error:
            print(error)

    def send_message(self, ip_addr, message):
        current_connection = None

        for peer in self.peers:
            if peer[0][0] == ip_addr:
                current_connection = peer[1]

        try:
            current_connection.send(message)
        except RuntimeError:
            current_connection.close()

            for peer in self.peers:
                if peer[0][0] == ip_addr:
                    self.peers.remove(self.peers.index(peer))

    def receive_message(self, connection, address):
        while True:
            try:
                message = connection.recv(2048)

                if message:
                    print(f"[{address[0]}]: {message.decode()}")
                else:
                    for peer in self.peers:
                        if peer[0][0] == address:
                            self.peers.remove(self.peers.index(peer))
            except RuntimeError:
                continue

    def send_audio(self):
        pass

    def receive_audio(self):
        pass

    def accept(self):
        connection, addr = self.server.accept()

        self.peers.append([addr, connection])

        print(addr[0] + " connected.")

        threading.Thread(self.receive_message(connection, addr))

    def close(self):
        self.server.close()
