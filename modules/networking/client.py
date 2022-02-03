import sys
from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET
from threading import Thread


def receive():
    """Handles incoming messages"""
    while True:
        try:
            server_message = peer_socket.recv(BUFFER).decode("utf8")

            if server_message == "{ack_disconnect}":
                print("[Disconnected]")
                break

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
            break
        else:
            peer_socket.send(bytes(peer_message, "utf8"))


if __name__ == "__main__":

    while True:
        sys.stdout.write("Enter server address (IP:Port): ")
        address_input = sys.stdin.readline().split(":")

        SERVER_HOST = address_input[0]
        SERVER_PORT = int(address_input[1])
        BUFFER = 2048
        ADDRESS = (SERVER_HOST, SERVER_PORT)

        peer_socket = socket(AF_INET, SOCK_STREAM)
        peer_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        peer_socket.connect(ADDRESS)

        receive_thread = Thread(target=receive)
        send_thread = Thread(target=send)
        receive_thread.start()
        send_thread.start()
        receive_thread.join()
        send_thread.join()

        restart = True
        while True:
            sys.stdout.write("Run again? (Y/n) ")
            restart = sys.stdin.readline().strip().lower()
            if restart == 'y':
                break
            elif restart == 'n':
                quit()

