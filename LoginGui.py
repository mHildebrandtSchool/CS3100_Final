from tkinter import *
from Gui import Gui
from Window import Window
from Db_Actions import Db_Actions
from BasicFunctions import BasicFunctions
import hashlib
import re
functions = BasicFunctions()
db = Db_Actions()
class LoginGui(Gui):
    def __init__(self, session):
        super().__init__("Login to Pages")
        self.session = session
        self.validate = (self.gui.register(self.is_valid), '%P')
        self.isValidEntry = False
        self.username = StringVar()
        self.password = StringVar()
        

    def add_static_labels(self):
        Label(self.mainframe, text='Username: ').grid(column=1, row=2, sticky=(W, N))
        Label(self.mainframe, text='Password: ').grid(column=1, row=3, sticky=(W, N))
        Label(self.mainframe, text='Click to register account-> ',
                                fg='Blue', bg="light blue").grid(column=1, row=4, columnspan=2, sticky=(W))
        self.error_label_character = Label(self.mainframe, text="Only use a-z, A-Z, numbers 0-9, and no whitespace", foreground="white", bg="red")
        self.error_label_login = Label(self.mainframe, text="Incorrect Username or Password. Please Try Again.", foreground="white", bg="red")



    def add_remove_error_label(self):
        if not self.isValidEntry:
            self.error_label_character.grid(column=1, row=5, columnspan=3)
        else:
            self.error_label_character.grid_forget()


    def add_entry_fields(self):
        Entry(self.mainframe, width=35, textvariable=self.username, validate="key",
               validatecommand=self.validate).grid(column=2, row=2, columnspan=1, sticky=(W))
        
        Entry(self.mainframe, width=35, show="*", textvariable=self.password, validate="key",
               validatecommand=self.validate).grid(column=2, row=3, columnspan=1, sticky=(W))
        
    def add_buttons(self):
        submit_button = Button(self.mainframe, text="Login", command=self.do_login).grid(column=2, row=4, sticky=(S, E))
        register_button = Button(self.mainframe, text="Register", command=self.register_window).grid(column=2, row=4)


    def register_window(self):
        window = RegisterWindow()
    
    
    def build_page(self, screen_size, px, py):
        super().build_page(screen_size, px, py)
        self.add_static_labels()
        self.add_entry_fields()
        self.add_buttons()


    def is_valid(self, entry):
        #validate the value to make sure it is only A-Z, a-z, or has the special chars ., !, @, #, $, @ if other characters such as ^*() or ; appear then it will fail
        pattern = re.compile("[A-Za-z0-9\s._~()'!*:@,+?-]") #set regex
        result = pattern.findall(entry) #find all matches to the regex
        if(len(entry) != len(result)): #if all matches is not equal to the orginial value then bad characters where given.
            self.isValidEntry = False
            self.add_remove_error_label()
        else:
            self.isValidEntry = True
            self.add_remove_error_label()
        
        return True #Want to allow bad character with a popup error message returning false prevents typing character at all
    
    def do_login(self):
        #usernames are unique so search for the username entry
        sql = f"SELECT rowid, user_username, user_full_name, user_pass_salt, user_pass_hash FROM users WHERE user_username = '{self.username.get()}'"
        try:
            response = db.cursor.execute(sql)
            user_data = response.fetchone()
            if user_data is not None:
                #hash the given user password with the salt in the database
                password = self.password.get()
                salt = user_data[3]
                current_password_hash = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()
                #if given pass matches saved pass
                if user_data[4] == current_password_hash:
                    #set session variables
                    self.session.active_user_id = user_data[0]
                    self.session.active_username = user_data[1]
                    self.session.active_full_name = user_data[2]
                    #end the login gui
                    self.gui.destroy()
                    return True

            self.error_label_login.grid(column=1, row=5, columnspan=3)        
        except Exception as e:
            print(e)
            return False
    
class RegisterWindow(Window):

    def __init__(self):
        super().__init__("Register", "300x220")
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
        self.error_label = Label(self.mainframe, text="Only use a-z, A-Z, numbers 0-9\n or special characters: \n ._~()'!*:@,+?-", foreground="white", bg="red")


    def add_entries(self):
        Entry(self.mainframe, width=35, textvariable=self.name).grid(column=2, row=1, columnspan=1, sticky=(W))
        Entry(self.mainframe, width=35, textvariable=self.email).grid(column=2, row=3, columnspan=1, sticky=(W))
        Entry(self.mainframe, width=35, textvariable=self.username).grid(column=2, row=5, columnspan=1, sticky=(W))
        Entry(self.mainframe, width=35, textvariable=self.password).grid(column=2, row=7, columnspan=1, sticky=(W))

    def add_buttons(self):
        Button(self.mainframe, text="Register", command=self.process_form).grid(column=2, row=8, sticky=(N, E), pady=5)
        Button(self.mainframe, text="Cancel", command=self.window.destroy).grid(column=2, row=8, sticky=(N, E), pady=5, padx=60)
        
    def process_form(self):
        db = Db_Actions()
        valid = False
        form_data = [self.username.get(), self.name.get(), self.email.get()]

        for data in form_data:
            if not functions.check_regex(data):
                valid = False
                break
            else:
                valid = True
        
        if valid:
            password = functions.hash_and_salt(self.password.get())
            if password:
                form_data.append(password[0])
                form_data.append(password[1])
                db.one_step_insert('users', form_data)
                self.window.destroy()
        else:
            self.error_label.grid(column=1, columnspan=2, row=8, sticky=(W), pady=5)
            print("BAD Form Data")    
            
        

