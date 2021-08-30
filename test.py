from sql_handler import sql_handler

sqh = sql_handler('hasan', 'Iloveubuntu1!', 'passwords')
print(sqh.execute('SELECT password FROM passwords WHERE website = "amazon" AND username = "hasan"')[0][0])