import json

file = open('dropbox.json', 'r')
dropbox_json = json.load(file)

print(dropbox_json['access_token'])