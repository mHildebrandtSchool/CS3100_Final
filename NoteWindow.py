from tkinter import *
from Window import Window
from BasicFunctions import BasicFunctions



f = BasicFunctions()

class NoteWindow(Window):

    def __init__(self, window_title, row_list, session, action, queue, selected_row = None):
        super().__init__(window_title, "300x200",)
        self.new_name = StringVar()
        self.new_password = StringVar()
        self.row_list = row_list
        self.session = session
        self.action = action
        self.selected_row = selected_row
        self.row_index = (int(self.selected_row.get()) - 1) if self.selected_row else None
        self.save_queue = queue

        self.action_button = Button(self.mainframe)
        self.cancel_button = Button(self.mainframe, text='Cancel', command=self.close_window)

        self.the_text = Text(self.mainframe, width=35, height=5, )
    
    def build_window(self):
        current_state = NORMAL
        if self.action == 'delete':
            self.fill_entries()
            current_state = DISABLED
        elif self.action == 'modify':
            self.fill_entries()

        Label(self.mainframe, text="Site Name: ").grid(column=0, row=0, sticky=(E))
        Entry(self.mainframe, textvariable=self.new_name, width=35, state=current_state).grid(column=1, columnspan=2, row=0, sticky=(E))

        Label(self.mainframe, text="Notes: ").grid(column=0, row=2, sticky=(W))
        self.the_text.grid(column=0,columnspan=3, row=3, sticky=(E))
        self.the_text.config(state=current_state)

        Label(self.mainframe, text="Password: ").grid(column=0, row=4, sticky=(W))
        Entry(self.mainframe, textvariable=self.new_password, width=35, 
              state=current_state).grid(column=1, columnspan=2, row=4, pady=5, sticky=(E))

        self.cancel_button.grid(column=2, row=5, sticky=(W))
        self.add_action_button()

        if self.action == 'add':
            self.cancel_button.grid(column=2, row=5, sticky=(N))
        else:
            self.cancel_button.grid(column=2, row=5, padx=25, sticky=(W))

        if self.selected_row is not None:
            Label(self.mainframe, 
                  text=f"Currently working on Row: #{self.selected_row.get()}").grid(column=0, row = 5, columnspan=2, sticky=(N, S, W))

    def add_action_button(self):
        if self.action == 'add':
            self.action_button.config(text=self.action.capitalize(), command=self.add_data)
        elif self.action == 'delete':
            self.action_button.config(text=self.action.capitalize(), command=self.delete_data)
        elif self.action == 'modify':
            self.action_button.config(text=self.action.capitalize(), command=self.modify_data)
        self.action_button.grid(column=2, row=5, sticky=(N, E))


    def fill_entries(self):
        #search linked list for selected row data. Linked list will always be in order of rows
        #selected_row is a str index starting 1 change to int index starting 0 for search
        entry_data = self.row_list.search_index(self.row_index).data
        self.new_password.set(value=entry_data['note_password'])
        self.new_name.set(value=entry_data['note_site_name'])
        self.the_text.insert('1.0', entry_data['note_text'])
        return True

    def close_window(self):
        self.window.destroy()

    def add_data(self):
        new_node = f.create_row_node(None, self.the_text.get('1.0', 'end'), self.new_password.get(), self.new_name.get(),
                                     f.get_now_time(), f.get_now_time(), self.row_list.length + 1)
        self.row_list.append(new_node)
        #Queue SQL Statment for adding new row
        sql = f"""INSERT INTO notes 
                VALUES(NULL, {self.session.active_user_id}, 
                '{self.the_text.get('1.0', 'end').strip()}', 
                '{self.new_password.get()}', 
                '{self.new_name.get()}', 
                '{f.get_now_time()}', 
                '{f.get_now_time()}')"""
        self.save_queue.enqueue(sql)
        self.session.main_gui.refresh_table()
        self.window.destroy()
    
    def delete_data(self):
        deleted_note_id = self.row_list.delete(self.row_index)
        #Queue SQL Statment for deleting a row
        sql = f"DELETE FROM notes WHERE note_id = {deleted_note_id}"
        self.save_queue.enqueue(sql)
        self.session.main_gui.refresh_table()
        self.window.destroy()

    def modify_data(self):
        row_data = self.row_list.search_index(self.row_index)
        row_data.data['note_text'] = self.the_text.get('1.0', 'end')
        row_data.data['note_password'] = self.new_password.get()
        row_data.data['note_site_name'] = self.new_name.get()
        row_data.data['note_last_mod_date'] = f.get_now_time()
        #Queue SQL Statment for updating a row
        sql = f"""UPDATE notes
                 SET
                 note_text = '{self.the_text.get('1.0', 'end')}',
                 note_password = '{self.new_password.get()}',
                 note_site_name = '{self.new_name.get()}',
                 note_last_mod_date = '{f.get_now_time()}'
                 WHERE note_id = {row_data.data['note_id']}
                """
        self.save_queue.enqueue(sql)
        self.session.main_gui.refresh_table()
        self.window.destroy()
