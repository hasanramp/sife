import dropbox
# from dropbox.files import WriteMode
import json
from termcolor import colored
import platform
import os
from github import Github
from github.GithubException import UnknownObjectException
from github.GithubException import BadCredentialsException
from github.GithubException import GithubException
import base64


class CloudStorageHandler:
    def __init__(self, access_token):
        # self.dbx = dropbox.Dropbox(oauth2_access_token=access_token, app_key=app_key, app_secret=app_secret)
        self.app_key = '6lxue1h2tvjoglh'
        self.app_secret = 'wmt8rdfou4d8obq'
        self.dbx = dropbox.Dropbox(oauth2_access_token=access_token, app_key=self.app_key, app_secret=self.app_secret)
        self.default_hdn_file = 'backup.hdn'
        self.default_excel_file = 'backup.xlsx'
        if platform.system() == 'Linux':
            self.os_file_divider = '/'
        elif platform.system() == 'Windows':
            self.os_file_divider = '\\'
    def upload(self, file, dir=''):
        with open(file, 'rb') as f:
            # print(file)
            # self.dbx.files_upload(f.read(), '/' + file)
            self.dbx.files_upload(f.read(), dir + '/' + file)

    def update(self, filepath, dir=''):
        file = filepath.split(self.os_file_divider)[-1]
        f = open(filepath, 'rb')
        try:
            self.dbx.files_upload(f.read(), os.path.join(dir, file), mode=dropbox.files.WriteMode.overwrite)
        except dropbox.dropbox_client.BadInputException:
        	print(colored('There is something wrong with your dropbox configuration', 'red'))
        	print(colored('try using sife connect to connect to dropbox', 'magenta'))
        except dropbox.exceptions.AuthError:
            print('most likely your request token has expired. use "sife connect" to refresh access token.')
            exit()
    def get_file_data(self, file, dir=''):
         metadata, res = self.dbx.files_download(path=dir + '/' + file)
         return res.content

    def update_with_data(self, data, filename, dir=''):
        # print(dir + '/' + filename)
        # self.dbx.files_delete(dir + '/' + filename)
        self.dbx.files_upload(data.encode('utf-8'), dir + '/' + filename, mode=dropbox.files.WriteMode.overwrite)
        
    def download(self, file, dir=''):
        filepath = file
        file = file.split(self.os_file_divider)[-1]
        print(dir + '/' + file)
        with open(filepath, 'wb') as f:
            metadata, res = self.dbx.files_download(path=dir + '/' + file)
            f.write(res.content)

    def authorize(auth_token):
        # session_dict = {
        #     "dropbox-auth-csrf-token" : ''
        # }
        dropbox_oauth = dropbox.oauth.DropboxOAuth2FlowNoRedirect(consumer_key='6lxue1h2tvjoglh', use_pkce=True,
        include_granted_scopes=None,
        locale="en", token_access_type="legacy")
        dropbox_oauth_link = dropbox_oauth.start()
        if auth_token != None:
            authorization_token = auth_token
        else:
            authorization_token = input('click on this link to get the authorization token - ' + dropbox_oauth_link + '/\nauthorization token: ')
        # print(access_token)
        access_token = dropbox_oauth.finish(authorization_token)
        # print(access_token)
        file = open('data/dropbox.json', 'r')
        dropbox_json = json.load(file)
        # print(dropbox_json)
        default_dir = dropbox_json['default_dir']
        new_json = {
            "access_token" : str(access_token.access_token),
            "default_dir" : default_dir
        }
        
        file = open('data/dropbox.json', 'w')
        json.dump(new_json, file)
        CloudStorageHandler(access_token.access_token).create_folder('/passwords')
        # self.create_folder('/passwords')
        

    def create_folder(self, path):
        self.dbx.files_create_folder(path, autorename=True)

class GithubCLoud:
    def __init__(self, access_token, repo):
        self.repo_name = repo
        self.access_token = access_token
        self.github = Github(access_token)
        try:
            self.repo = self.github.get_repo(repo)
        except BadCredentialsException:
            print("something is wrong with your github config")
            exit(1)
        
    def upload(self, filename, path):
        with open(path, 'rb') as f:
            self.repo.create_file(filename, "uploaded new file", f.read(), branch="main")
    def update(self, filename, path):

        try:
            contents = self.repo.get_contents(filename, ref='main')
        except UnknownObjectException:
            self.upload(filename, path)
            return
        except GithubException:
            self.upload(filename, path)
            return


        with open(path, 'rb') as f:
            backup_file_content = f.read()
            self.repo.update_file(contents.path, 'updated', backup_file_content, contents.sha, branch='main')

    def download(self, filename, path):
        contents = self.repo.get_contents(filename, ref='main')
        with open(path, 'wb') as f:
            f.write(base64.b64decode(contents.content))
