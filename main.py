from sql_handler import sql_handler
from password_manager import password_manager
import sys
import pyperclip
from pwd_gen_mysql import candidate_password_code
import json



function = sys.argv[1]

def get_dropbox_info():
    file = open('dropbox.json', 'r')
    dropbox_json = json.load(file)
    return dropbox_json['access_token'], dropbox_json['app_key'], dropbox_json['app_secret']


def verify_for_illegal_password(password):
    index = 0
    for p in password:
        if p == '"':
            if password[index + 1] == ',':
                password = password.replace(',', '|')
                return password, False
        index += 1

a_word = 'kdjf",fdk'

def get_username_and_password():
    username_password_file = open('UsernamePassword.json')
    username_password_json = json.load(username_password_file)
    return username_password_json['username'], username_password_json['password']

user, database_password = get_username_and_password()
database = 'passwords'

pm = password_manager(user, database_password, database)
sqh = sql_handler(user, database_password, database)
if function != 'show' and function != 'create_backup' and function != 'transfer_backup' and function != 'load_backup':
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
    if username == None:
        username = '#none'
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
            if username != '#none':
                password = username_password.split('|')[1].replace(' ', '')
            elif password[0] != 'candidate passwords':
                password = username_password.split('|')[0].replace('password: ', '')
            else:
                # password
                password = username_password.split('|')[1].replace('password: ', '')
            print(password)
            copy(password)
elif function == 'g':
    n_of_char = sys.argv[4]
    password = pm.generate(website, n_of_char, username)
    password, passed = verify_for_illegal_password(password)
    print(password)
    copy(password)

elif function == 'ep':
    try:
        password = sys.argv[4]
    except IndexError:
        password = sys.argv[3]
        word, passed = verify_for_illegal_password(password)
        if passed is False:
            print('This is an illegal password. Password cannot have \'"\' and \',\' next to each other try another password')
            exit()
        username = None
    print(pm.enter_password(website, password, username))
elif function == 'del':
    if username == None:
        username = '#none'
    elif website[0] == '@':
        website = website.replace('@', '')
        website = website + ' ' + username
        username = '#none'
    sqh.delete_password(website, username)

elif function == 'show':
    result = sqh.get_result()
    for r in result:
        website, password, username = r[0], r[1], r[2]
        print(f'website: {website}| password: {password}| username: {username}\n')

elif function == 'backup':
    from backup import Backup, Backup_hdn
    backup_file_format = sys.argv[3]
    cloud = False
    try:
        if sys.argv[4] == 'cloud':
            cloud = True
            access_token, app_key, app_secret = get_dropbox_info()
    except IndexError:
        pass
    if backup_file_format == 'excel':
        if cloud is True:
            backup = Backup(cloud=True, access_token=access_token, app_key=app_key, app_secret=app_secret)
        else:
            backup = Backup()
    elif backup_file_format == 'hdn':
        if cloud is True:
            backup = Backup_hdn(cloud=True, access_token=access_token, app_key=app_key, app_secret=app_secret)
        else:
            backup = Backup_hdn()
    else:
        print('choose a file format to create backup')
        print('pass the arguement after sub-function')
        print('file formats are:')
        print('excel **recommended**')
        print('hdn **choose this if u know what u are doing**')
    sub_function = sys.argv[2]
    
    if sub_function == 'create':
        backup.create_backup()
    elif sub_function == 'transfer':
        backup.transfer_backup()
    elif sub_function == 'load':
        backup.load_backup()
    elif sub_function == 'upload':
        if backup_file_format == 'excel':
            backup = Backup(cloud=True, access_token=access_token, app_key=app_key, app_secret=app_secret)
            backup.upload()
        elif backup_file_format == 'hdn':
            backup = Backup_hdn(cloud=True, access_token=access_token, app_key=app_key, app_secret=app_secret)
            backup.upload()
    else:
        print('invalid option for function backup')
        #print('type --help for more info')

