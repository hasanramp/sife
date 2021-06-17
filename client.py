import socket
import pyperclip

'''
            this is the command list format
for generate (g) - 
[username, password, 'generate', n_of_char, website_name]
for find password (fp) - 
[username, password, 'find password', website_name]
for enter password (ep) - 
[username, password, 'enter password', website_name, password]
'''

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.225.105"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def generate():
    n_of_char = input('number of characters in your password: ')
    website_name = input('website name: ')
    # com_list stands for command list
    com_list = f"""hasan,Iamthecreator!!,generate, {n_of_char}, {website_name}"""
    return com_list
def find_password():
    website_name = input('website name: ')
    com_list = f"""hasan,Iamthecreator!!,find password,{website_name}"""
    return com_list
def enter_password():
    website_name = input('website name: ')
    password = input('password: ')
    com_list = f"""hasan,Iamthecreator!!,enter password,{website_name},{password}"""
    return com_list

function = input('function: ')
if function == 'g':
    com_list = generate()
    com_list = com_list.encode(FORMAT)
    msg_length = len(com_list)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(com_list)
    password = client.recv(10240).decode(FORMAT)
    print(password)
    pyperclip.copy(password)

elif function == 'fp':
    com_list = find_password()
    com_list = com_list.encode(FORMAT)
    msg_length = len(com_list)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(com_list)
    password = client.recv(10240).decode(FORMAT)
    print(password)
    pyperclip.copy(password)
elif function == 'ep':
    com_list = enter_password()
    com_list = com_list.encode(FORMAT)
    msg_length = len(com_list)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(com_list)
    response = client.recv(10240).decode(FORMAT)
    print(response)
