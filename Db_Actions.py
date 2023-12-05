import sqlite3
from BasicFunctions import BasicFunctions as f


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


    
        



        