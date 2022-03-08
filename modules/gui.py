import threading
from sys import platform

from tkinter import Tk, Listbox, END, BooleanVar, messagebox
from tkinter import ttk
import requests

from modules.communication2 import ChatNetwork


class GUI:
    def __init__(self):
        # CREATE EXECUTABLE

        # ROOT WINDOW
        self.root = Tk()
        self.root.title("DexChat")
        self.root.geometry("275x115")
        self.root.resizable(False, False)
        self.root.call("source", "../static/themes/azure.tcl")
        self.root.call("set_theme", "dark")

        # DEXCHAT CONFIG
        self.IP = None
        self.PORT = None
        self.NICK = None
        self.VOICE_ENABLED = BooleanVar(self.root)

        # GLOBAL FLAGS
        self.chat = None
        self.voice = None
        self.my_ip = requests.get("https://ifconfig.me/ip").text
        self.style = ttk.Style()
        self.RESTART = False

        # START FRAME FOR HOST/CONNECT OPTIONS
        self.start_frame = ttk.Frame(self.root, width=275, height=115)
        self.start_frame.place(x=0, y=0)

        # START FRAME CONFIG
        self.connect_button = ttk.Button(self.start_frame, text="Connect to DexChat", command=lambda: self.display_menu(connect=True), style="Accent.TButton")
        self.host_button = ttk.Button(self.start_frame, text="Host DexChat", command=lambda: self.display_menu(host=True))

        self.connect_button.place(x=137, y=20, anchor="n")
        self.host_button.place(x=137, y=65, anchor="n")

        # MENU FRAME FOR CONNECTING
        self.menu_frame = ttk.Frame(self.root, width=250, height=325)

        # MENU FRAME CONFIG
        self.config_frame = ttk.Frame(self.menu_frame, width=250, height=325)
        self.ip_entry = ttk.Entry(self.config_frame, width=10, justify="center")
        self.port_entry = ttk.Entry(self.config_frame, width=10, justify="center")
        self.nickname_entry = ttk.Entry(self.config_frame, width=10, justify="center")
        self.voice_check = ttk.Checkbutton(self.config_frame, text="Enable DexVoice", variable=self.VOICE_ENABLED)
        self.start_button = ttk.Button(self.menu_frame, text="Connect", width=10, command=self.connect_dex, style="Accent.TButton")

        self.add_placeholder(self.ip_entry, "IP Address")
        self.add_placeholder(self.port_entry, "(default port 25000)")
        self.add_placeholder(self.nickname_entry, "Nickname (optional)")

        self.ip_entry.bind("<FocusIn>", lambda event: self.focus_in(event, self.ip_entry))
        self.ip_entry.bind("<FocusOut>", lambda event: self.focus_out(event, self.ip_entry, "IP Address"))

        self.port_entry.bind("<FocusIn>", lambda event: self.focus_in(event, self.port_entry))
        self.port_entry.bind("<FocusOut>", lambda event: self.focus_out(event, self.port_entry, "(default port 25000)"))

        self.nickname_entry.bind("<FocusIn>", lambda event: self.focus_in(event, self.nickname_entry))
        self.nickname_entry.bind("<FocusOut>",
                                 lambda event: self.focus_out(event, self.nickname_entry, "Nickname (optional)"))

        self.config_frame.place(x=5, y=10)
        self.ip_entry.place(x=20, y=20, anchor="nw", width=200, height=40)
        self.port_entry.place(x=20, y=70, anchor="nw", width=200, height=40)
        self.nickname_entry.place(x=20, y=120, anchor="nw", width=200, height=40)
        self.voice_check.place(x=60, y=170, anchor="nw")
        self.start_button.place(x=125, y=230, anchor="n")

        # TTK ROOT FRAME
        self.root_frame = ttk.Frame(self.root, width=550, height=650)

        # BUTTON FRAME
        self.button_frame = ttk.Frame(self.root_frame, width=550, height=80)
        self.voice_button = ttk.Button(self.button_frame, text="Enable Voice", width=10, command=self.enable_voice)
        self.theme_button = ttk.Button(self.button_frame, text="Light Mode", width=10, command=self.change_theme)
        self.disconnect_button = ttk.Button(self.button_frame, text="Disconnect", width=10, style="Accent.TButton", command=self.disconnect)

        self.button_frame.place(x=0, y=0, anchor="nw")
        self.voice_button.place(x=525, y=22, anchor="ne", width=150, height=40)
        self.theme_button.place(x=25, y=22, anchor="nw", width=150, height=40)
        self.disconnect_button.place(x=275, y=22, anchor="n", width=120, height=40)

        # CHAT FRAME
        self.chat_frame = ttk.Frame(self.root_frame, width=550, height=363)
        self.chat_labelframe = ttk.LabelFrame(self.chat_frame, text="Chat", labelanchor="n", width=500, height=353)

        if platform == "win32":
            self.status_box = Listbox(self.chat_frame, width=68, height=4, bd=0)
            self.chat_box = Listbox(self.chat_frame, width=68, height=11, bd=0)
        elif platform == "darwin":
            self.status_box = Listbox(self.chat_frame, width=68, height=4, bd=0)
            self.chat_box = Listbox(self.chat_frame, width=68, height=16, bd=0)

        self.message_entry = ttk.Entry(self.chat_frame, width=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.chat_frame.place(x=0, y=80, anchor="nw")
        self.chat_labelframe.place(x=25, y=0, anchor="nw")
        self.status_box.place(x=35, y=20, anchor="nw")
        if platform == "win32":
            self.chat_box.place(x=35, y=90, anchor="nw")
        else:
            self.chat_box.place(x=35, y=71, anchor="nw")
        self.message_entry.place(x=40, y=297, anchor="nw", width=470, height=40)

        # STATUS FRAME
        self.status_frame = ttk.Frame(self.root_frame, width=550, height=250)
        self.chat_peer_labelframe = ttk.LabelFrame(self.status_frame, width=230, height=175,
                                                   text="Connected Peers: Chat", labelanchor="n")
        self.voice_peer_labelframe = ttk.LabelFrame(self.status_frame, width=230, height=175,
                                                    text="Connected Peers: Voice", labelanchor="n")

        self.connected_chat = Listbox(self.chat_peer_labelframe, width=23, height=8, bd=0)
        self.connected_voice = Listbox(self.voice_peer_labelframe, width=23, height=8, bd=0)

        self.status_frame.place(x=0, y=443, anchor="nw")
        self.chat_peer_labelframe.place(x=25, y=10, anchor="nw")
        self.voice_peer_labelframe.place(x=525, y=10, anchor="ne")
        self.connected_chat.place(x=12, y=5, anchor="nw")
        self.connected_voice.place(x=12, y=5, anchor="nw")

    @staticmethod
    def add_placeholder(widget, placeholder: str):
        widget.insert(0, placeholder)

    @staticmethod
    def focus_in(event, widget):
        if widget.get() == "IP Address" or widget.get() == "(default port 25000)" or widget.get() == "Nickname (optional)":
            widget.delete(0, END)

    def focus_out(self, event, widget, placeholder: str):
        if not widget.get():
            self.add_placeholder(widget, placeholder)

    def send_message(self, event=None):
        original_message = self.message_entry.get()

        self.chat_box.insert(END, f"\nMe: {original_message}")

        self.chat_box.yview(END)
        self.message_entry.delete(0, END)
        # self.chat.client_send(f"{message}")

    def set_chat(self, chat_object):
        self.chat = chat_object

    def change_theme(self):
        if self.root.call("ttk::style", "theme", "use") == "azure-dark":
            self.root.call("set_theme", "light")
            self.theme_button.configure(text="Dark Mode")
        else:
            self.root.call("set_theme", "dark")
            self.theme_button.configure(text="Light Mode")

    def enable_voice(self):
        self.status_box.delete(2)

        self.status_box.insert(2, "System (INFO): Voice Enabled.")
        self.status_box.itemconfig(2, {"fg": "green"})

        self.connected_voice.insert(END, "System: Connected")
        self.connected_voice.itemconfig(0, {"fg": "green"})

        self.voice_button.configure(text="Disable Voice", command=self.disable_voice)

    def disable_voice(self):
        self.status_box.delete(2)

        self.status_box.insert(2, "System (INFO): Voice Disabled")
        self.status_box.itemconfig(2, {"fg": "red"})

        self.connected_voice.delete(0)

        self.voice_button.configure(text="Enable Voice", command=self.enable_voice)

    def display_menu(self, connect=False, host=False):
        if connect:
            self.start_frame.destroy()
            self.root.geometry("250x325")
            self.menu_frame.place(x=0, y=0)
        if host:
            self.start_frame.destroy()
            self.host_dex()

    def host_dex(self):
        self.start_dex(host=True)

    def connect_dex(self):
        if not self.ip_entry.get() or self.ip_entry.get() == "IP Address" or (self.ip_entry.get()).isspace():
            messagebox.showerror("DexChat", "You must enter an IP address to start DexChat!")
        elif not self.port_entry.get or (self.port_entry.get()).isspace():
            if (self.port_entry.get()).isspace():
                messagebox.showerror("DexChat", "You must enter a specific port or leave as default port: 25000!")
        else:
            self.IP = self.ip_entry.get()

            if self.port_entry.get() == "(default port 25000)":
                self.PORT = 25000
            else:
                self.PORT = int(self.port_entry.get())

            if self.nickname_entry.get():
                self.NICK = self.nickname_entry.get()

                self.start_dex(connect=True)

    def start_dex(self, connect=False, host=False):
        if connect:
            self.menu_frame.destroy()
        else:
            self.start_frame.destroy()

        self.root.geometry("550x650")
        self.root_frame.place(x=0, y=0)

        self.status_box.insert(END, f"System (INFO): Running on {self.my_ip}")
        self.status_box.insert(END, "System (INFO): Encryption Enabled.")
        self.status_box.insert(END, "System (INFO): Voice Disabled.")
        if platform == "win32":
            self.status_box.insert(END,
                                   "-----------------------------------------------------------------------------------"
                                   "------------")
        elif platform == "darwin":
            self.status_box.insert(END,
                                   "-----------------------------------------------------------------------------------"
                                   "---------------")

        self.status_box.itemconfig(0, {"fg": "green"})
        self.status_box.itemconfig(1, {"fg": "green"})
        self.status_box.itemconfig(2, {"fg": "red"})

        self.connected_chat.insert(END, "System: Connected")

        self.connected_chat.itemconfig(0, {"fg": "green"})

        self.root.mainloop()

    def disconnect(self):
        for child in self.root.winfo_children():
            child.destroy()

        print(self.root.children)
        self.start_frame.place(x=0, y=0)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = GUI()

    # chat = ChatNetwork("100.67.164.33", 25000, app)
    #
    # threading.Thread(target=chat.server_accept, daemon=True).start()
    #
    # app.set_chat(chat)

    app.run()
