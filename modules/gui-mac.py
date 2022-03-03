from tkinter import Tk, Listbox, END
from tkinter import ttk
import requests
import threading

from modules.communication import ChatNetwork


class GUI:
    def __init__(self):
        # GLOBAL FLAGS
        self.chat = None
        self.voice = None

        # ROOT WINDOW
        self.root = Tk()
        self.root.title("DexChat")
        self.root.geometry("550x650")
        self.root.resizable(False, False)

        # TTK ROOT FRAME
        self.root_frame = ttk.Frame(self.root, width=550, height=650)
        self.root_frame.place(x=0, y=0)

        # VOICE FRAME
        self.voice_frame = ttk.Frame(self.root_frame, width=550, height=80)
        self.voice_button = ttk.Button(self.voice_frame, text="Enable Voice", width=10, command=self.enable_voice)
        self.theme_button = ttk.Button(self.voice_frame, text="Light Mode", width=10, command=self.change_theme)

        self.voice_frame.place(x=0, y=0, anchor="nw")
        self.voice_button.place(x=525, y=22, anchor="ne", width=150, height=40)
        self.theme_button.place(x=25, y=22, anchor="nw", width=150, height=40)

        # CHAT FRAME
        self.chat_frame = ttk.Frame(self.root_frame, width=550, height=363)
        self.chat_labelframe = ttk.LabelFrame(self.chat_frame, text="Chat", labelanchor="n", width=500, height=353)
        self.status_box = Listbox(self.chat_frame, width=53, height=4, bd=0)
        self.chat_box = Listbox(self.chat_frame, width=53, height=11, bd=0)
        self.message_entry = ttk.Entry(self.chat_frame, width=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.chat_frame.place(x=0, y=80, anchor="nw")
        self.chat_labelframe.place(x=25, y=0, anchor="nw")
        self.status_box.place(x=35, y=20, anchor="nw")
        self.chat_box.place(x=35, y=89, anchor="nw")
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

    def send_message(self, event=None):
        message = self.message_entry.get()
        self.chat.client_send(message)
        self.chat_box.insert(END, f"Me: {message}")
        self.message_entry.delete(0, END)

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

    def set_chat(self, chat):
        self.chat = chat

    def run(self):
        my_ip = requests.get("https://ifconfig.me/ip").text
        self.status_box.insert(END, f"System (INFO): Running on {my_ip}")
        self.status_box.insert(END, "System (INFO): Encryption Enabled.")
        self.status_box.insert(END, "System (INFO): Voice Disabled.")
        self.status_box.insert(END,
                               "-------------------------------------------------------------------------------------")

        self.status_box.itemconfig(0, {"fg": "green"})
        self.status_box.itemconfig(1, {"fg": "green"})
        self.status_box.itemconfig(2, {"fg": "red"})

        self.connected_chat.insert(END, "System: Connected")

        self.connected_chat.itemconfig(0, {"fg": "green"})

        self.root.call("source", "../static/themes/azure.tcl")
        self.root.call("set_theme", "dark")

        self.root.mainloop()


if __name__ == '__main__':
    app = GUI()

    chat = ChatNetwork("100.67.164.33", 25000)

    threading.Thread(target=chat.server_accept, daemon=True).start()

    app.set_chat(chat)

    app.run()
