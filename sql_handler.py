import mysql.connector as connector

class sql_handler:
    def __init__(self, user, password, database):
        self.password_database = connector.connect(
            host='localhost',
            user=user,
            password=password,
            auth_plugin='mysql_native_password',
            database=database
        )
        self.database = database
        self.cursor = self.password_database.cursor()
    
    def get_result(self):
        self.cursor.execute('SELECT * FROM passwords')
        result = self.cursor.fetchall()
        return result
    
    def commit(self):
        self.password_database.commit()

    def execute(self, query):
        self.cursor.execute(query)
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
