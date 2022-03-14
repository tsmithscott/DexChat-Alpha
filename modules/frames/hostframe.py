from threading import Thread
from tkinter import ttk, END

from modules.communication import ChatNetwork


class HostFrame(ttk.Frame):
    def __init__(self, controller, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.controller = controller

        self.parent.bind("<Return>", lambda event: self.configure_dex_chat())

        # Create widgets
        self.nickname_entry = ttk.Entry(self, width=10, justify="center")
        self.port_entry = ttk.Entry(self, width=10, justify="center")
        self.start_button = ttk.Button(self, text="Start", style="Accent.TButton", command=self.configure_dex_chat)
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

    def configure_dex_chat(self):
        nick = self.nickname_entry.get()
        port = self.port_entry.get()

        if nick == "Nickname (optional)":
            if port == "(default port 25000)":
                self.controller.CHAT_CONTROLLER = ChatNetwork(self.controller)
            else:
                self.controller.CHAT_CONTROLLER = ChatNetwork(self.controller, port=int(port))
        else:
            if port == "(default port 25000)":
                # RUN NICK + DEFAULT PORT HOST
                self.controller.CHAT_CONTROLLER = ChatNetwork(self.controller, nick=nick)
            else:
                # RUN NICK + SPECIFIC PORT
                self.controller.CHAT_CONTROLLER = ChatNetwork(self.controller, port=int(port), nick=nick)

        Thread(target=self.controller.CHAT_CONTROLLER.server_accept, daemon=True).start()
        self.controller.open_dex_frame()
