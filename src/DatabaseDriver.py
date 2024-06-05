import sqlite3

class DatabaseDriver:

    connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect('database.db')
        except sqlite3.Error as e:
            print(e)
    
    def disconnect(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def create_sqlite_db(self):
        try:
            self.connect() 
        except sqlite3.Error as e:
            print(e)
        finally:
            if self.connection:
                self.disconnect()

    def create_tables(self):
        sql_insurancelist = """CREATE TABLE IF NOT EXISTS Insurance (
                id INTEGER PRIMARY KEY, 
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL, 
                dob TEXT, 
                attributedprovider TEXT
        );"""
        sql_activepatientslist = """CREATE TABLE IF NOT EXISTS ActivePatients (
                id INTEGER PRIMARY KEY, 
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL, 
                dob TEXT, 
                attributedprovider TEXT
        );"""
        try: 
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(sql_insurancelist)
            cursor.execute(sql_activepatientslist)
            self.commit()
            self.disconnect()
        except sqlite3.Error as e:
            print(e)





if __name__ == '__main__':
    database = DatabaseDriver()
    database.create_sqlite_db()
    database.create_tables()
