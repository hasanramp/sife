from sql_handler import sql_handler
from password_manager import password_manager
import sys
import pyperclip
from pwd_gen_mysql import candidate_password_code

function = sys.argv[1]

user = 'hasan'
database_password = 'Iloveubuntu1!'
database = 'passwords'

pm = password_manager(user, database_password, database)
sqh = sql_handler(user, database_password, database)
if function != 'show':
    website = sys.argv[2]
else:
    website = 'something'

if website == candidate_password_code:
    print('The website name is illegal to use in this application.')
    exit()

def copy(msg):
    pyperclip.copy(msg)

try:
    username = sys.argv[3]
except IndexError:
    username = None

if function == 'fp':
    password = pm.find_password(website, username)
    if type(password) != list:
        print(password)
        copy(password)
    else:
        index = 1
        try:
            passwords = password[1]
        except IndexError:
            passwords = password
            # copy(password)
            # exit()
        for p in passwords:
            print(f'[{str(index)}] ' + p)
            index += 1
        index_num = input('which password to copy?("n" to abort!): ')
        if index_num == 'n':
            exit()
        elif int(index_num) > index - 1:
            print('There is no suggestion with that index number!')
        else:
            index_num = int(index_num) - 1
            username_password = passwords[index_num]
            if username != None:
                password = username_password.split('|')[1].replace(' ', '')
            else:
                if password[0] != 'candidate passwords':
                    password = username_password.split('|')[0].replace('password: ', '')
                else:
                    password = username_password.split('|')[1].replace('password: ', '')
            print(password)
            copy(password)
elif function == 'g':
    n_of_char = sys.argv[4]
    print(n_of_char)
    password = pm.generate(website, n_of_char, username)
    print(password)
    copy(password)

elif function == 'ep':
    try:
        password = sys.argv[4]
    except IndexError:
        password = sys.argv[3]
        username = None
    print(pm.enter_password(website, password, username))
elif function == 'del':
    pass
    sqh.delete_password(website)

elif function == 'show':
    result = sqh.get_result()
    for r in result:
        website, password, username = r[0], r[1], r[2]
        print(f'website: {website}| password: {password}| username: {username}\n')

else:
    print('Invalid function!')