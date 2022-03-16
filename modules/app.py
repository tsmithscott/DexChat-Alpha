import sys
from tkinter import Tk, BooleanVar

from modules.frames.startframe import StartFrame
from modules.frames.connectframe import ConnectFrame
from modules.frames.hostframe import HostFrame
from modules.frames.dexframe import DexFrame

from modules.encryption.crypto import Crypto


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("DexChat")
        self.root.geometry("275x115")
        self.root.resizable(False, False)
        self.root.call("source", "static/themes/azure.tcl")
        self.root.call("set_theme", "dark")

        self.VOICE_ENABLED = BooleanVar(self.root)
        self.CHAT_CONTROLLER = None
        self.VOICE_PEER_OBJECTS = []
        self.CRYPTO_CONTROLLER = Crypto()
        self.NICKS = {}
        self.KEYS = {}

        self.start_frame = StartFrame(self, self.root, width=275, height=115)
        self.connect_frame = None
        self.host_frame = None
        self.dex_frame = None

        self.start_frame.place(x=0, y=0)

    def open_connect_frame(self):
        self.start_frame.destroy()
        self.resize_root(250, 325)

        self.connect_frame = ConnectFrame(self, self.root, width=250, height=325)
        self.connect_frame.place(x=0, y=0)

    def open_host_frame(self):
        self.start_frame.destroy()
        self.resize_root(250, 230)

        self.host_frame = HostFrame(self, self.root, width=250, height=230)
        self.host_frame.place(x=0, y=0)

    def open_dex_frame(self):
        if self.host_frame:
            self.host_frame.destroy()
        else:
            self.connect_frame.destroy()

        self.resize_root(550, 685)

        self.dex_frame = DexFrame(self, self.root, width=550, height=685)
        self.dex_frame.place(x=0, y=0)

    def resize_root(self, width, height):
        self.root.geometry(f"{width}x{height}")

    def disconnect(self):
        self.dex_frame.disable_voice()
        self.CHAT_CONTROLLER.client_send("/disconnect")
        sys.exit()

    def cancel(self):
        self.resize_root(275, 115)
        self.connect_frame.destroy()
        self.start_frame = StartFrame(self, self.root, width=275, height=115)
        self.start_frame.place(x=0, y=0)

    def cancel_host(self):
        self.resize_root(275, 115)
        self.host_frame.destroy()
        self.start_frame = StartFrame(self, self.root, width=275, height=115)
        self.start_frame.place(x=0, y=0)

    def run(self):
        self.root.mainloop()
