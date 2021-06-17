import socket
from pwd_gen import pswd_gen
import threading

HEADER = 64
PORT = 5050
SERVER = '192.168.225.105'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

users_list = ['hasan']
passwords_list = ['Iamthecreator!!']
'''
            this is the command list format
for generate (g) - 
[username, password, 'generate', n_of_char, website_name]
for find password (fp) - 
[username, password, 'find password', website_name]
for enter password (ep) - 
[username, password, 'enter password', website_name, password]
'''
def verify_user(username, password):
    for user in users_list:
        if user == username:
            username_index = users_list.index(username)
            if password == passwords_list[username_index]:
                return 'passed'
                
            else:
                return 'failed'

        else:
            pass
    return 'failed'
def pg_app(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        command_length = conn.recv(HEADER).decode(FORMAT)
        if command_length:
            command_length = int(command_length)
            command = conn.recv(command_length).decode(FORMAT)
            decoded_command_list = command.split(',')
            username = decoded_command_list[0]
            print(username)
            password = decoded_command_list[1]
            if verify_user(username, password) == 'failed':
                conn.send('access denied'.encode(FORMAT))
                conn.close()
            else:
                pass
            if username == 'hasan':
                file = 'password_database.xlsx'
            else:
                file = 'this is not a file'
            print(file)
            pg = pswd_gen.password_generator(file)
            
            command_name=  decoded_command_list[2]
            if command_name == 'find password':
                website_name = decoded_command_list[3]
                print(website_name)
                password = pg.find_password(website_name)
                print(password)
                conn.send(str(password).encode(FORMAT))
                conn.close()
            elif command_name == 'generate':
                n_of_char =  int(decoded_command_list[3])
                website_name = decoded_command_list[4]
                password = pg.generate_pswd(n_of_char=n_of_char, website_name=website_name)
                conn.send(str(password).encode(FORMAT))
                conn.close()
            elif command_name == 'enter password':
                website_name = decoded_command_list[3]
                password = decoded_command_list[4]
                response = pg.enter_password(website_name=website_name, password=password)
                conn.send(str(response).encode(FORMAT))
                conn.close()
            else:
                pass    
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=pg_app, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()
