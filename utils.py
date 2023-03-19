import json
import pyperclip
import os
import subprocess

def set_dab_engine(new_engine):
    curr_dir = os.path.dirname(__file__)
    configuration_file = open(os.path.join(curr_dir, 'data/sife_configuration.json'), 'r')
    configuration_json = json.load(configuration_file)
    configuration_json['db_engine'] = new_engine
    configuration_file = open(os.path.join(curr_dir, 'data/sife_configuration.json'), 'w')

    json.dump(configuration_json, configuration_file)

def get_dropbox_info():
    curr_dir = os.path.dirname(__file__)
    file = open(os.path.join(curr_dir, 'data/dropbox.json'), 'r')
    dropbox_json = json.load(file)
    return dropbox_json['access_token'], dropbox_json['default_dir']


def verify_for_illegal_password(password):
    index = 0
    for p in password:
        if p == '"':
            if password[index + 1] == ',':
                password = password.replace(',', '|')
                return password, False
        index += 1
    return password, True

def get_username_and_password():
    curr_dir = os.path.dirname(__file__)
    username_password_file = open(os.path.join(curr_dir, 'data/UsernamePassword.json'), 'r')
    username_password_json = json.load(username_password_file)
    return username_password_json['username'], username_password_json['password']

def migrate(curr_engine):
    from db.sql_handler import sql_handler
    import db.sqlite3_handler
    from __init__ import get_username_and_password
    from cloud.backup import Backup_hdn
    user, pswd = get_username_and_password()
    curr_dir = os.path.dirname(__file__)
    if curr_engine == 'mysql':
        # print('old sqh', 'sqlite3')
        # exit()
        old_sqh = sql_handler(user, pswd, 'passwords')
        # old_sqh = db.sqlite3_handler.sql_handler('db/passwords.db')
    else:
        # print('old sqh', 'mysql')
        # exit()
        # old_sqh = sql_handler(user, pswd, 'passwords')
        print('reached here')
        old_sqh = db.sqlite3_handler.sql_handler(os.path.join(curr_dir, 'data/passwords.db'))

    backup = Backup_hdn()
    all_data = old_sqh.get_result()
    backup.load_backup(rows=all_data)

def transfer_from_excel_to_mysql(file):
    import openpyexcel as xl
    from db.sql_handler import sql_handler
    from __init__ import get_username_and_password
    import time
    user, pswd = get_username_and_password()
    sqh = sql_handler(user, pswd, database='passwords')
    wb = xl.load_workbook(file)
    sheet = wb['Sheet1']

    for row in range(1, sheet.max_row + 1):
        website_cell = sheet.cell(row, 1).value
        password_cell = sheet.cell(row, 2).value
        username_cell = sheet.cell(row, 3).value
        print(website_cell, password_cell, username_cell)
        if website_cell != None:
            sqh.insert_password(website_cell, password_cell, username_cell)
            time.sleep(0.5)

def transfer_from_excel_to_sqlite3(file):
    import openpyexcel as xl
    from db.sqlite3_handler import sql_handler
    from __init__ import get_username_and_password
    import time
    user, pswd = get_username_and_password()
    curr_dir = os.path.dirname(__file__)
    sqh = sql_handler(database='data/passwords.db')
    wb = xl.load_workbook(file)
    sheet = wb['Sheet1']

    for row in range(1, sheet.max_row + 1):
        website_cell = sheet.cell(row, 1).value
        password_cell = sheet.cell(row, 2).value
        username_cell = sheet.cell(row, 3).value
        print(website_cell, password_cell, username_cell)
        if website_cell != None:
            sqh.insert_password(website_cell, password_cell, username_cell)
            time.sleep(0.5)

def compress_file(file, comp_format):
    if comp_format == 'gz':
        import gzip
        compressed_filename = file + '.gz'
        file = open(file, 'rb')
        compressed_file = gzip.open(compressed_filename, 'wb')
        compressed_file.writelines(file)
        return compressed_filename
    elif comp_format == 'zip':
        from zipfile import ZipFile
        with ZipFile(file + '.zip', 'w') as f_out:
            f_out.write(file)
        return file + '.zip'
    else:
        print('this file format for compression is not supported')

def decompress_file(file, comp_format):
    if comp_format == 'gz':
        import gzip
        import shutil
        with gzip.open(file, 'rb') as f_in:
            with open(file.replace('.gz', ''), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    elif comp_format == 'zip':
        from zipfile import ZipFile
        with ZipFile(file, 'r') as zf:
            zf.extract(file.replace('.zip', ''))
    else:
        print('this file format for compression is not supported')

def copy(msg):
    if os.getenv('XDG_SESSION_TYPE') == 'wayland':
        subprocess.run(["wl-copy", msg])
        return
    pyperclip.copy(msg)
