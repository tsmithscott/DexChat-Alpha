import sys
from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET
from threading import Thread


HOST = "192.168.1.11"
PORT = 25000
BUFFER = 2048
ADDRESS = (HOST, PORT)

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

        Thread(target=handle_peers, args=(peer,)).start()


def handle_peers(peer):
    """Takes a socket as argument and handles a single peer connection in a thread."""
    while True:
        peer_message = peer.recv(BUFFER)

        if peer_message.decode() != "{disconnect}\n":
            print(f"{addresses[peer][0]}: {peer_message.decode()}")
        else:
            peer.send(bytes("{ack_disconnect}", "utf8"))
            peer.close()
            print(f"{addresses[peer]}: Disconnected.")
            del addresses[peer]
            break


def send_message():
    """Use sys.stdin to send message to connected clients."""
    while True:
        server_message = sys.stdin.readline()

        for peer in addresses:
            peer.send(bytes(f"{HOST}: {server_message}", "utf8"))


if __name__ == '__main__':
    server.listen(1)
    print("Waiting for connections...")
    incoming_thread = Thread(target=incoming_connections)
    send_thread = Thread(target=send_message)
    incoming_thread.start()
    send_thread.start()
    incoming_thread.join()
    send_thread.join()
    server.close()
