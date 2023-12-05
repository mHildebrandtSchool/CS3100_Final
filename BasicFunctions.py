import re
#Salt and hash requirments idea from: https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
import hashlib, uuid


class BasicFunctions():
        
    def check_regex(entry):
        #validate the value to make sure it is only A-Z, a-z, or has the special chars ., !, @, #, $, @ if other characters such as ^*() or ; appear then it will fail
        pattern = re.compile("[A-Za-z0-9\s._~()'!*:@,+?-]") #set regex
        result = pattern.findall(entry) #find all matches to the regex
        test = len(entry)
        if(len(entry) != len(result)): #if all matches is not equal to the orginial value then bad characters where given.
            return False
        else:
            return True
        
    def hash_and_salt(password, salt = None):
        if salt is None:
            salt = uuid.uuid4().hex
        
        if BasicFunctions.check_regex(password):
            salty_hash = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()
            return (salt, salty_hash)
        else:
            return False
        
    def print_shit(a, b):
        print(a, b)