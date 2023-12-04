from tkinter import *

class Gui():
    def __init__(self, title):
        #intialize the gui object
        self.gui = Tk()
        self.gui.title(title)
        #get screen size
        self.screen_width = self.gui.winfo_screenwidth()
        self.screen_height = self.gui.winfo_screenheight()
        #menu bar intialization
        self.gui.option_add('*tearOff', FALSE)
        self.mainframe = None

    def create_mainframe(self, px, py):
        self.mainframe = Frame(self.gui, pady=py, padx=px)
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.gui.columnconfigure(0, weight=1)
        self.gui.rowconfigure(0, weight=1)

    def create_menu(self):
        menubar = Menu(self.gui)
        menu_file = Menu(menubar)
        menu_edit = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menubar.add_cascade(menu=menu_edit, label='Edit')
        self.gui.config(menu = menubar)

    def set_screen_size(self, width_str):
        self.gui.geometry(f"+{int(self.screen_width / 2)}+{int(self.screen_height / 3)}")
        self.gui.geometry(width_str)

    def build_page(self, screen_size, menu_enabled, px, py):
        self.set_screen_size(screen_size)
        self.create_mainframe(px, py)
        if(menu_enabled):
            self.create_menu()
    