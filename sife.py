import os
import platform

# if platform.system() == 'Linux':
#     if os.getuid() == 0:
#         pass
#     else:
#         print("You don't have the permission to execute this command. Are you root?")
#         exit()

file_dir = os.path.abspath(__file__)
if platform.system() == 'Linux':
	parent_dir_list = file_dir.split('/')
else:
	parent_dir_list = file_dir.split('\\')
parent_dir_list.remove('')
parent_dir_list.remove(parent_dir_list[-1])

if platform.system() == 'Linux':
	parent_dir = '/'.join(parent_dir_list)
	parent_dir = '/' + parent_dir

os.chdir(parent_dir)

from password_manager import password_manager
import sys
from __init__ import candidate_password_code
import json
from termcolor import colored
import time
from __init__ import get_db_engine
import click
from utils import get_dropbox_info, get_username_and_password, copy
import getpass

init_time = time.time()

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

def create_empty_mysql_config_file():
    destination = os.path.join(os.path.dirname(__file__), 'data/UsernamePassword.json')
    if os.path.isfile(destination):
        return
    file_str = '{ "username":"", "password":""}'
    with open(destination, 'w') as f:
        f.write(file_str)

    return 1

def evaluate_if_prompt_is_asked(prompt):
    if prompt == 'PROMPT':
        password = getpass.getpass('Password: ')
        return password
    
    return prompt

@click.group()
def cli():
    pass

@cli.command()
@click.argument('website')
@click.option('-u', type=str, default=None)
def fn_pwd(website, u):
    username = u
    import pyperclip
    if username == None:
        username = 'NULL'
    password = pm.find_password(website, username)
    find_password_time = time.time() - init_time
    find_password_time_colored = colored(find_password_time, 'magenta')
    if type(password) != list and type(password) != dict:
        with open('password.txt', 'w') as f:
            f.write(password)
        copy(password)
        password = colored(password, 'blue')
        print(password)
        find_password_time = time.time() - init_time
        find_password_time_colored = colored(find_password_time, 'magenta')
    #    print('time taken: ' + find_password_time_colored)
    else:
        if type(password) == list:
            index = 1
            for p in password:
                website = p[0]
                password_ = p[1]
                username = p[2]
                print(f'[{str(index)}] website: {website} | password: {password_} | username: {username}')
                index += 1
            index_num = input('which password to copy?("n" to abort!): ')
            if index_num == 'n':
                exit()
            try:
                index_num = int(index_num)
            except ValueError:
                print('Invalid response for Index number')
                print('no password was copied')
                print('Aborting!')
                exit()
            if index_num > index - 1:
                print('there is no suggestion with that number')
                exit()
            else:
                index_num = int(index_num) - 1
                # print(password)
                # exit()
                website, password, username = password[index_num]
                
                print(f'website: {website}, password: {password}, username: {username}')
                copy(password)
                with open('password.txt', 'w') as f:
                    f.write(password)
        else:
            import operator
            sorted_d = dict( sorted(password.items(), key=operator.itemgetter(1),reverse=True))
            matched_arr = []
            index = 1
            website_length = len(website)
            for keys in sorted_d:
                matches = sorted_d[keys]
                if matches >= website_length and len(keys[0]) <= len(website) * 3:
                    website, password_, username = keys
                    print(f'[{str(index)}] website: {website} | password: {password_} | username: {username} | {matches}')
                    matched_arr.append([website, password_, username])
                    index += 1
            
            index_num = input('which password to copy?("n" to abort!): ')
            try:
                index_num = int(index_num)
            except ValueError:
                print('Invalid response for Index number')
                print('no password was copied')
                print('Aborting!')
                exit()
            if index_num == 'n':
                exit()
            elif index_num > index - 1:
                print('There is no suggestion with that index number!')
            else:
                index_num = int(index_num) - 1
                # print(password)
                # exit()
                website, password, username = matched_arr[index_num]
                
                print(f'website: {website}, password: {password}, username: {username}')
                copy(password)
                with open('password.txt', 'w') as f:
                    f.write(password)
        print('time taken to find password: ' + find_password_time_colored)
        print('total time taken: ' + colored(str(time.time() - init_time), 'magenta'))

@cli.command()
@click.argument('website')
@click.argument('password')
@click.option('-u', type=str, default=None)
def en_pwd(website, password, u):
    password = evaluate_if_prompt_is_asked(password)
    username = u
    init_time2 = time.time()
    result = pm.enter_password(website, password, username)
    if result != None:
        print(result)
    else:
        print('total time taken: ' + colored(str(time.time() - init_time), 'magenta'))
        exit()

@cli.command()
@click.argument('website')
@click.argument('n_of_char')
@click.option('-u', type=str, default=None)
def gen(website, n_of_char, u):
    import pyperclip
    from utils import verify_for_illegal_password
    username = u
    password = pm.generate(website, n_of_char, username)
    password, passed = verify_for_illegal_password(password)
    password = colored(password, 'blue')
    print(password)
    copy(password)
    print('total time taken: ' + colored(str(time.time() - init_time), 'magenta'))
    exit()

@cli.command()
@click.argument('website')
@click.option('-u', type=str, default=None)
def delete(website, u):
    username = u
    if username == None:
        username = 'NULL'
    elif website[0] == '@':
        website = website.replace('@', '')
        website = website + ' ' + username
        username = 'NULL'
    sqh.delete_password(website, username)
    print('total time taken: ' + colored(str(time.time() - init_time), 'magenta'))

@cli.command()
def show():
    result = sqh.get_result()
    index = 0
    for r in result:
        website, password, username = r[0], r[1], r[2]
        print(f'website: {website}| password: {password}| username: {username}\n')
        index += 1
    
    print(f'number of entries: {index}')
    print('total time taken: ' + colored(str(time.time() - init_time), 'magenta'))

@cli.group()
@click.argument('filetype', type=click.Choice(['hdn', 'xlsx']))
@click.option('-cloud', type=bool, default=False)
@click.option('-compressed', '-cmp', type=click.Choice(['gz', 'zip']), default=None)
@click.option('-backup-path', '-path', '-p', type=click.Path(exists=True), default=None)
def backup(filetype, cloud, compressed, backup_path):
    from cloud.backup import Backup, Backup_hdn, BackupSqlite
    global default_dir
    global path_of_backup
    path_of_backup = backup_path
    # global isCompressed
    # isCompressed = compressed
    default_dir = ''

    global backup
    if cloud:
        access_token, default_dir = get_dropbox_info()
        if filetype == 'hdn':
            backup = Backup_hdn(cloud=True, access_token=access_token, compress_file_type=compressed)
        else:
            backup = Backup(cloud=True, access_token=access_token, compress_file_type=compressed)
    else:
        if filetype == 'hdn':
            backup = Backup_hdn(compress_file_type=compressed)
        else:
            backup = Backup(compress_file_type=compressed)
    
@backup.command()
def create():
    backup.create_backup(default_dir='/' + default_dir, default_path=path_of_backup)
    time_taken = str(time.time() - init_time)
    print(colored(f'total time taken: {time_taken}', 'blue'))

@backup.command()
def load():
    backup.load_backup(default_dir='/' + default_dir)
    time_taken = str(time.time() - init_time)
    print(colored(f'total time taken: {time_taken}', 'blue'))

@cli.command()
def set_db_engine():
    from utils import set_dab_engine
    curr_db_engine = get_db_engine()
    if curr_db_engine == 'sqlite3':
        new_db_engine_num = input(f"""
    these are the availaible database options:
    [1] sqlite3 {colored('**recommended**', 'cyan')} ({colored('current', 'magenta')})
    [2] mysql {colored('**if you know what you are doing**', 'cyan')}
        """)
    else:
        new_db_engine_num = input(f"""
    these are the availaible database options:
    [1] sqlite3 {colored('**recommended**', 'cyan')})
    [2] mysql {colored('**if you know what you are doing**', 'cyan')} ({colored('current', 'magenta')})
        """)

    valid_entry = True

    try:
        new_db_engine_num = int(new_db_engine_num)
    except ValueError:
        print('Enter 1 to select sqlite3 and 2 to select mysql')
        valid_entry = False
    
    if valid_entry:
        if new_db_engine_num == 1:
            new_db_engine = 'sqlite3' 
        else:
            curr_dir = os.path.dirname(__file__)
            config_file_path = os.path.join(curr_dir, 'data/UsernamePassword.json')
            new_db_engine = 'mysql'
            config_created = create_empty_mysql_config_file()
            if config_created == 1:
                print("install the mysql-connector pip package using 'pip install mysql-connector'")
                message_str = f"an empty config file has been generated in {config_file_path}"
                print(colored(message_str, 'red'))



    else:
        new_db_engine = curr_db_engine

    if curr_db_engine != new_db_engine:
        allow_changing_engine = input(f"""
        {colored('warning', 'red')}: you are about to change your database engine.
        The new database will not have your existing password information updated.
        Migrate information from previous db to new? (m to proceed with migration).
        proceed without migrating? (Y to proceed. any other to abort)
        """)
        if allow_changing_engine == 'm':
            print(new_db_engine)
            set_dab_engine(new_db_engine)
            from utils import migrate
            migrate(curr_db_engine)
        elif allow_changing_engine == 'Y':
            set_dab_engine(new_db_engine)
        else:
            print('Abort')

@cli.command()
def connect():
    from cloud import cloud
    cloud.CloudStorageHandler.authorize(None)
    exit()
if __name__ == '__main__':
    cli()
