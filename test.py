from sql_handler import sql_handler

sqh = sql_handler('hasan', 'Iloveubuntu1!', 'passwords')
result = sqh.get_result()
for r in result:
    website, password, username = r[0], r[1], r[2]
    print(f'website: {website}| password: {password}| username: {username}\n')