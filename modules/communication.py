import socket
import sys
import threading
import multiprocessing
import json
import requests
import uuid

import pyaudio
import wave


class ChatNetwork:
    def __init__(self, host: str, port: int):
        """
        Initiates a server and client socket. Clients will connect to servers
        and servers will connect to clients.

        :param host:
        :param port:
        :return:
        """

        # Fetch public IP. This can be from any server. Used to communicate connections and disconnects.
        self.my_ip = requests.get("https://ifconfig.me/ip").text

        # Create ALIVE flag. server_accept will wait for this flag and gracefully close.
        self.ALIVE = True

        # Create a peer discovery filter and a peer connection storage for multiple, simultaneous connections.
        self.peers = {}
        self.peer_filter = {}

        # Assign socket attributes.
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("0.0.0.0", 25000))

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

                initiate = threading.Thread(target=self.server_receive, args=(connection, address), daemon=True)
                initiate.start()

    def server_receive(self, connection: socket.socket, address: tuple):
        """
        Threaded instance listening for imcoming messages and filtering based on packets.

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

                # Output incoming message.
                else:
                    sys.stdout.write(message.decode())
                    sys.stdout.flush()

            # Broken connection.
            except OSError:
                del self.peers[address]
                connection.close()
                sys.exit()

    def client_send(self):
        """
        Threaded instance takes user input and filters based on packet. Send globally to peers in current discovery.

        :return:
        """
        while True:
            # Take input from user.
            message = input("Message: ")

            # Filter message. If connection attempt, connected self.client to the provided parameters when initialised.
            if message == "/connect":
                try:
                    # Connect to provided paramters and add to global discovery.
                    self.client.connect((self.host, self.port))
                    self.peers[self.host] = self.client
                except ConnectionError as error:
                    print(error)

            # If disconnect request, attach public IP to packet and broadcast to current peer discovery.
            elif message == "/disconnect":
                try:
                    for address in self.peers:
                        self.peers.get(address).send((message + "+" + self.my_ip).encode())
                        self.peers.get(address).close()

                    # Reset ALIVE flag to disable server_receive thread.
                    self.ALIVE = False
                    sys.exit()
                except ConnectionError as error:
                    print(error)
            # Broadcast message to current peer discovery.
            else:
                for address in self.peers:
                    self.peers.get(address).send(message.encode())

    def dispatch_peers(self):
        """
        Runs when called, creates peer discovery packet and attaches header. Sends to all current peers.

        :return:
        """
        for address in self.peers:
            self.peers.get(address).send(("peer_filter+" + json.dumps(self.peer_filter)).encode())


class VoiceNetwork:
    def __init__(self):
        self.AUDIO_CHUNK = 1024
        self.AUDIO_FORMAT = pyaudio.paInt16
        self.AUDIO_CHANNELS = 2
        self.AUDIO_RATE = 44100
        self.AUDIO_FRAMES = []
        self.TEMP_OUT = f"crypt/temp/{uuid.uuid4().hex}.enco"

        self.audio_handler = pyaudio.PyAudio()
        self.stream_handler = None

        self.enco_wave = wave.open(self.TEMP_OUT, "wb")
        self.enco_wave.setnchannels(self.AUDIO_CHANNELS)
        self.enco_wave.setsamplewidth(self.audio_handler.get_sample_size(self.AUDIO_FORMAT))
        self.enco_wave.setframerate(self.AUDIO_RATE)

        self.streamer = multiprocessing.Process(target=self.stream)
        self.streamer.daemon = True
        self.streamer.start()

        self.recorder = multiprocessing.Process(target=self.record)
        self.recorder.daemon = True
        self.recorder.start()

    def stream(self):
        self.stream_handler = self.audio_handler.open(format=self.AUDIO_FORMAT,
                                                      channels=self.AUDIO_CHANNELS,
                                                      rate=self.AUDIO_RATE,
                                                      frames_per_buffer=self.AUDIO_CHUNK)

        print("AUDIO STREAMING STARTED!")

        while True:
            audio_stream = self.stream_handler.read(self.AUDIO_CHUNK)
            self.AUDIO_FRAMES.append(audio_stream)

    def record(self):
        while True:
            if self.AUDIO_FRAMES:
                self.enco_wave.write(b"" .join(self.AUDIO_FRAMES[0]))

    def close(self):
        self.streamer.terminate()
        self.recorder.terminate()
        self.enco_wave.close()
        del self.AUDIO_FRAMES

        self.stream_handler.stop_stream()
        self.stream_handler.close()
        self.audio_handler.terminate()

        sys.exit()
