from sys import platform
from threading import Thread

from tkinter import Tk, BooleanVar, END, messagebox, Listbox, Label
from tkinter import ttk

from modules.communication import ChatNetwork


class StartFrame(ttk.Frame):
    def __init__(self, controller, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.controller = controller

        connect_button = ttk.Button(self, text="Connect to DexChat", style="Accent.TButton", command=self.controller.open_connect_frame)
        host_button = ttk.Button(self, text="Host DexChat", command=self.controller.open_host_frame)

        connect_button.place(x=137, y=20, anchor="n")
        host_button.place(x=137, y=65, anchor="n")


class ConnectFrame(ttk.Frame):
    def __init__(self, controller, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.controller = controller

        # Create input widgets
        self.ip_entry = ttk.Entry(self, width=10, justify="center")
        self.port_entry = ttk.Entry(self, width=10, justify="center")
        self.nickname_entry = ttk.Entry(self, width=10, justify="center")
        self.voice_check = ttk.Checkbutton(self, text="Enable DexVoice", variable=self.controller.VOICE_ENABLED)
        self.start_button = ttk.Button(self, text="Connect", style="Accent.TButton", command=self.configure_dex_chat)
        self.cancel_button = ttk.Button(self, text="Cancel", command=self.controller.cancel)

        # Place widgets on frame
        self.ip_entry.place(x=25, y=30, anchor="nw", width=200, height=40)
        self.port_entry.place(x=25, y=80, anchor="nw", width=200, height=40)
        self.nickname_entry.place(x=25, y=130, anchor="nw", width=200, height=40)
        self.voice_check.place(x=65, y=185, anchor="nw")
        self.start_button.place(x=125, y=230, anchor="n")
        self.cancel_button.place(x=125, y=275, anchor="n")

        self.add_placeholder(self.ip_entry, "IP Address")
        self.add_placeholder(self.port_entry, "(default port 25000)")
        self.add_placeholder(self.nickname_entry, "Nickname (optional)")

        self.ip_entry.bind("<FocusIn>", lambda event: self.focus_in(self.ip_entry))
        self.ip_entry.bind("<FocusOut>", lambda event: self.focus_out(self.ip_entry, "IP Address"))

        self.port_entry.bind("<FocusIn>", lambda event: self.focus_in(self.port_entry))
        self.port_entry.bind("<FocusOut>", lambda event: self.focus_out(self.port_entry, "(default port 25000)"))

        self.nickname_entry.bind("<FocusIn>", lambda event: self.focus_in(self.nickname_entry))
        self.nickname_entry.bind("<FocusOut>", lambda event: self.focus_out(self.nickname_entry, "Nickname (optional)"))

    @staticmethod
    def add_placeholder(widget, placeholder: str):
        widget.insert(0, placeholder)

    @staticmethod
    def focus_in(widget):
        if widget.get() == "IP Address" or widget.get() == "(default port 25000)" or widget.get() == "Nickname (optional)":
            widget.delete(0, END)

    def focus_out(self, widget, placeholder: str):
        if not widget.get():
            self.add_placeholder(widget, placeholder)

    def configure_dex_chat(self):
        if not self.ip_entry.get() or self.ip_entry.get() == "IP Address" or (self.ip_entry.get()).isspace():
            messagebox.showerror("DexChat", "You must enter an IP address to start DexChat!")
        elif not self.port_entry.get() or (self.port_entry.get()).isspace():
            if (self.port_entry.get()).isspace():
                messagebox.showerror("DexChat", "You must enter a specific port or leave as default port: 25000!")
        else:
            self.controller.IP = self.ip_entry.get()

            if self.port_entry.get() == "(default port 25000)":
                self.controller.PORT = 25000
            else:
                self.controller.PORT = int(self.port_entry.get())

            if self.nickname_entry.get() != "Nickname (optional)":
                self.controller.NICK = self.nickname_entry.get()
            else:
                self.controller.NICK = None

            self.controller.start_dex_client()


class HostFrame(ttk.Frame):
    def __init__(self, controller, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.controller = controller

        # Create widgets
        self.nickname_entry = ttk.Entry(self, width=10, justify="center")
        self.port_entry = ttk.Entry(self, width=10, justify="center")
        self.start_button = ttk.Button(self, text="Start", style="Accent.TButton", command=self.controller.start_dex_host)
        self.cancel_button = ttk.Button(self, text="Cancel", command=self.controller.cancel_host)

        # Place widgets
        self.nickname_entry.place(x=25, y=30, anchor="nw", width=200, height=40)
        self.port_entry.place(x=25, y=80, anchor="nw", width=200, height=40)
        self.start_button.place(x=125, y=135, anchor="n")
        self.cancel_button.place(x=125, y=180, anchor="n")

        self.add_placeholder(self.nickname_entry, "Nickname (optional)")
        self.add_placeholder(self.port_entry, "(default port 25000)")

        self.nickname_entry.bind("<FocusIn>", lambda event: self.focus_in(self.nickname_entry))
        self.nickname_entry.bind("<FocusOut>", lambda event: self.focus_out(self.nickname_entry, "Nickname (optional)"))

        self.port_entry.bind("<FocusIn>", lambda event: self.focus_in(self.port_entry))
        self.port_entry.bind("<FocusOut>", lambda event: self.focus_out(self.port_entry, "(default port 25000)"))

    @staticmethod
    def add_placeholder(widget, placeholder: str):
        widget.insert(0, placeholder)

    @staticmethod
    def focus_in(widget):
        if widget.get() == "IP Address" or widget.get() == "(default port 25000)" or widget.get() == "Nickname (optional)":
            widget.delete(0, END)

    def focus_out(self, widget, placeholder: str):
        if not widget.get():
            self.add_placeholder(widget, placeholder)

    def configure_dex_chat(self):  # TODO: Bind to start button and add handling for custom port in communication.py and controller.start_dex_host()
        if not self.port_entry.get() or (self.port_entry.get()).isspace():
            if (self.port_entry.get()).isspace():
                messagebox.showerror("DexChat", "You must enter a specific port or leave as default port: 25000!")
        else:
            if self.nickname_entry.get() != "Nickname (optional)":
                self.controller.NICK = self.nickname_entry.get()
            else:
                self.controller.NICK = None

            if self.port_entry.get() == "(default port 25000)":
                self.controller.PORT = 25000
            else:
                self.controller.PORT = int(self.port_entry.get())

            self.controller.start_dex_host()


class DexFrame(ttk.Frame):
    def __init__(self, controller, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.controller = controller

        # Create button frame and buttons
        button_frame = ttk.Frame(self, width=550, height=80)
        self.voice_button = ttk.Button(button_frame, text="Enable Voice", width=10, command=self.enable_voice)
        self.theme_button = ttk.Button(button_frame, text="Light Mode", width=10, command=self.change_theme)
        disconnect_button = ttk.Button(button_frame, text="Disconnect", width=10, style="Accent.TButton", command=self.controller.disconnect)

        # Place button frame and buttons
        button_frame.place(x=0, y=0, anchor="nw")
        self.voice_button.place(x=525, y=22, anchor="ne", width=150, height=40)
        self.theme_button.place(x=25, y=22, anchor="nw", width=150, height=40)
        disconnect_button.place(x=275, y=22, anchor="n", width=120, height=40)

        chat_frame = ttk.Frame(self, width=550, height=363)
        chat_labelframe = ttk.LabelFrame(chat_frame, text="Chat", labelanchor="n", width=500, height=353)

        status_frame = ttk.Frame(self, width=550, height=250)
        chat_peer_labelframe = ttk.LabelFrame(status_frame, width=230, height=175, text="Connected Peers: Chat", labelanchor="n")
        voice_peer_labelframe = ttk.LabelFrame(status_frame, width=230, height=175, text="Connected Peers: Voice", labelanchor="n")

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
            self.chat_box = Listbox(chat_frame, width=53, height=12, bd=0)

            self.chat_box.place(x=35, y=71, anchor="nw")

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
            self.status_box.insert(END, "-----------------------------------------------------------------------------------------------")
        elif platform == "darwin":
            self.status_box.insert(END, "--------------------------------------------------------------------------------------------------")

        self.status_box.itemconfig(0, {"fg": "green"})
        self.status_box.itemconfig(1, {"fg": "green"})
        self.status_box.itemconfig(2, {"fg": "red"})

        self.connected_chat.insert(END, "System: Connected")

        self.connected_chat.itemconfig(0, {"fg": "green"})

        quote_label = Label(self, text="Simplicity, carried to the extreme, becomes elegance.", font=("Courier", 11, "italic"), justify="center")
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

    def send_message(self, event):
        message = self.message_entry.get()

        self.chat_box.yview(END)
        self.message_entry.delete(0, END)
        self.controller.CHAT.client_send(message)


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("DexChat")
        self.root.geometry("275x115")
        self.root.resizable(False, False)
        self.root.call("source", "./static/themes/azure.tcl")
        self.root.call("set_theme", "dark")

        self.IP = None
        self.PORT = None
        self.NICK = None
        self.VOICE_ENABLED = BooleanVar(self.root)
        self.CHAT = None

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

    def start_dex_client(self):
        self.connect_frame.destroy()
        self.resize_root(550, 685)

        self.CHAT = ChatNetwork(self)
        Thread(target=self.CHAT.server_accept, daemon=True).start()

        self.CHAT.set_nick(self.NICK)

        self.CHAT.connect(self.IP, self.PORT)

        self.dex_frame = DexFrame(self, self.root, width=550, height=685)
        self.dex_frame.place(x=0, y=0)

    def start_dex_host(self):
        self.host_frame.destroy()
        self.resize_root(550, 685)

        self.CHAT = ChatNetwork(self)
        self.CHAT.set_nick(self.NICK)
        Thread(target=self.CHAT.server_accept, daemon=True).start()

        self.dex_frame = DexFrame(self, self.root, width=550, height=685)
        self.dex_frame.place(x=0, y=0)

    def resize_root(self, width, height):
        self.root.geometry(f"{width}x{height}")

    def disconnect(self):
        self.CHAT.client_send("/disconnect")
        self.resize_root(275, 115)
        self.dex_frame.destroy()
        self.start_frame = StartFrame(self, self.root, width=275, height=115)
        self.start_frame.place(x=0, y=0)

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


if __name__ == '__main__':
    App().run()
