import socket
import threading


class ServerNode:
    def __init__(self):
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.node.bind(("0.0.0.0", 25000))
        self.node.listen(5)
        self.connection, address = self.node.accept()

    def send_message(self, message):
        self.connection.send(message.encode())

    def receive_message(self):
        while True:
            message = self.connection.recv(1024).decode()
            print(message)

    def main(self):
        while True:
            message = input("Me: ")
            self.send_message(message)


server = ServerNode()
enable_read = threading.Thread(target=server.receive_message)
enable_read.daemon = True
enable_read.start()
server.main()
