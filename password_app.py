from os import replace
from re import T
import openpyexcel as xl
import random2 as r
import pyperclip
import sys

class password_generator:
    def __init__(self, file):
        self.file = file
        self.wb = xl.load_workbook(file)
        self.sheet = self.wb['Sheet1']
    def save_file(self):
        self.wb.save(self.file)
    def generate_pswd(self, n_of_char, website_name):
        char_str = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
        char_sp = '!@#$%^&*()[]{}|,./<>?;:"\''
        char_num = '1234567890'
        pswd = ''
        for x in range(0, (n_of_char - 2)):
            pswd += r.choice(char_str)
        pswd = pswd + r.choice(char_sp) + r.choice(char_num)
        # seeing if user wants to replace existing website
        
        if website_name[0] == '!':
            replace_web = True
            website_name = website_name.replace('!', '')
        else:
            replace_web = False
        for row in range(1, self.sheet.max_row + 2):
            web_cell = self.sheet.cell(row, 1).value
            if web_cell == website_name and replace_web == True:
                self.sheet.cell(row, 2).value = pswd
                self.wb.save(self.file)
                return pswd
            elif web_cell == website_name and replace_web == False:
                return 'website already exists in the database. If you want to replace website type "!(wesite name)"'
                
             
            elif web_cell == None:
                
                # this is the web_cell. The cell value wasn't changing if i used the variable name
                # instead of actual value of the variable for some reason so i used the value.
                self.sheet.cell(row, 1).value = website_name
                # This is the password cell in the spreadsheet
                self.sheet.cell(row, 2).value = pswd
                break
            else:
                pass
        self.wb.save(self.file)
        return pswd
    def find_password(self, website_name):
        for row in range(1, self.sheet.max_row + 1):
            web_cell = self.sheet.cell(row, 1).value
            pswd_cell = self.sheet.cell(row, 2).value
            if web_cell == website_name:
                return pswd_cell
    def enter_password(self, website_name, password):
        # seeing if user wants to replace existing website
        if website_name[0] == '!':
            replace_web = True
            website_name = website_name.replace('!', '')
        else:
            replace_web = False
        for row in range(1, self.sheet.max_row + 2):
            web_cell = self.sheet.cell(row, 1).value
            pswd_cell = self.sheet.cell(row, 2).value
            if web_cell == website_name and replace_web == True:
                self.sheet.cell(row, 2).value = password
                self.wb.save(self.file)
                pass
            elif web_cell ==  website_name and replace_web == False:
                 return 'The password wasn\'t entered. website already exists in the database. If you want to replace website type "!(wesite name)"'
            elif web_cell == None:
                self.sheet.cell(row, 1).value = website_name
                self.sheet.cell(row, 2).value = password
                break
            else:
                pass
        self.wb.save(self.file)   
    def get_all_websites(self):
        websites_list = []
        for row in range(1, self.sheet.max_row):
            website = self.sheet.cell(row, 1).value
            websites_list.append(website)
        return websites_list

