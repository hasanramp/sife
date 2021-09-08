import openpyexcel as xl
from sql_handler import sql_handler
from __init__ import get_username_and_password
import time


def transfer_from_excel_to_mysql(file):
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