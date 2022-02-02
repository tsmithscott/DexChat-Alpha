import socket
import select
import sys


class Client:
    def __init__(self, ip_addr: str, port: int):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip_addr, port))

    def send_message(self):
        socket_list = [sys.stdin, self.server]

        read_sockets, write_socket, error_socket = select.select(socket_list, [], [])

        for socks in socket_list:
            if socks == self.server:
                message = socks.recv(2048)
                print(message)
            else:
                message = sys.stdin.readline()
                self.server.send(message.encode())
                sys.stdin.flush()

    def receive_message(self):
        pass

    def send_audio(self):
        pass

    def receive_audio(self):
        pass

