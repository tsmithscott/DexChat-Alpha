import socket

import pyaudio


class VoiceNetwork:
    def __init__(self, server, host=None, port=None):
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
        # self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.server.bind(("0.0.0.0", 25000))

        self.server = server

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
        while self.ALIVE:
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
        while self.ALIVE:
            voice = self.streamer_input.read(4096)

            for peer in self.peers:
                self.client.sendto(voice, (peer, self.peers.get(peer)))

    def play_voice(self):
        while self.ALIVE:
            for packet in self.voice_frames:
                self.streamer_output.write(packet)
                self.voice_frames.remove(packet)

    def die(self):
        self.ALIVE = False
