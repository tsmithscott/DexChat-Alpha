import threading
import socket
from sys import platform
from tkinter import ttk, Listbox, END, Label

from modules.network.voicenetwork import VoiceNetwork


class DexFrame(ttk.Frame):
    def __init__(self, controller, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.server = None
        self.controller = controller

        self.parent.protocol("WM_DELETE_WINDOW", self.controller.disconnect)
        self.parent.unbind("<Return>")

        button_frame = ttk.Frame(self, width=550, height=80)
        self.voice_button = ttk.Button(button_frame, text="Enable Voice", width=10, command=self.enable_voice)
        self.theme_button = ttk.Button(button_frame, text="Light Mode", width=10, command=self.change_theme)
        disconnect_button = ttk.Button(button_frame, text="Disconnect", width=10, style="Accent.TButton",
                                       command=self.controller.disconnect)

        button_frame.place(x=0, y=0, anchor="nw")
        self.voice_button.place(x=525, y=22, anchor="ne", width=150, height=40)
        self.theme_button.place(x=25, y=22, anchor="nw", width=150, height=40)
        disconnect_button.place(x=275, y=22, anchor="n", width=120, height=40)

        chat_frame = ttk.Frame(self, width=550, height=363)
        chat_labelframe = ttk.LabelFrame(chat_frame, text="Chat", labelanchor="n", width=500, height=353)

        status_frame = ttk.Frame(self, width=550, height=250)
        chat_peer_labelframe = ttk.LabelFrame(status_frame, width=230, height=175, text="Connected Peers: Chat",
                                              labelanchor="n")
        voice_peer_labelframe = ttk.LabelFrame(status_frame, width=230, height=175, text="Connected Peers: Voice",
                                               labelanchor="n")

        if platform == "win32":
            self.status_box = Listbox(chat_frame, width=68, height=4, bd=0)
            self.chat_box = Listbox(chat_frame, width=68, height=11, bd=0)

            self.chat_box.place(x=35, y=90, anchor="nw")

            self.connected_chat = Listbox(chat_peer_labelframe, width=28, height=8, bd=0)
            self.connected_voice = Listbox(voice_peer_labelframe, width=28, height=8, bd=0)
        elif platform == "darwin":
            self.status_box = Listbox(chat_frame, width=68, height=4, bd=0)
            self.chat_box = Listbox(chat_frame, width=68, height=16, bd=0)

            self.chat_box.place(x=35, y=71, anchor="nw")

            self.connected_chat = Listbox(chat_peer_labelframe, width=28, height=11, bd=0)
            self.connected_voice = Listbox(voice_peer_labelframe, width=28, height=11, bd=0)
        elif platform == "linux":
            self.status_box = Listbox(chat_frame, width=53, height=4, bd=0)
            self.chat_box = Listbox(chat_frame, width=53, height=11, bd=0)

            self.chat_box.place(x=35, y=90, anchor="nw")

            self.connected_chat = Listbox(chat_peer_labelframe, width=22, height=7, bd=0)
            self.connected_voice = Listbox(voice_peer_labelframe, width=22, height=7, bd=0)

        self.message_entry = ttk.Entry(chat_frame, width=10)
        self.message_entry.bind("<Return>", self.send_message)

        chat_frame.place(x=0, y=80, anchor="nw")
        chat_labelframe.place(x=25, y=0, anchor="nw")
        self.status_box.place(x=35, y=20, anchor="nw")

        self.message_entry.place(x=40, y=297, anchor="nw", width=470, height=40)

        status_frame.place(x=0, y=443, anchor="nw")
        chat_peer_labelframe.place(x=25, y=10, anchor="nw")
        voice_peer_labelframe.place(x=525, y=10, anchor="ne")
        self.connected_chat.place(x=12, y=5, anchor="nw")
        self.connected_voice.place(x=12, y=5, anchor="nw")

        self.status_box.insert(END, "System (INFO): Running on 0.0.0.0")
        self.status_box.insert(END, "System (INFO): Encryption Enabled.")
        self.status_box.insert(END, "System (INFO): Voice Disabled.")

        if platform == "win32" or platform == "linux":
            self.status_box.insert(END,
                                   "-----------------------------------------------------------------------------------------------")
        elif platform == "darwin":
            self.status_box.insert(END,
                                   "--------------------------------------------------------------------------------------------------")

        self.status_box.itemconfig(0, {"fg": "green"})
        self.status_box.itemconfig(1, {"fg": "green"})
        self.status_box.itemconfig(2, {"fg": "red"})

        self.connected_chat.insert(END, "System: Connected")

        self.connected_chat.itemconfig(0, {"fg": "green"})

        quote_label = Label(self, text="Simplicity, carried to the extreme, becomes elegance.",
                            font=("Courier", 11, "italic"), justify="center")
        quote_label.place(x=275, y=655, anchor="center")

    def change_theme(self):
        if self.parent.call("ttk::style", "theme", "use") == "azure-dark":
            self.parent.call("set_theme", "light")
            self.theme_button.configure(text="Dark Mode")
        else:
            self.parent.call("set_theme", "dark")
            self.theme_button.configure(text="Light Mode")

    def enable_voice(self):
        self.status_box.delete(2)
        self.connected_voice.insert(END, "System: Connected")
        self.connected_voice.itemconfig(0, {"fg": "green"})

        current_chat_peers = self.controller.CHAT_CONTROLLER.get_peers()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("0.0.0.0", 25000))

        for peer in current_chat_peers:
            voice_object = VoiceNetwork(self.controller, self.server, peer, current_chat_peers.get(peer))

            self.controller.VOICE_PEER_OBJECTS.append(voice_object)

            threading.Thread(target=voice_object.server_receive).start()
            threading.Thread(target=voice_object.client_send).start()
            threading.Thread(target=voice_object.play_voice).start()

            if peer in self.controller.NICKS:
                self.connected_voice.insert(END, f"{self.controller.NICKS.get(peer)} ({peer})")
                self.connected_voice.itemconfig(0, {"fg": "green"})

        self.status_box.insert(2, "System (INFO): Voice Enabled.")
        self.status_box.itemconfig(2, {"fg": "green"})

        self.voice_button.configure(text="Disable Voice", command=self.disable_voice)
        self.controller.VOICE_ENABLED = True

    def disable_voice(self):
        self.status_box.delete(2)

        for voice_objects in self.controller.VOICE_PEER_OBJECTS:
            voice_objects.die()
            self.controller.VOICE_PEER_OBJECTS.remove(voice_objects)
            del voice_objects

        self.server.close()

        self.status_box.insert(2, "System (INFO): Voice Disabled")
        self.status_box.itemconfig(2, {"fg": "red"})

        self.connected_voice.delete(0, END)

        self.voice_button.configure(text="Enable Voice", command=self.enable_voice)
        self.controller.VOICE_ENABLED = False

    def send_message(self, event):
        message = self.message_entry.get()

        self.chat_box.yview(END)
        self.message_entry.delete(0, END)
        self.controller.CHAT_CONTROLLER.client_send(message)
