import socket
import threading


class Client:
    def __init__(self):
        self.PEERS = []

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.bind(("0.0.0.0", 25000))

        send_thread = threading.Thread(target=self.send)
        receive_thread = threading.Thread(target=self.receive)

        send_thread.daemon = True
        receive_thread.daemon = True

        send_thread.run()
        receive_thread.run()

        self.client.listen()

    def send(self):
        while True:
            message = input("Message: ")

            self.client.send(message.encode())

    def receive(self):
        while True:
            peer_socket, peer_address = self.client.accept()

            self.PEERS.append((peer_socket, peer_address))

            peer_thread = threading.Thread(target=self.handle, args=(peer_socket,))
            peer_thread.daemon = True
            peer_thread.start()

    def handle(self, peer_socket):
        while True:
            try:
                message = peer_socket.recv(4096)

                if message:
                    for peer in self.PEERS:
                        if peer[0] == peer_socket:
                            address = peer[1][0]

                            print(f"[{address}]: {message.decode()}")
                else:
                    for peer in self.PEERS:
                        if peer[0] == peer_socket:
                            self.PEERS.remove(self.PEERS.index(peer))

                            peer_socket.close()
                            break
            except RuntimeError as error:
                print(error)
