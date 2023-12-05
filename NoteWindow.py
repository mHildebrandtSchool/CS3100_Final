from tkinter import *
from Window import Window
from Node import Node
from BasicFunctions import BasicFunctions
from datetime import date

f = BasicFunctions()

class NoteWindow(Window):

    def __init__(self, window_title, row_list, session):
        super().__init__(window_title, "300x200",)
        self.new_name = StringVar()
        self.new_password = StringVar()
        self.the_text = Text(self.mainframe, width=35, height=5)
        self.row_list = row_list
        self.session = session
    
    def build_window(self):
         Label(self.mainframe, text="Site Name: ").grid(column=0, row=0, sticky=(E))
         Entry(self.mainframe, textvariable=self.new_name, width=35).grid(column=1, columnspan=2, row=0, sticky=(E))

         Label(self.mainframe, text="Notes: ").grid(column=0, row=2, sticky=(W))
         self.the_text.grid(column=0,columnspan=3, row=3, sticky=(E))

         Label(self.mainframe, text="Password: ").grid(column=0, row=4, sticky=(W))
         Entry(self.mainframe, textvariable=self.new_password, width=35).grid(column=1, columnspan=2, row=4, pady=5, sticky=(E))

         Button(self.mainframe, text='Cancel', command=self.close_window).grid(column=2, row=5, sticky=(N))
         Button(self.mainframe, text='Add', command=self.add_data).grid(column=2, row=5, sticky=(E))



    def close_window(self):
        self.window.destroy()

    def add_data(self):
        current_date = date.today()
        current_date.isoformat()
        user = self.session.active_user_id
        new_node = f.create_row_node(None, self.session.active_user_id, self.the_text.get('1.0', 'end'), self.new_password.get(), self.new_name.get(),
                                     current_date.strftime("%m/%d/%y"), current_date.strftime("%m/%d/%y"))
        self.row_list.append(new_node)
        f.refresh_tabel(self.session.main_gui.mainframe)
        self.session.main_gui.create_mainframe(10, 5)
        self.session.main_gui.add_table()
        self.row_list.print_info()
        self.window.destroy()