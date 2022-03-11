import socket
import sys
import threading
import json
import datetime

from tkinter import END

import pyaudio


class ChatNetwork:
    def __init__(self, controller, port: int = 25000, nick: str = None):
        """
        Initiates a server and client socket. Clients will connect to servers
        and servers will connect to clients.
        """

        self.controller = controller

        # Fetch public IP. This can be from any server. Used to communicate connections and disconnects.
        self.my_ip = '100.67.164.33'  # TODO: REMOVE THIS AND CHANGE BACK TO IFCONFIG.ME IP
        self.my_nick = nick

        # Create ALIVE flag. server_accept will wait for this flag and gracefully close.
        self.ALIVE = True

        # Create a peer discovery filter and a peer connection storage for multiple, simultaneous connections.
        self.peers = {}
        self.peer_filter = {}
        self.nicks = {}

        # Assign socket attributes.
        # self.host = host
        # self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("0.0.0.0", port))

        # Listen for a maximum of 100 connections.
        self.server.listen(100)

        # Create a client socket to connect to other servers.
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def server_accept(self):
        """
        Accepts connections on listening server socket. Updates current peer discovery dictionary for later JSON encoding.

        :return:
        """

        # Always listen for connection. Stop when exiting.
        while True:
            # Check if program is exiting.
            if not self.ALIVE:
                sys.exit()

            # Accept incoming connections. Store an instance of the connection socket and a tuple of the connection details.
            connection, address = self.server.accept()

            # If a connection with this peer's server already exists (user may have connected first), create a thread to receive messages.
            # Threads are Daemon to prevent blocking.
            if address[0] in self.peers.keys():
                self.client_send("/nickname")
                initiate = threading.Thread(target=self.server_receive, args=(connection, address), daemon=True)
                initiate.start()

            # If connection doesn't exists, create a new instance of a connection with the peer's server.
            else:
                new_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                new_client.connect((address[0], 25000))

                # Add the new connection to a global peer discovery.
                self.peers[address[0]] = new_client
                self.peer_filter[address[0]] = 25000

                # Broadcast a peer discovery.
                self.dispatch_peers()
                self.client_send("/nickname")

                initiate = threading.Thread(target=self.server_receive, args=(connection, address), daemon=True)
                initiate.start()

    def server_receive(self, connection: socket.socket, address: tuple):
        """
        Threaded instance listening for incoming messages and filtering based on packets.

        :param connection:
        :param address:
        :return:
        """
        while True:
            try:
                # Accept an incoming message. Buffer can be changed.
                message = connection.recv(4096)

                # If a message is a disconnect request.
                if "/disconnect" in message.decode():
                    # Separate request header and public IP.
                    remote_ip = message.decode().split("+")[1]

                    # If public IP of peer is pending peer discovery, remove.
                    if remote_ip in self.peer_filter:
                        del self.peer_filter[remote_ip]

                    # Remove peer from current connections.
                    del self.peers[remote_ip]
                    connected_ip = self.controller.dex_frame.connected_chat.get(0, END).index(
                        f"{self.nicks[remote_ip]} ({remote_ip})")
                    del self.nicks[remote_ip]
                    self.controller.dex_frame.connected_chat.delete(connected_ip)
                    connection.close()
                    sys.exit()

                # If message is an incoming peer discovery.
                elif "peer_filter" in message.decode():
                    # Separate packet header and discovery data.
                    peer_filter = message.decode().split("+")[1]
                    peer_filter = json.loads(peer_filter)

                    # Filter through peer discovery json. If current peer is not in global discovery, connect and add.
                    for address in peer_filter:
                        if address not in self.peers and not address == self.my_ip:
                            new_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            new_client.connect((address, peer_filter.get(address)))
                            self.peers[address] = new_client

                elif "/nickname" in message.decode():
                    nickname = message.decode().split("+")[1]
                    ip = connection.getpeername()[0]
                    self.nicks[ip] = nickname

                    if nickname != "None":
                        self.controller.dex_frame.connected_chat.insert(END, f"{nickname} ({ip})")
                    else:
                        self.controller.dex_frame.connected_chat.insert(END, f"{ip}")

                # Output incoming message.
                else:
                    self.controller.dex_frame.chat_box.insert(END, f"{message.decode()}")
                    self.controller.dex_frame.chat_box.yview(END)

            # Broken connection.
            except OSError:
                del self.peers[address]
                connection.close()
                sys.exit()

    def client_send(self, message):
        """
        Threaded instance takes user input and filters based on packet. Send globally to peers in current discovery.

        :return:
        """

        # If disconnect request, attach public IP to packet and broadcast to current peer discovery.
        if message == "/disconnect":
            try:
                for address in self.peers:
                    self.peers.get(address).send((message + "+" + self.my_ip).encode())
                    self.peers.get(address).close()

                # Reset ALIVE flag to disable server_receive thread.
                self.ALIVE = False
                sys.exit()
            except ConnectionError as error:
                print(error)
        elif message == "/nickname":
            for address in self.peers:
                self.peers.get(address).send(f"/nickname+{self.my_nick}".encode())
        # Broadcast message to current peer discovery.
        else:
            for address in self.peers:
                self.controller.dex_frame.chat_box.insert(END,
                                                          f"{datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')} [Me]: {message}")

                if self.my_nick is None:
                    self.peers.get(address).send(
                        f"{datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')} [{self.my_ip}]: {message}".encode())
                else:
                    self.peers.get(address).send(
                        f"{datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')} [{self.my_nick}]: {message}".encode())

    def dispatch_peers(self):
        """
        Runs when called, creates peer discovery packet and attaches header. Sends to all current peers.

        :return:
        """
        for address in self.peers:
            self.peers.get(address).send(("peer_filter+" + json.dumps(self.peer_filter)).encode())

    def connect(self, host, port):
        try:
            # Connect to provided parameters and add to global discovery.
            self.client.connect((host, port))
            self.peers[host] = self.client

            # voice_object = VoiceNetwork(host, 26000)
            # threading.Thread(target=voice_object.server_receive, daemon=True).start()
            # threading.Thread(target=voice_object.client_send).start()

        except ConnectionError as error:
            print(error)

    def set_nick(self, nickname):
        self.my_nick = nickname


class VoiceNetwork:
    def __init__(self, host=None, port=None):
        # Fetch public IP. This can be from any server. Used to communicate connections and disconnects.
        # self.my_ip = requests.get("https://ifconfig.me/ip").text

        # Create ALIVE flag. server_accept will wait for this flag and gracefully close.
        self.ALIVE = True

        # Create a peer discovery filter and a peer connection storage for multiple, simultaneous connections.
        self.peers = {}
        self.peer_filter = {}

        # Assign socket attributes.
        self.host = host
        self.port = port

        # Create a server socket to receive voice packets from other clients.
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("0.0.0.0", 25000))

        # Create a client socket to send voice packets to other servers.
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Create voice system.
        self.stream_handler = pyaudio.PyAudio()

        self.streamer_output = self.stream_handler.open(format=pyaudio.paInt16,
                                                        channels=1,
                                                        rate=44100,
                                                        output=True)

        self.streamer_input = self.stream_handler.open(format=pyaudio.paInt16,
                                                       channels=1,
                                                       rate=44100,
                                                       input=True,
                                                       frames_per_buffer=4096)

        # Create voice data system.
        self.voice_frames = []

        # Activate initial connection
        self.peers[self.host] = 25000

    def server_receive(self):
        """
        Threaded instance listening for incoming messages and filtering based on packets.

        :return:
        """
        while True:
            try:
                # Accept an incoming message. Buffer can be changed.
                datagram = self.server.recvfrom(8192)
                voice = datagram[0]
                address = datagram[1]

                if address[0] not in self.peers:
                    self.peers[address[0]] = address[1]

                if voice != '':
                    self.voice_frames.append(voice)
            # Broken connection.
            except OSError as error:
                print(error)

    def client_send(self):
        """
        Threaded instance takes user input and filters based on packet. Send globally to peers in current discovery.

        :return:
        """
        while True:
            voice = self.streamer_input.read(4096)

            for peer in self.peers:
                self.client.sendto(voice, (peer, self.peers.get(peer)))

    def play_voice(self):
        while True:
            for packet in self.voice_frames:
                self.streamer_output.write(packet)
                self.voice_frames.pop(self.voice_frames.index(packet))

    def dispatch_peers(self):
        """
        Runs when called, creates peer discovery packet and attaches header. Sends to all current peers.

        :return:
        """
        pass
