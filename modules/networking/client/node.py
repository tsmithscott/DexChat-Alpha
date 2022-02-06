import socket
import threading


class ClientNode:
    def __init__(self):
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host = input("Please enter host IP: ")
        port = int(input("Please enter host port: "))

        self.node.connect((host, port))

    def send_message(self, message):
        self.node.send(message.encode())

    def receive_message(self):
        while True:
            message = self.node.recv(1024).decode()
            print(message)

    def main(self):
        while True:
            message = input("Me: ")
            self.send_message(message)


client = ClientNode()
enable_read = threading.Thread(target=client.receive_message)
enable_read.daemon = True
enable_read.start()
client.main()