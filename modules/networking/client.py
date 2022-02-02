import sys
import time
from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET
from threading import Thread


def die():
    quit()


def receive():
    """Handles incoming messages"""
    while True:
        try:
            server_message = peer_socket.recv(BUFFER).decode("utf8")

            if server_message == "{ack_disconnect}":
                print(server_message)
                global DEAD
                DEAD = True
                quit()

            else:
                print(f"{server_message}")
        except OSError as error:
            print(error)
            break


def send():
    """Use sys.stdin and send message"""
    while True:
        peer_message = sys.stdin.readline()

        if peer_message == "{disconnect}\n":
            peer_socket.send(bytes(peer_message, "utf8"))
            quit()
        else:
            peer_socket.send(bytes(peer_message, "utf8"))


SERVER_HOST = "82.0.10.30"
SERVER_PORT = 25000
BUFFER = 2048
ADDRESS = (SERVER_HOST, SERVER_PORT)

peer_socket = socket(AF_INET, SOCK_STREAM)
peer_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
peer_socket.connect(ADDRESS)

DEAD = False

receive_thread = Thread(target=receive)
send_thread = Thread(target=send)
receive_thread.start()
send_thread.start()
receive_thread.join()
send_thread.join()
