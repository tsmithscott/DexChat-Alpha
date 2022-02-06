import tkinter as tk


class GUI(tk.Frame):

    def __init__(self):
        super().__init__()
        root.title("DexChat")
        root.geometry("275x400")

        startup_frame = tk.Frame(root)
        connect_frame = tk.Frame(root)
        messages_frame = tk.Frame(root)
        voice_frame = tk.Frame(root)

        """==========Widgets for startup_frame========== """


        """==========Widgets for connect_frame=========="""


        """==========Widgets for messages_frame=========="""
        client_message = tk.StringVar()
        client_message.set("Type your message here.")
        entry_field = tk.Entry(root, textvariable=client_message)
        # entry_field.bind("<Return>", send_message())
        # entry_field.bind("<Button-1>", placeholder)

        scrollbar = tk.Scrollbar(messages_frame)
        message_view = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        message_view.place(x=7, y=25, anchor=tk.CENTER)
        send_button = tk.Button(root, text="Send")

        message_view.pack()
        messages_frame.pack()
        message_view.pack()
        messages_frame.pack()
        entry_field.pack()
        send_button.pack()
        """==========Widgets for voice_frame=========="""




        # root.protocol("WM_DELETE_WINDOW", close)


if __name__ == "__main__":
    root = tk.Tk()
    GUI().pack(side="top", fill="both", expand=True)
    root.mainloop()
