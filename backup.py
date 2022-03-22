from utils import compress_file
import openpyexcel as xl
# from password_managing_app.sql_handler import sql_handler
from __init__ import get_username_and_password
from utils import transfer_from_excel_to_mysql
import time
from hdn import Parser
from cloud.cloud import CloudStorageHandler
import shutil
from __init__ import get_db_engine

class Backup:
    def __init__(self, compressed=False, cloud=False, access_token=None):
        # self.username, self.password = get_username_and_password()
        self.compressed = compressed
        db_engine = get_db_engine()
        self.db_engine = db_engine
        if db_engine == 'sqlite3':
            from db.sqlite3_handler import sql_handler
            self.sqh = sql_handler(database='data/passwords.db')
        else:
            from db.sql_handler import sql_handler
            user, password = get_username_and_password()
            self.sqh = sql_handler(user, password, 'passwords')
        self.cloud = cloud
        if self.cloud is True:
            self.csh = CloudStorageHandler(access_token)
        
    def create_backup(self, default_dir=''):
        backup_file = 'data/password_backup.xlsx'
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
            if self.compressed:
                compressed_backup_filename = compress_file(backup_file)
                return
        else:
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
            if self.compressed:
                compressed_backup_filename = compress_file(backup_file)
                self.csh.update(compressed_backup_filename, dir=default_dir)
                return
            self.csh.update(backup_file, dir=default_dir)

    def transfer_backup(self):
        to_transfer_from = 'data/password_backup.xlsx'
        to_transfer = '/media/kevin/Windows/Users/Kevin/py_projects/pma-windows/password_backup.xlsx'

        to_transfer_from_file = open(to_transfer_from, 'rb')
        to_transfer_file = open(to_transfer, 'wb')
        data = to_transfer_from_file.read()
        to_transfer_file.write(data)

    def load_backup(self, default_dir=''):
        to_transfer_from = '/usr/share/sife/data/password_backup.xlsx'
        if self.cloud is True:
            if self.compressed:
                self.csh.download('data/password_backup.xlsx.gz', dir=default_dir)
                from utils import decompress_file
                decompress_file('data/password_backup.xlsx.gz')
                to_transfer_from = 'data/password_backup.xlsx'
            else:
                self.csh.download('data/password_backup.xlsx', dir=default_dir)
                to_transfer_from = 'data/password_backup.xlsx'
        
        print('[DELETING INFO TABLE OF EXISTING DATABASE]......')
        self.sqh.execute('DELETE FROM passwords;')
        self.sqh.commit()
        time.sleep(5)
        print('[WRITING INTO DATABASE]....')
        if self.db_engine == 'mysql':
            from utils import transfer_from_excel_to_mysql
            transfer_from_excel_to_mysql(to_transfer_from)
        else:
            from utils import transfer_from_excel_to_sqlite3
            transfer_from_excel_to_sqlite3(to_transfer_from)
        
    def upload(self, default_dir=''):
        self.csh.upload('password_backup.xlsx', dir=default_dir)

class Backup_hdn:
    def __init__(self, compressed=False, cloud=False, access_token=None):
        # self.username, self.password = get_username_and_password()
        self.compressed = compressed
        db_engine = get_db_engine()
        if db_engine == 'sqlite3':
            from db.sqlite3_handler import sql_handler
            self.sqh = sql_handler(database='data/passwords.db')
        else:
            from db.sql_handler import sql_handler
            user, password = get_username_and_password()
            self.sqh = sql_handler(user, password, 'passwords')
        self.hdn_parser = Parser('data/backup.hdn')
        self.cloud = cloud
        self.file = 'data/backup.hdn'
        if self.cloud is True:
            self.csh = CloudStorageHandler(access_token)
        
    def create_backup(self, default_dir=''):
        if self.cloud is False:
            lines = self.sqh.get_result()
            hdn_parser = self.hdn_parser
            hdn_str = hdn_parser.write_in_hdn(lines)
            hdn_parser.dump(hdn_str, 'data/backup.hdn')
            if self.compressed:
                compressed_backup_filename = compress_file('data/backup.hdn')
                return
        else:
            lines = self.sqh.get_result()
            hdn_parser = self.hdn_parser
            hdn_str = hdn_parser.write_in_hdn(lines)
            hdn_parser.dump(hdn_str, 'data/backup.hdn')
            self.csh.update('data/backup.hdn', dir=default_dir)
            if self.compressed:
                compressed_backup_filename = compress_file('data/backup.hdn')
                self.csh.update(compressed_backup_filename, dir=default_dir)
                return
            self.csh.update('data/backup.hdn', dir=default_dir)
    def load_backup(self, file='data/backup.hdn', default_dir='', rows=None):
        if self.cloud is True:
            if self.compressed:
                self.csh.download(file + '.gz', dir=default_dir)
                from utils import decompress_file
                decompress_file('data/password_backup.xlsx.gz')
            else:
                self.csh.download(file, dir=default_dir)
            # self.csh.download(file, dir=default_dir)
            shutil.move(file, self.file)
        
        if rows is None:
            rows = self.hdn_parser.parse()
        
        print('[DELETING INFO TABLE OF EXISTING DATABASE]......')
        self.sqh.delete_table()
        self.sqh.commit()
        print('[LOADING INFO IN DATABASE].....')
        for row in rows:
            website = row[0]
            password = row[1]
            username = row[2]
            self.sqh.insert_password(website, password, username)
        print('Done!')
    
    def upload(self, file, default_dir=''):
        print('reached here')
        self.csh.upload(file, dir=default_dir)

class BackupSqlite(Backup_hdn):
    def __init__(self, cloud=False, access_token=None):
        Backup_hdn.__init__(self, cloud, access_token)
        self.file = 'data/passwords.db'

    def create_backup(self, default_dir=''):
        file_exists = self.check_if_file_exists()
        if file_exists:
            self.csh.update(self.file, dir=default_dir)
        else:
            self.upload(file='passwords.db', default_dir=default_dir)

    def load_backup(self, file='passwords.db', default_dir=''):
        self.csh.download(file, dir=default_dir)
        shutil.move(file, self.file)

    def check_if_file_exists(self):
        try:
            dbx.files_get_metadata('/passwords/passwords.db')
            return True
        except:
            return False

# media/kevin/Windows/Users/Kevin/py_projects/pma-windows
