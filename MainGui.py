from tkinter import *
from tkinter import ttk
from Gui import Gui
from Db_Actions import Db_Actions
from BasicFunctions import BasicFunctions
from LinkedList import LinkedList
from Node import Node
from NoteWindow import NoteWindow
from Window import Window
from Queue import Queue

CELL_WIDTH = 15

db = Db_Actions()
f = BasicFunctions()
class MainGui(Gui):

    def __init__(self, session, check):
        super().__init__("Passwords")
        self.session = session
        self.row_list = LinkedList()
        self.search_list = None
        self.row_data = []
        self.search_string = StringVar()
        self.save_queue = Queue()
        self.program_running = check
        
        
        
        
    def add_statics(self):
        Label(self.mainframe, text=f"Welcome to Notes: {self.session.active_full_name}", 
              font=('Arial', 10, 'bold')).grid(column=1, row=0, columnspan=3, sticky=(W))
        
        Button(self.mainframe, text='Search', command=self.search_table, height=1).grid(column= 3, row=0, sticky=(N, W), padx=15, pady=5)
        Entry(self.mainframe, width=25, textvariable=self.search_string).grid(column=3, row=0, columnspan=2, sticky=(E))

    def add_table(self):
        if self.search_list is not None:
            self.table = Table(self.mainframe, self.row_list, self.row_data, self.session, self.search_list)
        else:
            self.table = Table(self.mainframe, self.row_list, self.row_data, self.session)
        self.row_list = self.table.table_setup()

    def create_menu(self):
        menubar = Menu(self.gui)
        menu_file = Menu(menubar)
        menu_edit = Menu(menubar)
        menu_sort = Menu(menubar)

        menubar.add_cascade(menu=menu_file, label='Options')
        menu_file.add_command(label='Save', command=self.save_data)
        menu_file.add_command(label='Logout', command=self.logout_user)

        menubar.add_cascade(menu=menu_edit, label='Edit')
        menu_edit.add_command(label='Add', command=self.add_entry)
        menu_edit.add_command(label='Delete', command=lambda: self.row_select_popup('delete'))
        menu_edit.add_command(label='Modify', command=lambda: self.row_select_popup('modify'))
        

        menubar.add_cascade(menu=menu_sort, label='Sort')
        menu_sort.add_command(label='Sort Alpha', command=lambda: self.sort_table('note_site_name'))
        menu_sort.add_command(label='Sort RowID', command=lambda: self.sort_table('note_row_id'))
    
        
        
        
        #menubar.add_cascade(menu=menu_sort, label='Sort', command=self.sort_table)
        self.gui.config(menu = menubar)

    def build_page(self, screen_size, px, py):
        super().build_page(screen_size, px, py)
        self.create_menu()
        self.add_statics()
        self.add_table()

    def add_entry(self):
        self.add_window = NoteWindow("Add Site", self.row_list, self.session, 'add', self.save_queue)
        self.add_window.build_window()   
        
    def delete_entry(self):
        self.popup.window.grab_release()
        self.popup.window.destroy()
        self.delete_window = NoteWindow("Delete Site", self.row_list, self.session, 'delete', self.save_queue, self.selection)
        self.delete_window.build_window()

    def modify_entry(self):
        self.popup.window.grab_release()
        self.popup.window.destroy()
        self.delete_window = NoteWindow("Modify Site", self.row_list, self.session, 'modify', self.save_queue, self.selection)
        self.delete_window.build_window()

    def search_table(self, *args):
        #Table is built with a LL, use new LL to display search data
        self.search_list = LinkedList()
        temp = self.row_list.head
        #loop current tables rows
        while temp is not None:
            #get the site_name from current row
            site_name = temp.data['note_site_name']
            #check if the current search string is in the site_name
            if site_name.find(self.search_string.get()) != -1:
                #delete pointers we are appending
                new_node = Node(temp.data)
                self.search_list.append(new_node)
            temp = temp.next
        
        self.refresh_table()
        
    def sort_table(self, cmp_value):
        self.row_list.sort_alpha(cmp_value)
        self.refresh_table()

    def save_data(self):
        db.queue_to_db(self.save_queue)

    def row_select_popup(self, action = 'add'):
        self.selection = StringVar()
        self.popup = Window('Get Row #', "200x100", self.gui)
        
        self.row_combo = ttk.Combobox(self.popup.mainframe, textvariable=self.selection, state='readonly', width=22)
        num_row_tuple = f.num_rows_list(self.row_list.length)
        self.row_combo.grid(column=0, row=0, columnspan=2, sticky=(N))
        self.row_combo['values'] = num_row_tuple
        self.row_combo.set('Select a Row to Change')

        action_button = Button(self.popup.mainframe, text="Done")
        
        if(action == 'delete'):
            action_button.config(command=self.delete_entry)
            action_button.grid(column=1, row=1, sticky=(E))
        elif(action == 'modify'):
            action_button.config(command=self.modify_entry)
            action_button.grid(column=1, row=1, sticky=(E))

        self.popup.window.transient(self.gui)   # dialog window is related to main
        self.popup.window.wait_visibility() # can't grab until window appears, so we wait
        self.popup.window.grab_set()        # ensure all input goes to our window
        self.popup.window.wait_window()     # block until window is destroyed
                

    def refresh_table(self):
        self.mainframe.destroy()
        self.create_mainframe(10, 5)
        self.add_statics()
        self.add_table()

    def logout_user(self):
        self.close_window()

        



class Table():

    def __init__(self, mainframe, row_list, row_data, session, search_list = None):
        self.session = session
        self.mainframe = mainframe
        self.column_headers = ['Site Name', 'Password', 'Last Modification', 'Created On']
        self.row_list = row_list
        self.search_list = search_list
        self.row_data = row_data

    def table_setup(self):
        for key, header in enumerate(self.column_headers):
            Label(self.mainframe, width=CELL_WIDTH, height=2, text=header, borderwidth=1, relief='solid').grid(column=key+1, row=1, sticky=(E))

        if self.session.inital_launch:
            for row in db.get_tabel_data(self.session.active_user_id):
                self.build_row_list(row)
            #self.row_list.print_info()

        self.build_rows()
        return self.row_list


    def build_row_list(self, row_data):
        new_node = f.create_row_node(row_data[0], row_data[1],row_data[2],row_data[3],row_data[4], row_data[5], (self.row_list.length + 1))
        self.row_list.append(new_node)

    def build_rows(self):
        if self.search_list is not None:
            temp = self.search_list.head
        else:
            temp = self.row_list.head
        if temp == None:
            Label(self.mainframe, text="No Data Avalible. Add Data to display", borderwidth=1, relief='sunken', 
                  font=("Arial", 18)).grid(column=1, columnspan=4, row=2, sticky=(N))

        row_number = 2
        while temp is not None:
            row_data = temp.data
            Label(self.mainframe, width=5, height=2, text=row_data['note_row_id'], 
                  borderwidth=1, relief='sunken' ).grid(column=0, row=row_number, sticky=(S))
            
            Label(self.mainframe, width=CELL_WIDTH, height=2, text=row_data['note_site_name'], 
                  borderwidth=1, relief='sunken').grid(column=1, row=row_number, sticky=(E))
            
            Label(self.mainframe, width=CELL_WIDTH, height=2, text=row_data['note_password'], 
                  borderwidth=1, relief='sunken').grid(column=2, row=row_number, sticky=(E))
            
            Label(self.mainframe, width=CELL_WIDTH, height=2, text=row_data['note_last_mod_date'], 
                  borderwidth=1, relief='sunken').grid(column=3, row=row_number, sticky=(E))
            
            Label(self.mainframe, width=CELL_WIDTH, height=2, text=row_data['note_creation_date'], 
                  borderwidth=1, relief='sunken').grid(column=4, row=row_number, sticky=(E))
            
            temp = temp.next
            row_number += 1
