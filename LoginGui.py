from tkinter import *
from Gui import Gui
import re

class LoginGui(Gui):
    def __init__(self):
        super().__init__("Login to Pages")

    def add_static_labels(self):
        username_label = Label(self.mainframe, text='Username: ').grid(column=1, row=2, sticky=(W, N))
        password_label = Label(self.mainframe, text='Password: ').grid(column=1, row=3, sticky=(W, N))
        register_label = Label(self.mainframe, text='Click to register account-> ', fg='Blue', bg="light blue").grid(column=1, row=4, columnspan=2, sticky=(W))

    def add_entry_fields(self):
        self.user_name_entry = Entry(self.mainframe, width=35)
        self.user_name_entry.grid(column=2, row=2, columnspan=1, sticky=(W))

        self.password_entry = Entry(self.mainframe, width=35, show="*")
        self.password_entry.grid(column=2, row=3, columnspan=1, sticky=(W))

    def add_buttons(self):
        submit_button = Button(self.mainframe, text="Login", command=self.sanatize_value).grid(column=2, row=4, sticky=(S, E))
        register_button = Button(self.mainframe, text="Register").grid(column=2, row=4)


    def create_menu(self):
        pass
    
    
    def build_page(self, screen_size, menu_enabled, px, py):
        super().build_page(screen_size, menu_enabled, px, py)
        self.add_static_labels()
        self.add_entry_fields()
        self.add_buttons()


    def sanatize_value(self):
        #validate the value to make sure it is only A-Z, a-z, or has the special chars ., !, @, #, $, @ if other characters such as ^*() or ; appear then it will fail
        clean_val = self.user_name_entry.get()
        pattern = re.compile("[A-Za-z0-9- .!@#$@]") #set regex
        result = pattern.findall(clean_val) #find all matches to the regex 
        if(len(clean_val) != len(result)): #if all matches is not equal to the orginial value then bad characters where given.
            print("Bad Entry")
            self.user_name_entry.delete(0, 'end')
   
            
        

        


    
        




