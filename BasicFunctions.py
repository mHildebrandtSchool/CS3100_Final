import re



class BasicFunctions():
    
    def check_regex(entry):
        #validate the value to make sure it is only A-Z, a-z, or has the special chars ., !, @, #, $, @ if other characters such as ^*() or ; appear then it will fail
        pattern = re.compile("[A-Za-z0-9._~()'!*:@,;+?-]") #set regex
        result = pattern.findall(entry) #find all matches to the regex
        if(len(entry) != len(result)): #if all matches is not equal to the orginial value then bad characters where given.
            return False
        else:
            return True