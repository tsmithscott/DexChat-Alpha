from tkinter import Tk, Frame, Button, Listbox, LabelFrame, END, RIDGE, Entry


class GUI:
    def __init__(self):
        # ROOT WINDOW
        self.root = Tk()
        self.root.title("DexChat")
        self.root.geometry("550x650")
        self.root.resizable(False, False)

        # VOICE FRAME
        self.voice_frame = Frame(self.root, width=550, height=100)
        self.voice_button = Button(self.voice_frame, text="Enable Voice", padx=20, pady=10, command=self.enable_voice)

        self.voice_frame.place(x=0, y=0, anchor="nw")
        self.voice_button.place(x=525, y=30, anchor="ne")

        # CHAT FRAME
        self.chat_frame = Frame(self.root, width=550, height=300)
        self.chat_labelframe = LabelFrame(self.chat_frame, width=500, height=290)
        self.status_box = Listbox(self.chat_frame, width=53, height=10, bd=0)
        self.chat_box = Listbox(self.chat_frame, width=53, height=7, bd=0)
        self.message_entry = Entry(self.chat_frame, width=51, relief=RIDGE)
        self.message_entry.bind("<Return>", self.send_message)

        self.chat_frame.place(x=0, y=100, anchor="nw")
        self.chat_labelframe.place(x=25, y=0, anchor="nw")
        self.status_box.place(x=35, y=10, anchor="nw")
        self.chat_box.place(x=35, y=62, anchor="nw")
        self.message_entry.place(x=40, y=200, anchor="nw")

        # STATUS FRAME
        self.status_frame = Frame(self.root, width=550, height=250)
        self.chat_peer_labelframe = LabelFrame(self.status_frame, width=230, height=175, text="Connected Peers: Chat",
                                               labelanchor="n")
        self.voice_peer_labelframe = LabelFrame(self.status_frame, width=230, height=175, text="Connected Peers: Voice",
                                                labelanchor="n")

        self.connected_chat = Listbox(self.chat_peer_labelframe, width=20, height=8, bd=0)
        self.connected_voice = Listbox(self.voice_peer_labelframe, width=20, height=8, bd=0)

        self.status_frame.place(x=0, y=400, anchor="nw")
        self.chat_peer_labelframe.place(x=25, y=10, anchor="nw")
        self.voice_peer_labelframe.place(x=525, y=10, anchor="ne")
        self.connected_chat.place(x=12, y=5, anchor="nw")
        self.connected_voice.place(x=12, y=5, anchor="nw")

    def send_message(self, event=None):
        message = self.message_entry.get()
        self.chat_box.insert(END, f"Me: {message}")
        self.message_entry.delete(0, END)

    def enable_voice(self):
        self.status_box.delete(1)

        self.status_box.insert(1, "System (INFO): Voice Enabled.")
        self.status_box.itemconfig(1, {"fg": "green"})

        self.connected_voice.insert(END, "System: Connected")
        self.connected_voice.itemconfig(0, {"fg": "green"})

        self.voice_button.configure(text="Disable Voice", command=self.disable_voice)

    def disable_voice(self):
        self.status_box.delete(1)

        self.status_box.insert(1, "System (INFO): Voice Disabled")
        self.status_box.itemconfig(1, {"fg": "red"})

        self.connected_voice.delete(0)

        self.voice_button.configure(text="Enable Voice", command=self.enable_voice)

    def run(self):
        self.status_box.insert(END, "System (INFO): Encryption Enabled.")
        self.status_box.insert(END, "System (INFO): Voice Disabled.")
        self.status_box.insert(END,
                               "-------------------------------------------------------------------------------------")

        self.status_box.itemconfig(0, {"fg": "green"})
        self.status_box.itemconfig(1, {"fg": "red"})

        self.connected_chat.insert(END, "System: Connected")

        self.connected_chat.itemconfig(0, {"fg": "green"})

        self.root.mainloop()


if __name__ == '__main__':
    app = GUI()
    app.run()
