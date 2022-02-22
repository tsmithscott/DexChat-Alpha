import socket
import sys
import threading
import json
import requests


class Network:
    def __init__(self, host, port):
        self.ALIVE = True
        self.peers = {}
        self.peer_filter = {}
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("0.0.0.0", 25000))
        self.server.listen(5)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.my_ip = requests.get("https://ifconfig.me/ip").text

    def server_accept(self):
        while self.ALIVE:
            connection, address = self.server.accept()

            if address[0] in self.peers.keys():
                initiate = threading.Thread(target=self.server_receive, args=(connection, address), daemon=True)
                initiate.start()
            else:
                new_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                new_client.connect((address[0], 25000))
                self.peers[address[0]] = new_client
                self.peer_filter[address[0]] = 25000

                self.dispatch_peers()

                initiate = threading.Thread(target=self.server_receive, args=(connection, address), daemon=True)
                initiate.start()

    def server_receive(self, connection, address):
        while True:
            try:
                message = connection.recv(4096)

                if message.decode() == "/disconnect":
                    del self.peers[address[0]]
                    connection.close()
                    sys.exit()
                elif "peer_filter" in message.decode():
                    peer_filter = message.decode().split("+")[1]
                    peer_filter = json.loads(peer_filter)

                    for address in peer_filter:
                        if address not in self.peers and not address == self.my_ip:
                            new_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            new_client.connect((address, peer_filter.get(address)))
                            self.peers[address] = new_client
                else:
                    sys.stdout.write(message.decode())
                    sys.stdout.flush()
            except OSError:
                del self.peers[address]
                connection.close()
                sys.exit()

    def client_send(self):
        while True:
            message = input("Message: ")

            if message == "/connect":
                try:
                    self.client.connect((self.host, self.port))
                    self.peers[self.host] = self.client
                except ConnectionError as error:
                    print(error)
            elif message == "/disconnect":
                try:
                    for address in self.peers:
                        self.peers.get(address).send(message.encode())
                        self.peers.get(address).close()
                    # self.client.send(message.encode())
                    # self.client.close()
                    self.ALIVE = False
                    sys.exit()
                except ConnectionError as error:
                    print(error)
            else:
                for address in self.peers:
                    self.peers.get(address).send(message.encode())

    def dispatch_peers(self):
        for address in self.peers:
            self.peers.get(address).send(("peer_filter+" + json.dumps(self.peer_filter)).encode())
