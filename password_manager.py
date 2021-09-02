from password_managing_app.sql_handler import sql_handler
from password_managing_app.password_generator import password_gen

class password_manager:
    def __init__(self, user, password, database):
        self.user = user
        self.password = password
        self.database = database
        self.sqh = sql_handler(self.user, self.password, self.database)
        self.pg = password_gen()
        self.already_exists = 'Password already exists in database. If you want to replace the password, put an \'@\' sign in fron of website name.\n example "@examplewebsite"'

    def verify_for_double_insertions(self, website, username):
        """This function verifies if the website already exists in database"""
        result = self.sqh.get_result()
        for r in result:
            data_website = r[0]
            data_username = r[2]
            if data_website == website and data_username == username:
                return True
            elif data_website == website and username == None and data_username == '#none':
                return True
            else:
                pass
        return False

    def generate(self, website, n_of_char, username=None):
        """This simply generates a new random password from password generator.
           Then if the website first letter is "@", it means that the website already exists
           and the password should be changed.
        """
        does_exist_in_db = self.verify_for_double_insertions(website, username)
        password = self.pg.generate(n_of_char)
        if website[0] == '@':
            website = website.replace('@', '')
            self.replace_password(website, password, username)
            return password
        elif does_exist_in_db == True:
            return self.already_exists

        elif does_exist_in_db == False:
            self.sqh.insert_password(website, password, username)
            return password
        
    def replace_password(self, website, password, username):
        """
        This function replaces the old password and username of thew website with a new one.
        """
        self.sqh.delete_password(website, username)
        self.sqh.insert_password(website, password, username)

    def find_password(self, website, username):
        password = self.sqh.execute(f'SELECT password FROM passwords WHERE website = "{website}" AND username = "{username}"')
        if password == []:
            return self.find_candidate_passwords(website)
        else:
            return password[0][0]

    def find_candidate_passwords(self, website):
        """
        Finds for passwords if the find_password() function couldn't find.
        This looks and the some of the letters of the website entered by user and website in database.
        It then compares them and sees if there is any entry.
        """
        result = self.sqh.get_result()
        website_password_username = []
        for r in result:
            data_website, data_password, data_username = r[0], r[1], r[2]
            if len(website) >= 4:
                first_four_char_of_data_website = data_website[0 : 4]
                first_four_char_of_website = website[0 : 4]
                if first_four_char_of_data_website == first_four_char_of_website:
                    website_password_username.append(f'website: {data_website}|password: {data_password}|username: {data_username}')
            else:
                len_of_website = len(website)
                first_n_characters_of_data_website = data_website[0 : len_of_website]
                if first_n_characters_of_data_website == website:
                    website_password_username.append(f'{data_website}, {data_password}, {data_username}')
        if website_password_username == []:
            return False
        else:
            return ['candidate passwords', website_password_username]
    
    def enter_password(self, website, password, username):
        does_exist = self.verify_for_double_insertions(website, username)
        if website[0] == '@':
            website = website.replace('@', '')
            self.replace_password(website, password, username)
        elif does_exist == True:
            return self.already_exists
        else:
            self.sqh.insert_password(website, password, username)

