from hdn import Parser
from cloud.cloud import CloudStorageHandler
import random2 as r
import json
from datetime import date

class ChangeLog:
    
    def __init__(self, access_token, app_key, app_secret):
        self.csh = CloudStorageHandler(access_token, app_key, app_secret)
        config_file = open('data/sife_configuration.json', 'r')
        config_json = json.load(config_file)
        self.devices_names = config_json['device_names']
        self.current_device = config_json['current_device']
        self.devices_names.remove(self.current_device)
        
    def update_change_log(self, changes):
        file_data = self.csh.get_file_data('changeLog.hdn', '/passwords').decode('utf8')
        file_data += f'\n{changes}'
        self.csh.update_with_data(file_data, 'changeLog.hdn', '/passwords')

    def upload_change_log(self):
        self.csh.upload('changeLog.hdn', '/passwords')

    def generate_change_id(self):
        id = ''
        for x in range(0, 10):
            id += r.choice('qwertyuiopasdfghjklxcvbnm')

        return id
    
    def make_changes_in_hdn(self, changes_raw):
        id = self.generate_change_id()
        parser = Parser('changeLog.hdn')
        changes_raw.append(id)
        changes_raw.append(date.today().strftime('%d-%m-Y'))
        devices_names = ' '.join(self.devices_names)
        changes_raw.append(self.devices_names)
        changes_hdn = parser.write_in_hdn([changes_raw])
        self.update_change_log(changes_hdn)

    def get_file_data(self):
        res = self.csh.get_file_data('changeLog.hdn', '/passwords').decode()
        parser = Parser('changeLog.hdn')
        res_list = parser.parse(res)
        return res_list

    def remove_device(self, device, id_):
        res = self.csh.get_file_data('changeLog.hdn', '/passwords').decode()
        parser = Parser('changeLog.hdn')
        res_list = parser.parse(res)
        for change in res_list:
            data_id = change[3]
            if id_ == data_id:
                data_device = change[5]
                if data_device == device:
                    change[5] = change[5].replace(device, '')
                else:
                    change[5] = change[5].replace(device + ' ', '')
        parser = Parser('changeLog.hdn')
        res_hdn = parser.write_in_hdn(res_list)
        change_log_file = open('changeLog.hdn', 'w').write(res_hdn)
        self.remove_entry(res_list)
        self.csh.update('changeLog.hdn', '/passwords')
    
    def remove_entry(self, res_list):
        changes_were_made = False
        old_res_list = res_list
        new_res_list = res_list
        index = 0
        for changes in new_res_list:
            data_device = changes[5]
            if data_device == '':
                new_res_list.remove(new_res_list[index])
                changes_were_made = True
            
            index += 1
        parser = Parser('changeLog.hdn')
        res_hdn = parser.write_in_hdn(res_list)
        change_log_file = open('changeLog.hdn', 'w').write(res_hdn)
        # self.csh.update('changeLog.hdn', '/passwords')
if __name__ == '__main__':
    def get_dropbox_info():
        file = open('dropbox.json', 'r')
        dropbox_json = json.load(file)
        return dropbox_json['access_token'], dropbox_json['app_key'], dropbox_json['app_secret'], dropbox_json['default_dir']

    access_token, app_key, app_secret, default_dir = get_dropbox_info()
    changeLog = ChangeLog(access_token, app_key, app_secret)
    # changeLog.make_changes_in_hdn(['hello', 'how', 'are'])
    changeLog.remove_device('windows', 'ddgrglqesx')
    changeLog.remove_device('android', 'ddgrglqesx')
    
