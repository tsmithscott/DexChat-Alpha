import requests

from modules.networking.server import node_server
from modules.networking.client import node_client


class Node:
    def __init__(self):
        self.s_node = node_server.NodeServer(self)
        self.c_node = node_client.NodeClient(self)
        self.peers = set()
        self.keys = {}
        self.host = requests.get("https://api.ipify.org").text

    def get_peer(self, peer):
        for p in peer:
            if p == peer:
                return peer[p]

    # def get_keys(self):
    #     return self.keys

    def purge_server_instance(self):
        self.s_node = None

    def purge_client_instance(self):
        self.c_node = None

    def add_peer(self, peer):
        self.peers.add(peer)

    def add_key(self, address, peer_key):
        self.keys[address] = peer_key

    def remove_peer(self, peer):
        for p in self.peers:
            if p == peer:
                self.peers.remove(peer)

    def remove_key(self, address):
        self.keys.pop(address)
