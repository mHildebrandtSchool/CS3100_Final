import re
#Salt and hash requirments idea from: https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
import hashlib, uuid
from Node import Node
from datetime import date


class BasicFunctions():
        
    def check_regex(self, entry):
        #validate the value to make sure it is only A-Z, a-z, or has the special chars ., !, @, #, $, @ if other characters such as ^*() or ; appear then it will fail
        pattern = re.compile("[A-Za-z0-9\s._~()'!*:@,+?-]") #set regex
        result = pattern.findall(entry) #find all matches to the regex
        test = len(entry)
        if(len(entry) != len(result)): #if all matches is not equal to the orginial value then bad characters where given.
            return False
        else:
            return True
        
    def hash_and_salt(self, password, salt = None):
        if salt is None:
            salt = uuid.uuid4().hex
        
        if self.check_regex(password):
            salty_hash = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()
            return (salt, salty_hash)
        else:
            return False

    def create_row_node(self, note_id, note_text, note_password, site_name, last_mod, create_date, row_id):
        row_dict = {
            'note_id': note_id,
            'note_row_id': str(row_id),
            'note_text': note_text,
            'note_password': note_password,
            'note_site_name': site_name,
            'note_last_mod_date': last_mod,
            'note_creation_date': create_date,
        }
        new_node = Node(row_dict)
        return new_node
    
    def num_rows_list(self, num_rows):
        row_nums = []
        for row_num in range(1, num_rows + 1):
            row_num_str = str(row_num)
            row_nums.append(row_num_str)
        return tuple(row_nums)
    
    def get_now_time(self):
        current_date = date.today()
        current_date.isoformat()
        return current_date.strftime("%m/%d/%y")
