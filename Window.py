from tkinter import *

class Window():
    def __init__(self, window_title, window_size):
        self.window = Toplevel()
        self.window.geometry(f"+{int(self.window.winfo_screenwidth() / 2)}+{int(self.window.winfo_screenheight() / 3)}")
        self.window.geometry(window_size)
        self.window.title(window_title)
        self.create_mainframe(10, 5)
        

    def create_mainframe(self, px, py):
        self.mainframe = Frame(self.window, pady=py, padx=px)
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

    