import socket


class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("0.0.0.0", 25000))
        self.server.listen(5)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def server_accept(self):
        while True:
            connection, address = self.server.accept()

            self.server_receive(connection)

    def server_receive(self, connection):
        while True:
            message = connection.recv(4096)

            if message:
                print(message.decode())
            else:
                connection.close()

    def client_send(self):
        while True:
            message = input("Message: ")

            if message == "/connect":
                try:
                    self.client.connect((self.host, self.port))
                except ConnectionError as error:
                    print(error)
            elif message == "/disconnect":
                try:
                    self.client.close()
                except ConnectionError as error:
                    print(error)
            else:
                self.client.send(message.encode())
