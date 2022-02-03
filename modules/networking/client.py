import sys
import socket
from threading import Thread


def die():
    quit()


def receive():
    """Handles incoming messages"""
    while True:
        try:
            server_message = peer_socket.recv(BUFFER).decode("utf8").strip()

            if server_message == "{ack_disconnect}":
                print("[Disconnected]")
                quit()
            else:
                print(f"{server_message}")
        except OSError as error:
            print(error)
            break


def send():
    """Use sys.stdin and send message"""
    while True:
        peer_message = sys.stdin.readline().strip()

        if peer_message == "{disconnect}":
            peer_socket.send(bytes(peer_message, "utf8"))
            quit()
        else:
            peer_socket.send(bytes(peer_message, "utf8"))


if __name__ == "__main__":
    SERVER_HOST = socket.gethostbyname(socket.gethostname())
    SERVER_PORT = 25000
    BUFFER = 2048
    ADDRESS = (SERVER_HOST, SERVER_PORT)

    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    peer_socket.connect(ADDRESS)

    receive_thread = Thread(target=receive)
    send_thread = Thread(target=send)
    receive_thread.start()
    send_thread.start()
    receive_thread.join()
    send_thread.join()
