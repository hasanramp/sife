import openpyexcel as xl
from password_manager import password_manager

pm = password_manager('hasan', 'Iloveubuntu1!', 'passwords')
wb = xl.load_workbook('/home/kevin/password_database 1.xlsx')
sheet = wb['Sheet1']

for row in range(1, sheet.max_row + 1):
    website_cell = sheet.cell(row, 1).value
    password_cell = sheet.cell(row, 2).value
    username_cell = sheet.cell(row, 3).value
    print(website_cell, password_cell, username_cell)
    if website_cell != None:
        pm.enter_password(website_cell, password_cell, username_cell)

