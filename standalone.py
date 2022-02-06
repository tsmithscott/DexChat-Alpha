import time
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SOCK_STREAM
from threading import Thread
import tkinter

CONTACTS = {}
PEERS = []

KEEP_ALIVE = True

self_socket = socket(AF_INET, SOCK_STREAM)
self_socket.bind(("127.0.0.1", 25000))
# self_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

peer_socket = None


class Server:
    def __init__(self, client_string, message_view):
        self.client_string = client_string
        self.message_view = message_view

    def wait(self):
        while KEEP_ALIVE:
            peer_instance, peer_address = self_socket.accept()

            CONTACTS[peer_instance] = peer_address
            PEERS.append(peer_instance)

            Thread(target=self.sole_peer, args=(peer_instance,))

    def sole_peer(self, peer_instance):
        while KEEP_ALIVE:
            message = peer_instance.recv(2048).decode().strip()

            if message == "{disconnect}":
                for peers in PEERS:
                    if peers == peer_instance:
                        PEERS.pop(PEERS.index(peer_instance))
                        del CONTACTS[peer_instance]
                        peer_instance.close()
                break
            else:
                print(message)
                self.message_view.insert(tkinter.END, f"{CONTACTS[peer_instance][0]}: {message}")

    def send(self, event=None):
        message = self.client_string.get()

        if message == "{disconnect}":
            for peers in PEERS:
                peers.send(message.encode())

            global KEEP_ALIVE
            KEEP_ALIVE = False
        else:
            for peers in PEERS:
                print(message)
                peers.send(message.encode())

    def connect(self, address, port):
        self_socket.connect((address, port))

        CONTACTS[peer_socket] = (address, port)
        PEERS.append(peer_socket)


def placeholder(event=None):
    client_message.set("")


root = tkinter.Tk()
root.title("DexChat")

messages_frame = tkinter.Frame(root)

client_message = tkinter.StringVar()
client_message.set("Type your message here.")

scrollbar = tkinter.Scrollbar(messages_frame)

message_view = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)

server = Server(client_message, message_view)
time.sleep(3)
server.connect("82.0.10.30", 25000)

scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
message_view.place(x=7, y=25, anchor=tkinter.CENTER)
message_view.pack()
messages_frame.pack()

entry_field = tkinter.Entry(root, textvariable=client_message)
entry_field.bind("<Return>", server.send)
entry_field.bind("<Button-1>", placeholder)
entry_field.pack()
send_button = tkinter.Button(root, text="Send", command=server.send)
send_button.pack()

self_socket.listen(5)

incoming = Thread(target=server.wait)
incoming.start()
# incoming.join()

tkinter.mainloop()

# if __name__ == '__main__':
#     self_socket.listen(5)
#     incoming = Thread(target=wait)
#     incoming.start()
#     incoming.join()
#     self_socket.close()
