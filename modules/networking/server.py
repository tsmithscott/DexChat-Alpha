import sys
from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET
from threading import Thread
import urllib.request as req


I_HOST = "192.168.1.11"
E_HOST = req.urlopen("https://ifconfig.me/ip").read().decode("utf-8")
PORT = 25000
BUFFER = 2048
ADDRESS = (I_HOST, PORT)

peers = {}
addresses = {}

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(ADDRESS)


def incoming_connections():
    """Handle all incoming connections"""
    while True:
        peer, peer_address = server.accept()
        addresses[peer] = peer_address

        print(f"{peer_address[0]}: Connected.")

        for connected_peers in addresses:
            connected_peers.send(bytes(f"{addresses[peer][0]}: Connected", "utf8"))

        Thread(target=handle_peers, args=(peer,)).start()


def handle_peers(peer):
    """Takes a socket as argument and handles a single peer connection in a thread."""
    while True:
        peer_message = peer.recv(BUFFER)

        if peer_message.decode() != "{disconnect}\n":
            print(f"{addresses[peer][0]}: {peer_message.decode()}")

            for connected_peers in addresses:
                if connected_peers == peer:
                    pass
                else:
                    connected_peers.send(bytes(f"{addresses[peer][0]}: {peer_message.decode()}", "utf8"))
        else:
            peer.send(bytes("{ack_disconnect}", "utf8"))
            peer.close()

            for connected_peers in addresses:
                if connected_peers == peer:
                    pass
                else:
                    connected_peers.send(bytes(f"{addresses[peer][0]}: Disconnected.", "utf8"))

            print(f"{addresses[peer][0]}: Disconnected.")
            del addresses[peer]
            break


def send_message():
    """Use sys.stdin to send message to connected clients."""
    while True:
        server_message = sys.stdin.readline()

        for peer in addresses:
            peer.send(bytes(f"{E_HOST}: {server_message}", "utf8"))


if __name__ == '__main__':
    server.listen(5)
    print("Waiting for connections...")
    incoming_thread = Thread(target=incoming_connections)
    send_thread = Thread(target=send_message)
    incoming_thread.start()
    send_thread.start()
    incoming_thread.join()
    send_thread.join()
    server.close()
