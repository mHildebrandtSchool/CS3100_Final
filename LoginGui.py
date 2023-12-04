from tkinter import *
from Gui import Gui
from Window import Window
from Db_Actions import Db_Actions
from BasicFunctions import BasicFunctions as f
import re

class LoginGui(Gui):
    def __init__(self):
        super().__init__("Login to Pages")
        self.validate = (self.gui.register(self.is_valid), '%P')
        self.isValidEntry = False
        self.username = StringVar()
        self.password = StringVar()
        

    def add_static_labels(self):
        Label(self.mainframe, text='Username: ').grid(column=1, row=2, sticky=(W, N))
        Label(self.mainframe, text='Password: ').grid(column=1, row=3, sticky=(W, N))
        Label(self.mainframe, text='Click to register account-> ',
                                fg='Blue', bg="light blue").grid(column=1, row=4, columnspan=2, sticky=(W))
        self.error_label = Label(self.mainframe, text="Only use a-z, A-Z, numbers 0-9, and no whitespace", foreground="white", bg="red")



    def add_remove_error_label(self):
        if not self.isValidEntry:
            self.error_label.grid(column=1, row=5, columnspan=3)
        else:
            self.error_label.grid_forget()


    def add_entry_fields(self):
        Entry(self.mainframe, width=35, textvariable=self.username, validate="key",
               validatecommand=self.validate).grid(column=2, row=2, columnspan=1, sticky=(W))
        
        Entry(self.mainframe, width=35, show="*", textvariable=self.password, validate="key",
               validatecommand=self.validate).grid(column=2, row=3, columnspan=1, sticky=(W))

    def add_buttons(self):
        submit_button = Button(self.mainframe, text="Login").grid(column=2, row=4, sticky=(S, E))
        register_button = Button(self.mainframe, text="Register", command=self.register_window).grid(column=2, row=4)


    def register_window(self):
        window = RegisterWindow()
    
    
    def build_page(self, screen_size, menu_enabled, px, py):
        super().build_page(screen_size, menu_enabled, px, py)
        self.add_static_labels()
        self.add_entry_fields()
        self.add_buttons()


    def is_valid(self, entry):
        #validate the value to make sure it is only A-Z, a-z, or has the special chars ., !, @, #, $, @ if other characters such as ^*() or ; appear then it will fail
        pattern = re.compile("[A-Za-z0-9]") #set regex
        result = pattern.findall(entry) #find all matches to the regex
        if(len(entry) != len(result)): #if all matches is not equal to the orginial value then bad characters where given.
            self.isValidEntry = False
            self.add_remove_error_label()
            print("bad")
        else:
            self.isValidEntry = True
            self.add_remove_error_label()
            print("Good")
        
        return True #Want to allow bad character with a popup error message returning false prevents typing character at all
    
class RegisterWindow(Window):

    def __init__(self):
        super().__init__("Register", "300x200")
        self.username = StringVar()
        self.password = StringVar()
        self.email = StringVar()
        self.name = StringVar()
        self.add_static_labels()
        self.add_entries()
        self.add_buttons()

    def add_static_labels(self):
        Label(self.mainframe, text='Name: ').grid(column=1, row=1, sticky=(E))
        Label(self.mainframe, text=' ').grid(column=1, row=2, sticky=(E))
        Label(self.mainframe, text='Email: ').grid(column=1, row=3, sticky=(E))
        Label(self.mainframe, text=' ').grid(column=1, row=4, sticky=(E))
        Label(self.mainframe, text='Username: ').grid(column=1, row=5, sticky=(E))
        Label(self.mainframe, text=' ').grid(column=1, row=6, sticky=(E))
        Label(self.mainframe, text='Password: ').grid(column=1, row=7, sticky=(E))

    def add_entries(self):
        Entry(self.mainframe, width=35, textvariable=self.name).grid(column=2, row=1, columnspan=1, sticky=(W))
        Entry(self.mainframe, width=35, textvariable=self.email).grid(column=2, row=3, columnspan=1, sticky=(W))
        Entry(self.mainframe, width=35, textvariable=self.username).grid(column=2, row=5, columnspan=1, sticky=(W))
        Entry(self.mainframe, width=35, textvariable=self.password).grid(column=2, row=7, columnspan=1, sticky=(W))

    def add_buttons(self):
        Button(self.mainframe, text="Register", command=self.process_form).grid(column=2, row=8, sticky=(E), pady=5)
        Button(self.mainframe, text="Cancel", command=self.window.destroy).grid(column=2, row=8, sticky=(E), pady=5, padx=60)
        
    def process_form(self):
        db = Db_Actions()
        form_data = [self.username.get(), self.name.get(), self.email.get(), self.password.get()]

        for data in form_data:
            if f.check_regex(data):
                print(data)

        db.one_step_insert('users', form_data)
        self.window.destroy()

