from modules.networking.server import node_server
from modules.networking.client import node_client


class Node:
    def __init__(self):
        self.server = None
        self.client = None
        self.peers = set()
        self.keys = {}

    # def get_peers(self):
    #     return self.peers
    #
    # def get_keys(self):
    #     return self.keys

    def create_server_instance(self):
        self.server = node_server.NodeServer(self)

    def create_client_instance(self, host, port):
        self.client = node_client.NodeClient(host, port, self)

    def purge_server_instance(self):
        self.server = None

    def purge_client_instance(self):
        self.client = None

    def add_peer(self, connection):
        self.peers.add(connection)

    def add_key(self, address, peer_key):
        self.keys[address] = peer_key

    def remove_peer(self, connection):
        for p in self.peers:
            if p == connection:
                self.peers.remove(connection)

    def remove_key(self, address):
        self.keys.pop(address)
