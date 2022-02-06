import sys
import socket
import select


HOST = "localhost"
PORT = 25000
BUFFER = 4096


def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2)

    # Connect to remote host
    try:
        client_socket.connect((HOST, PORT))
    except:
        print("Cannot connect to server.")
        sys.exit()

    print("Connected to remote host. You can start sending messages!")
    sys.stdout.write("[Me] ")
    sys.stdout.flush()

    while True:
        socket_list = [sys.stdin, client_socket]

        # Get readable sockets from list.
        rtr, rtw, ie = select.select(socket_list, [], [])

        for sock in rtr:
            if sock == client_socket:
                # Incoming broadcast from remote server.
                data = sock.recv(BUFFER)

                if not data:
                    print("\nDisconnected from the remote host(s)")
                    sys.exit()
                else:
                    # print data
                    sys.stdout.write(data)
                    sys.stdout.write("[Me] ")
                    sys.stdout.flush()
            else:
                # User message
                message = sys.stdin.readline()
                client_socket.send(message)

                sys.stdout.write("[Me] ")
                sys.stdout.flush()


if __name__ == '__main__':
    sys.exit(client())
