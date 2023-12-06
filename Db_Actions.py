import sqlite3



class Db_Actions():

    def __init__(self):
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()

    #def insert_user(self, username, full_name, email, pass_hash):
    #    sql = "INSERT INTO users VALUES(null, "
    #    if(f.check_regex(str(username.get()))):
    #        sql += f"'{username.get()}',"
    #    if(f.check_regex(full_name.get())):
    #        sql += f"'{full_name.get()}',"
    #    if(f.check_regex(email.get())):
    #        sql += f"'{email.get()}',"
    #    if(f.check_regex(pass_hash.get())):
    #        sql += f"'{pass_hash.get()}')"
    #    self.db.execute(sql)
    #    return self.connection.commit()

    def one_step_insert(self, table, values):
        sql = f"INSERT INTO {table} VALUES(null, "
        for key, value in enumerate(values):
            if len(values) - 1 == key:
                sql += f"'{value}')"
            else:
                sql += f"'{value}',"

        self.cursor.execute(sql)
        self.connection.commit()

    def get_tabel_data(self, active_user_id = 1):
        sql = f"""SELECT
                    note_id, 
                    note_text, 
                    note_password, 
                    note_site_name, 
                    note_last_mod_date, 
                    note_create_date 
                    FROM notes 
                    WHERE fk_user_id = {active_user_id}"""
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data
    
    def queue_to_db(self, save_queue):
        while save_queue.list.head is not None:
            sql = save_queue.dequeue()
            self.cursor.execute(sql)
            self.connection.commit()


    
        



        