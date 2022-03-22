import sys
from password_manager import password_manager
from __init__ import get_db_engine
import os
from utils import copy
import subprocess
# from escape_quotes import escape_special_char

def escape_special_char(word):
    special_char = ['$', '!', '"']
    index = 0
    times = 0
    for x in word:
        if x in special_char:
            word = word[0:index] + '\\' + word[index:]
            index += 1
        index +=1
    
    return word

function = sys.argv[1]
db_engine = get_db_engine()

if db_engine == 'sqlite3':
    from db.sqlite3_handler import sql_handler
    pm = password_manager('data/passwords.db')
    sqh = sql_handler('data/passwords.db')
else:
    from db.sql_handler import sql_handler
    pm = password_manager('passwords')
    user, password = get_username_and_password()
    sqh = sql_handler(user, password, 'passwords')

if function == 'fn-pwd':
    import re
    website = sys.argv[2]
    try:
        username = sys.argv[3]
    except IndexError:
        username = 'NULL'
    if username == None or username == '':
        username = 'NULL'
    password = pm.find_password(website, username)
    if type(password) != list and type(password) != dict:
        # password = escape_special_char(password)
        print(password)
        os.system(f'echo {password} | rofi -dmenu -config ~/.config/rofi/themes/dt-center.rasi')
        copy(password)
    elif type(password) == list:
        dmenu_str = ''
        for item in password:
            website, password, username = item
            dmenu_str += f'website: {website} | password: {password} | username: {username} \n'
        
        # dmenu_str = escape_special_char(dmenu_str)
        process = subprocess.Popen(f'echo "{dmenu_str}" | rofi -l {len(password)} -p "select password to copy" -config ~/.config/rofi/themes/dt-center.rasi', shell=True, stdout=subprocess.PIPE)
        output = process.stdout.read().decode()
        password = output.split('|')[1]
        password = password[1:-1].split(':')[1]
        password = password[1:]
        copy(password)

    elif type(password) == dict:
        import operator
        sorted_d = dict( sorted(password.items(), key=operator.itemgetter(1),reverse=True))
        matched_arr = []
        index = 1
        website_length = len(website)
        dmenu_str = ''
        for keys in sorted_d:
            matches = sorted_d[keys]
            if matches >= website_length:
                website, password_, username = keys
                dmenu_str += f'website: {website} | password: {password_} | username: {username} \n'
        
        # dmenu_str = escape_special_char(dmenu_str)
        process = subprocess.Popen(f'echo "{dmenu_str}" | rofi -dmenu -l {len(password)} -p "select password to copy" -config ~/.config/rofi/themes/dt-center.rasi', shell=True, stdout=subprocess.PIPE)
        output = process.stdout.read().decode()
        password = output.split('|')[1]
        password = password[1:-1].split(':')[1]
        password = password[1:]
        copy(password)

elif function == 'en-pwd':
    website = sys.argv[2]
    password = sys.argv[3]
    try:
        username = sys.argv[4]
    except IndexError:
        username = 'NULL'
    if username == None or username == '':
        username = 'NULL'
    
    result = pm.enter_password(website, password, username)
    if result != None:
        result = result[5:-4]
        os.system(f'echo "{result}" | rofi -dmenu -l 1 -config ~/.config/rofi/themes/dt-center.rasi')

elif function == 'delete':
    website = sys.argv[2]
    try:
        username = sys.argv[3]
    except IndexError:
        username = 'NULL'

    if username == '' or username is None:
        username = 'NULL'
    elif website[0] == '@':
        website = website.replace('@', '')
        website = website + ' ' + username
        username = 'NULL'
    sqh.delete_password(website, username)

elif function == 'show':
    import re
    result = sqh.get_result()
    index = 0
    dmenu_str = ''
    for r in result:
        website, password, username = r[0], r[1], r[2]
        dmenu_str += f'website: {website} | password: {password} | username: {username}\n'
        index += 1
        if index % 20 == 0:
            # dmenu_str = escape_special_char(dmenu_str)
            process = subprocess.Popen(f'echo "{dmenu_str}" | rofi -dmenu -l {len(result)} -p "select password to copy" -config ~/.config/rofi/themes/dt-center.rasi', shell=True, stdout=subprocess.PIPE)
            output = process.stdout.read().decode()
            # print('start' + output + 'end')
            # exit()
            if output == '\n':
                dmenu_str = ''
            else:
                break

    password = output.split('|')[1]
    password = password[1:-1].split(':')[1]
    password = password[1:]
    copy(password)

elif function == 'set-db-engine':
    curr_db_engine = db_engine
    new_db_engine = sys.argv[1]
    if curr_db_engine != new_db_engine:
        allow_changing_engine = subprocess.Popen(f"""
        echo \"""warning: you are about to change your database engine.
        The new database will not have your existing password information updated.
        Migrate information from previous db to new? (m to proceed with migration).
        proceed without migrating? (Y to proceed. any other to abort)\""" | rofi -dmenu -l 4 -p "continue? -config ~/.config/rofi/themes/dt-center.rasi"
        """, shell=True, stdout=subprocess.PIPE)
        # allow_changing_engine = subprocess.Popen(f'printf "warning: You are about to change your db engine. new db engine will not have existing information. (enter m to proceed with migration, Y to proceed and n to abort)"')
        if allow_changing_engine == 'm':
            print(new_db_engine)
            set_dab_engine(new_db_engine)
            from utils import migrate
            migrate(curr_db_engine)
        elif allow_changing_engine == 'Y':
            set_dab_engine(new_db_engine)
        
elif function == 'connect':
    os.system('echo "connect can only be used on cli" | rofi -dmenu -config ~/.config/rofi/themes/dt-center.rasi')
    print('connect can only be used on cli!')