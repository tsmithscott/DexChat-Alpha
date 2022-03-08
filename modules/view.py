from tkinter import Tk
from tkinter import ttk


class StartFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        connect_button = ttk.Button(self, text="Connect to DexChat", style="Accent.TButton")
        host_button = ttk.Button(self, text="Host DexChat")

        connect_button.place(x=137, y=20, anchor="n")
        host_button.place(x=137, y=65, anchor="n")


class View(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent

        self.start_frame = StartFrame(self, width=275, height=115)


if __name__ == '__main__':
    root = Tk()
    root.title("DexChat")
    root.geometry("275x115")
    root.resizable(False, False)
    root.call("source", "../static/themes/azure.tcl")
    root.call("set_theme", "dark")

    View(root).place(x=0, y=0)
    root.mainloop()
