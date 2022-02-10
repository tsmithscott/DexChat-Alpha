import socket
import select
import sys

HOST = "localhost"
PORT = 25000
BUFFER = 4096
SOCKET_LIST = []


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    # Add socket object to readable connections (list)
    SOCKET_LIST.append(server_socket)

    print(f"Chat server started on {socket.gethostname}:{PORT}")

    while True:
        # Get list of sockets which are ready to be read through using select.
        # timeout = 0        poll and never block
        rtr, rtw, ie = select.select(SOCKET_LIST, [], [], 0)

        for sock in rtr:
            # A new connection request has been received.
            if sock == server_socket:
                sock_obj, addr = server_socket.accept()
                SOCKET_LIST.append(sock_obj)

                print(f"[Client {addr[0]}:{addr[1]} connected]")

                broadcast(server_socket, sock_obj, f"[SERVER] Client {addr[0]}:{addr[1]} joined the chat\n")
            else:
                # Message from an existing client, not a new connection.
                try:
                    data = sock.recv(BUFFER)
                    name = sock.getpeername()

                    if data:
                        broadcast(server_socket, sock, f"[{name}] {data.decode()}")
                    else:
                        # Broken connection.
                        if sock in SOCKET_LIST:

                            SOCKET_LIST.remove(sock)

                        broadcast(server_socket, sock, f"[SERVER] Client {name} disconnected!")
                except RuntimeError:
                    continue


def broadcast(server_socket, sock_obj, message):
    for sock in SOCKET_LIST:
        # Send message to peers.
        if sock != server_socket and sock != sock_obj:
            try:
                sock.send(message.encode())
            except RuntimeError:
                # Selected socket is broken.
                sock.close()

                if sock in SOCKET_LIST:
                    SOCKET_LIST.remove(sock)


if __name__ == '__main__':
    sys.exit(server())
