import sqlite3

class sql_handler:
    def __init__(self, database):
        self.password_database = sqlite3.connect(database)
        self.database = database.split('/')[-1]
        self.database_name = self.database.replace('.db', '')
        # print(self.database_name)
        self.cursor = self.password_database.cursor()

    def get_result(self):
        try:
            self.cursor.execute('SELECT * FROM passwords;')
        except sqlite3.OperationalError:
            self.cursor.execute('CREATE TABLE passwords (website text, password text, username text);')
            return []
        result = self.cursor.fetchall()
        return result

    def commit(self):
        self.password_database.commit()

    def execute(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_password(self, website, password, username):
        if username is None:
            username = 'NULL'
        try:
            query = f'INSERT INTO {self.database_name} VALUES ("{website}", "{password}", "{username}");'
            self.execute(query)
            self.commit()
        except sqlite3.OperationalError:
            self.insert_password_single_quotes(website, password, username)

    def delete_password(self, website, username):
        query = f'DELETE FROM {self.database_name} WHERE website = "{website}" AND username = "{username}"'
        self.execute(query)
        self.commit()
        
    def insert_password_single_quotes(self, website, password, username):
        """
        When inserting password and website, if either of them have double quotes, mysql throws an error.
        Therefore, this function is designed to counter that and execute query successfully
        """
        query = f"INSERT INTO {self.database_name} VALUES ('{website}', '{password}', '{username}')"
        self.execute(query)
        self.commit()

    def replace_password(self, website, password, username):
        if username == None:
            username = 'NULL'
        elif username == 'None':
            username = 'NULL'
        query = f"UPDATE {self.database_name} SET password='{password}' WHERE website='{website}' AND username='{username}'"
        self.execute(query)
        self.commit()

    def delete_table(self):
        self.execute('DELETE FROM ' + self.database_name + ';')
