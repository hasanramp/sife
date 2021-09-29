import json
import encryptor
candidate_password_code = 'mYtIMMthetIiT[9'

def get_username_and_password():
    username_password_file = open('UsernamePassword.json')
    username_password_json = json.load(username_password_file)
    return username_password_json['username'], username_password_json['password']

with open('public_key.pem', 'r') as f:
    if f.read() == '':
        encryptor.encryptor.set_encryption(2048)