import mysql.connector as connector

class sql_handler:
    def __init__(self, user, password, database):
        try:
            self.password_database = connector.connect(
                host='localhost',
                user=user,
                password=password,
                auth_plugin='mysql_native_password',
                database=database
            )
            self.database = database
            self.cursor = self.password_database.cursor()
        except connector.errors.ProgrammingError:
            print('Either the username or password is incorrect')
            change_to_sqlite = input('change the db the sqlite: (y/N): ')
            if change_to_sqlite == 'y':
                from utils import set_dab_engine
                set_dab_engine('sqlite3')
                exit()
        '''
        except connector.errors.InterfaceError:
            print('there is either no password or username entered in the file UsernamePassword.json in data dir')
            print('please enter the correct credentials or change the databse to sqlite3 manually in sife_configuration.json')
            exit()
'''
    
    def get_result(self):
        self.cursor.execute('SELECT * FROM passwords')
        result = self.cursor.fetchall()
        return result
    
    def commit(self):
        self.password_database.commit()

    def execute(self, query):
        try:
            self.cursor.execute(query)
        except connector.errors.DataError:
            print('The password or username or website which was generated or entered is too long.\nEither increase the limit by changing mysql table properties or decrease the length of given input or generated password.')
            exit()
        try:
            return self.cursor.fetchall()
        except connector.errors.InterfaceError:
            pass
    def insert_password(self, website, password, username):
        try:
            if username == None:
                username = 'NULL'

            query = f'INSERT INTO {self.database} (website, password, username) VALUES ("{website}", "{password}", "{username}")'
            self.execute(query)
            self.commit()
        except connector.errors.ProgrammingError:
            self.insert_password_single_quotes(website, password, username)
    
    def delete_password(self, website, username):
        query = f'DELETE FROM {self.database} WHERE website = "{website}" AND username = "{username}"'
        self.execute(query)
        self.commit()
    
    def insert_password_single_quotes(self, website, password, username):
        """
        When inserting password and website, if either of them have double quotes, mysql throws an error.
        Therefore, this function is designed to counter that and execute query successfully
        """
        query = f"INSERT INTO {self.database} (website, password, username) VALUES ('{website}', '{password}', '{username}')"
        self.execute(query)
        self.commit()

    def delete_table(self):
        self.execute(f'DELETE FROM {self.database};')

    def replace_password(self, website, password, username):
        if username == None:
            username = 'NULL'
        elif username == 'None':
            username = 'NULL'
        query = f"UPDATE {self.database} SET password='{password}' WHERE website='{website}' AND username='{username}'"
        self.execute(query)
        self.commit()
