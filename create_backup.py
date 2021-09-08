import openpyexcel as xl
from password_managing_app.sql_handler import sql_handler
from __init__ import get_username_and_password
from transfer_info import transfer_from_excel_to_mysql
import time

username, password = get_username_and_password()
sqh = sql_handler(username, password, database='passwords')
def create_backup():
    backup_file = 'password_backup.xlsx'
    
    result = sqh.get_result()
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

def transfer_backup():
    to_transfer_from = 'password_backup.xlsx'
    to_transfer = '/media/kevin/Windows/Users/Kevin/py_projects/pma-windows/password_backup.xlsx'

    to_transfer_from_file = open(to_transfer_from, 'rb')
    to_transfer_file = open(to_transfer, 'wb')
    data = to_transfer_from_file.read()
    to_transfer_file.write(data)

def load_backup():
    to_transfer_from = '/media/kevin/Windows/Users/Kevin/py_projects/pma-windows/password_backup.xlsx'
    print('[DELETING INFO TABLE OF EXISTING DATABASE]......')
    sqh.execute('DELETE FROM passwords;')
    sqh.commit()
    time.sleep(5)
    print('[WRITING INTO DATABASE]....')
    transfer_from_excel_to_mysql(to_transfer_from)

# media/kevin/Windows/Users/Kevin/py_projects/pma-windows

