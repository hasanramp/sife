import openpyexcel as xl
from password_managing_app.sql_handler import sql_handler
from __init__ import get_username_and_password
from transfer_info import transfer_from_excel_to_mysql
import time
from hdn import Parser
from password_managing_app.cloud import CloudStorageHandler

class Backup:
    def __init__(self, cloud=False, access_token=None, app_key=None, app_secret=None):
        self.username, self.password = get_username_and_password()
        self.sqh = sql_handler(self.username, self.password, database='passwords')
        self.csh = CloudStorageHandler(access_token, app_key, app_secret)
        self.cloud = cloud
    def create_backup(self):
        backup_file = '/home/kevin/password_backup.xlsx'
        if self.cloud is False:
            
            
            result = self.sqh.get_result()
            index = 1
            wb = xl.load_workbook(backup_file)
            sheet = wb['Sheet1']
            for r in result:
                website_data = r[0]
                password_data = r[1]
                username_data = r[2]
                website_cell = sheet.cell(index, 1)
                password_cell = sheet.cell(index, 2)
                username_cell = sheet.cell(index, 3)
                website_cell.value = website_data
                password_cell.value = password_data
                username_cell.value = username_data
                index += 1
            wb.save(backup_file)
        else:
            self.csh.update(backup_file)

    def transfer_backup(self):
        to_transfer_from = 'password_backup.xlsx'
        to_transfer = '/media/kevin/Windows/Users/Kevin/py_projects/pma-windows/password_backup.xlsx'

        to_transfer_from_file = open(to_transfer_from, 'rb')
        to_transfer_file = open(to_transfer, 'wb')
        data = to_transfer_from_file.read()
        to_transfer_file.write(data)

    def load_backup(self):
        to_transfer_from = '/media/kevin/Windows/Users/Kevin/py_projects/pma-windows/password_backup.xlsx'
        if self.cloud is True:
            self.csh.download('backup.xlsx')
            to_transfer_from = 'backup.xlsx'
        
        print('[DELETING INFO TABLE OF EXISTING DATABASE]......')
        self.sqh.execute('DELETE FROM passwords;')
        self.sqh.commit()
        time.sleep(5)
        print('[WRITING INTO DATABASE]....')
        transfer_from_excel_to_mysql(to_transfer_from)
        
    def upload(self):
        self.csh.upload('backup.xlsx')

class Backup_hdn:
    def __init__(self, cloud=False, access_token=None, app_key=None, app_secret=None):
        self.username, self.password = get_username_and_password()
        self.sqh = sql_handler(self.username, self.password, database='passwords')
        self.hdn_parser = Parser()
        self.csh = CloudStorageHandler(access_token, app_key, app_secret)
        self.cloud = cloud
    def create_backup(self):
        if self.cloud is False:
            lines = self.sqh.get_result()
            hdn_parser = self.hdn_parser
            hdn_str = hdn_parser.write_in_hdn(lines)
            hdn_parser.dump(hdn_str, 'backup.hdn')
        else:
            self.csh.update('backup.hdn')
    def load_backup(self, file='backup.hdn'):
        if self.cloud is True:
            self.csh.download('backup.hdn')
            file = 'backup.hdn'
        rows = self.hdn_parser.parse(file)
        print('[DELETING INFO TABLE OF EXISTING DATABASE]......')
        self.sqh.execute('DELETE FROM passwords;')
        self.sqh.commit()
        print('[LOADING INFO IN DATABASE].....')
        for row in rows:
            website = row[0]
            password = row[1]
            username = row[2]
            self.sqh.insert_password(website, password, username)
        print('Done!')
    
    def upload(self):
        self.csh.upload('backup.hdn')
# media/kevin/Windows/Users/Kevin/py_projects/pma-windows