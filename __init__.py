import json
# from encryption.encryptor import encryptor
import datetime
from calendar import monthrange
import os

candidate_password_code = 'mYtIMMthetIiT[9'

def get_db_engine():
    configuration_file = open('data/sife_configuration.json', 'r')
    configuration_json = json.load(configuration_file)
    db_engine = configuration_json['db_engine']
    return db_engine

def get_username_and_password():
    username_password_file = open('data/UsernamePassword.json')
    username_password_json = json.load(username_password_file)
    return username_password_json['username'], username_password_json['password']

def check_for_last_synced():
    changes_file = open('changes.json')
    changes_json = json.load(changes_file)
    last_date = changes_json['last synced']

    curr_date = datetime.date.today().strftime("%d-%m-%Y")
    last_day, last_month, last_year = last_date.split('-')
    last_day, last_month, last_year = int(last_day), int(last_month), int(last_year)
    curr_day, curr_month, curr_year = curr_date.split('-')
    curr_day, curr_month, curr_year = int(curr_day), int(curr_month), int(curr_year)
    day_diff = 0
    if last_year == curr_year:
        if last_month == curr_month:
            if last_day == curr_day:
                pass
            else:
                day_diff = curr_day - last_day
        else:
            month_diff = curr_month - last_month
            for x in range(0, month_diff):
                month = last_month + x
                num_days = monthrange(curr_year, month)[1]
                day_diff += num_days
            day_diff += curr_day - last_day
    else:
        return -1
    return day_diff

def register_latest_synced_date():
    changes_file = open('changes.json', 'r')
    changes_json = json.load(changes_file)
    n_of_changes = changes_json['no. of changes']
    new_json = {
        "no. of changes": n_of_changes,
        "last synced" : datetime.date.today().strftime("%d-%m-%Y")
    }
    changes_file = open('changes.json', 'w')
    json.dump(new_json, changes_file)
    return n_of_changes

def change_n_of_changes(reset=False):
    changes_file = open('changes.json', 'r')
    changes_json = json.load(changes_file)
    if reset:
        new_json = {
            "no. of changes": 0,
            "last synced" : datetime.date.today().strftime("%d-%m-%Y")
        }
    else:
        n_of_changes = changes_json['no. of changes']
        new_json = {
            "no. of changes": n_of_changes + 1,
            "last synced" : datetime.date.today().strftime("%d-%m-%Y")
        }
    changes_file = open('changes.json', 'w')
    json.dump(new_json, changes_file)


# try:
#     with open('public_key.pem', 'r') as f:
#         if f.read() == '':
#             encryptor.encryptor.set_encryption(2048)
# except FileNotFoundError:
#     encryptor().set_encryption(2048)
