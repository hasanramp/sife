import random2 as r

class password_gen:
    def __init__(self):
        pass
    
    def generate(self, n_of_char):
        char_str = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
        char_sp = '!@#$%^&*()[]{},./<>?;:"\''
        char_num = '1234567890'
        pswd = ''
        for x in range(0, (int(n_of_char) - 2)):
            pswd += r.choice(char_str)
        pswd = pswd + r.choice(char_sp) + r.choice(char_num)
        
        return pswd
    
    