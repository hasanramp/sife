import dropbox
from password_managing_app.errors import InvalidFileFormat


class CloudStorageHandler:
    def __init__(self, access_token, app_key, app_secret):
        self.dbx = dropbox.Dropbox(oauth2_access_token=access_token, app_key=app_key, app_secret=app_secret)
        self.default_hdn_file = 'backup.hdn'
        self.default_excel_file = 'backup.xlsx'

    def upload(self, file):
        with open(file, 'rb') as f:
            self.dbx.files_upload(f.read(), '/' + file)
    
    def update(self, file):
        self.dbx.files_delete('/' + file)
        with open(file, 'rb') as f:
            self.dbx.files_upload(f.read(), '/' + file)
    def download(self, file):
        
        with open(file, 'wb') as f:
            metadata, res = self.dbx.files_download(path='/' + file)
            f.write(res.content)
