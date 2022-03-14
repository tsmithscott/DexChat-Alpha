from threading import Thread
from tkinter import ttk, END
from tkinter import messagebox

from modules.network.chatnetwork import ChatNetwork


class ConnectFrame(ttk.Frame):
    def __init__(self, controller, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.controller = controller

        self.parent.bind("<Return>", lambda event: self.configure_dex_chat())

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
            ip = self.ip_entry.get()
            port = self.port_entry.get()
            nick = self.nickname_entry.get()

            if port == "(default port 25000)":
                if nick == "Nickname (optional)":
                    # DEFAULT CLIENT
                    self.controller.CHAT_CONTROLLER = ChatNetwork(self.controller)
                else:
                    # NICK + DEFAULT PORT CLIENT
                    self.controller.CHAT_CONTROLLER = ChatNetwork(self.controller, nick=nick)
            else:
                if nick == "Nickname (optional)":
                    # SPECIFIC PORT + NON-NICK
                    self.controller.CHAT_CONTROLLER = ChatNetwork(self.controller, port=int(port))
                else:
                    # SPECIFIC PORT + NICK
                    self.controller.CHAT_CONTROLLER = ChatNetwork(self.controller, port=int(port), nick=nick)

            Thread(target=self.controller.CHAT_CONTROLLER.server_accept, daemon=True).start()

            if port == "(default port 25000)":
                self.controller.CHAT_CONTROLLER.connect(ip, 25000)
            else:
                self.controller.CHAT_CONTROLLER.connect(ip, int(port))

            self.controller.open_dex_frame()
