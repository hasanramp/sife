from password_generator import password_gen
from termcolor import colored
from __init__ import get_db_engine

class Search:
    def __init__(self, to_search_from : list, to_search : str) -> None:
        self.search_arr = to_search_from
        self.to_search = to_search
        self.result = []
    
    def look_for_substring(self) -> list:
        for item in self.search_arr:
            if item.find(self.to_search)!= -1:
                self.result.append(item)
        
        return self.result
    
    def look_for_character_matches(self) -> dict:
        adv_res = {}
        for item in self.search_arr:
            for x in range(0, len(self.to_search)):
                char = self.to_search[x]
                if item.find(char) != -1:
                    try:
                        char_matches = adv_res[item]
                        adv_res[item] = char_matches + 1
                    except KeyError:
                        adv_res[item] = 1
        return adv_res

class TailorSearch(Search):
    def __init__(self, to_search_from : list, to_search : str) -> None:
        Search.__init__(self, to_search_from, to_search)

    def look_for_substring(self) -> list:
        for item in self.search_arr:
            if item[0].find(self.to_search)!= -1:
                self.result.append(item)
        
        return self.result

    def look_for_character_matches(self) -> dict:
        adv_res = {}
        for item in self.search_arr:
            index = 0
            for char in self.to_search:
                if item[0].find(char) != -1:
                    try:
                        char_matches = adv_res[item]
                        adv_res[item] = char_matches + 1
                    except KeyError:
                        adv_res[item] = 1
                if index == 0:
                    index += 1
                    if item[0][0] == char:
                        char_matches = adv_res[item]
                        adv_res[item] = char_matches + 2
        return adv_res

class password_manager:
    def __init__(self, database, encrypted=False):
        # self.encrypted = encrypted
        # self.encryption = encryptor()
        self.database = database
        # self.user = user
        # self.password = password
        # self.sqh = sql_handler(self.user, self.password, self.database)
        db_engine = get_db_engine()
        if db_engine == 'sqlite3':
            from db.sqlite3_handler import sql_handler
            self.sqh = sql_handler(self.database)
        else:
            from __init__ import get_username_and_password
            from db.sql_handler import sql_handler
            # print('reached here')
            user, password = get_username_and_password()
            # print('this is password', password)
            self.sqh = sql_handler(user, password, self.database)
        self.pg = password_gen()
        self.already_exists = colored('Password already exists in database. If you want to replace the password, put an \'@\' sign in fron of website name.\n example "@examplewebsite"', 'red')

    def verify_for_double_insertions(self, website, username):
        """This function verifies if the website already exists in database"""
        result = self.sqh.get_result()
        for r in result:
            data_website = r[0]
            data_username = r[2]
            if data_website == website and data_username == username:
                return True
            elif data_website == website and username == None and data_username == 'NULL':
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
        # if self.encrypted is True:
        #     password = self.encryption.encrypt(password)
        # else:
        #     pass
        if website[0] == '@':
            website = website.replace('@', '')
            self.replace_password(website, password, username)
            return self.encryption.decrypt(password)
        elif does_exist_in_db == True:
            return self.already_exists

        elif does_exist_in_db == False:
            self.sqh.insert_password(website, password, username)
            return password
        
    def replace_password(self, website, password, username):
        """
        This function replaces the old password and username of thew website with a new one.
        """
        # if self.encrypted is True:
        #     password = self.encryption.encrypt(password)
        self.sqh.replace_password(website, password, username)

    def find_password(self, website, username):
        query = f'SELECT password FROM passwords WHERE website = "{website}" AND username = "{username}";'
        password = self.sqh.execute(query)
        if password == []:
            return self.find_candidate_passwords(website)
        else:
            # if self.encrypted is True:
            #     return self.encryption.decrypt(password[0][0])
            return password[0][0]

    def find_candidate_passwords(self, website):
        """
        Finds for passwords if the find_password() function couldn't find.
        This looks at some of the letters of the website entered by user and website in database.
        It then compares them and sees if there is any entry.
        """
        # enc = self.encryption
        result = self.sqh.get_result()
        search = TailorSearch(result, website)
        base_search = search.look_for_substring()
        if base_search == []:
            return search.look_for_character_matches()
        else:
            return base_search
    
    def enter_password(self, website, password, username):
        does_exist = self.verify_for_double_insertions(website, username)
        # if self.encrypted is True:
        #     password = self.encryption.encrypt(password)
        if website[0] == '@':
            website = website[1:]
            self.replace_password(website, password, username)
        elif does_exist == True:
            return self.already_exists
        else:
            self.sqh.insert_password(website, password, username)

