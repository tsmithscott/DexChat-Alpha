from tkinter import ttk


class StartFrame(ttk.Frame):
    def __init__(self, controller, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.controller = controller

        connect_button = ttk.Button(self, text="Connect to DexChat", style="Accent.TButton", command=self.controller.open_connect_frame)
        host_button = ttk.Button(self, text="Host DexChat", command=self.controller.open_host_frame)

        connect_button.place(x=137, y=20, anchor="n")
        host_button.place(x=137, y=65, anchor="n")
