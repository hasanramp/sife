import json

f = open('UsernamePassword.json')

f_json = json.load(f)
print(f_json['username'], f_json['password'])