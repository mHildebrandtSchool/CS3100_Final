from tkinter import *
from Gui import Gui
from Db_Actions import Db_Actions
from BasicFunctions import BasicFunctions
from LinkedList import LinkedList
from Node import Node
from NoteWindow import NoteWindow

CELL_WIDTH = 15

db = Db_Actions()
f = BasicFunctions()
class MainGui(Gui):

    def __init__(self, session):
        super().__init__("Passwords")
        self.session = session
        self.row_list = LinkedList()
        self.row_data = []
        
        
    def add_static_labels(self):
        pass

    def add_table(self):
        self.table = Table(self.mainframe, self.row_list, self.row_data)
        self.row_list = self.table.table_setup()

    def create_menu(self):
        menubar = Menu(self.gui)
        menu_file = Menu(menubar)

        menu_edit = Menu(menubar)
        menu_edit.add_command(label='Add', command=self.add_entry)

        menu_sort = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='Options')
        menubar.add_cascade(menu=menu_edit, label='Edit')
        menubar.add_cascade(menu=menu_sort, label='Sort')
        self.gui.config(menu = menubar)

    def build_page(self, screen_size, px, py):
        super().build_page(screen_size, px, py)
        self.create_menu()
        self.add_static_labels()
        self.add_table()

    def add_entry(self):
        self.add_window = NoteWindow("Add Site", self.row_list, self.session)
        self.add_window.build_window()
        

class Table():

    def __init__(self, mainframe, row_list, row_data):
        self.mainframe = mainframe
        self.column_headers = ['Site Name', 'Password', 'Last Modification', 'Created On']
        self.row_list = row_list
        self.row_data = row_data

    def table_setup(self):
        for key, header in enumerate(self.column_headers):
            Label(self.mainframe, width=CELL_WIDTH, height=2, text=header, borderwidth=1, relief='solid').grid(column=key+1, row=1, sticky=(E))

        if self.row_list.head == None:
            for row in db.get_tabel_data():
                self.build_row_list(row)
            #self.row_list.print_info()
            
        self.build_rows()
        return self.row_list


    def build_row_list(self, row_data):
        new_node = f.create_row_node(row_data[0],row_data[1],row_data[2],row_data[3],row_data[4],row_data[5], row_data[6])
        self.row_list.append(new_node)

    def build_rows(self):
        temp = self.row_list.head
        row_number = 2
        while temp is not None:
            row_data = temp.data
            Label(self.mainframe, width=5, height=2, text=row_number - 1, borderwidth=1, relief='sunken' ).grid(column=0, row=row_number, sticky=(S))
            Label(self.mainframe, width=CELL_WIDTH, height=2, text=row_data['note_site_name'], borderwidth=1, relief='sunken').grid(column=1, row=row_number, sticky=(E))
            Label(self.mainframe, width=CELL_WIDTH, height=2, text=row_data['note_password'], borderwidth=1, relief='sunken').grid(column=2, row=row_number, sticky=(E))
            Label(self.mainframe, width=CELL_WIDTH, height=2, text=row_data['note_last_mod_date'], borderwidth=1, relief='sunken').grid(column=3, row=row_number, sticky=(E))
            Label(self.mainframe, width=CELL_WIDTH, height=2, text=row_data['note_creation_date'], borderwidth=1, relief='sunken').grid(column=4, row=row_number, sticky=(E))
            temp = temp.next
            row_number += 1
