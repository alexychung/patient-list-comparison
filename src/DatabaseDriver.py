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
        sql_insuranceonly = """CREATE TABLE IF NOT EXISTS InsuranceOnly (
                id INTEGER PRIMARY KEY, 
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL, 
                dob TEXT, 
                attributedprovider TEXT
        );"""
        sql_activepatientsonly = """CREATE TABLE IF NOT EXISTS ActivePatientsOnly (
                id INTEGER PRIMARY KEY, 
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL, 
                dob TEXT, 
                attributedprovider TEXT
        );"""
        sql_onbothlists = """CREATE TABLE IF NOT EXISTS OnBothLists (
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
            cursor.execute(sql_activepatientsonly)
            cursor.execute(sql_insuranceonly)
            cursor.execute(sql_onbothlists)
            self.commit()
            self.disconnect()
        except sqlite3.Error as e:
            print(e)

    def getOnBothLists(self):
        query = """INSERT INTO OnBothLists
            SELECT * FROM Insurance ilist LEFT JOIN ActivePatients alist ON ilist.firstname LIKE '%' + alist.firstname + '%'
            WHERE (ilist.lastname LIKE '%' + alist.lastname + '%' OR alist.lastname LIKE '%' + ilist.lastname + '%') AND ilist.dob = alist.dob
            UNION
            SELECT * FROM Insurance ilist LEFT JOIN ActivePatients alist ON alist.firstname LIKE '%' + ilist.firstname + '%'
            WHERE (ilist.lastname LIKE '%' + alist.lastname + '%' OR alist.lastname LIKE '%' + ilist.lastname + '%') AND ilist.dob = alist.dob
            """
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.commit()
            self.disconnect()
        except sqlite3.Error as e:
            print(e)

    def getInsuranceNotActive(self):
        self.getOnBothLists()
        query = """INSERT INTO InsuranceOnly
            SELECT * FROM Insurance ilist LEFT JOIN ActivePatients alist ON ilist.firstname LIKE '%' + alist.firstname + '%'
            WHERE (ilist.lastname LIKE '%' + alist.lastname + '%' OR alist.lastname LIKE '%' + ilist.lastname + '%') AND ilist.dob = alist.dob
            UNION
            SELECT ilist.* FROM Insurance ilist LEFT JOIN ActivePatients alist ON alist.firstname LIKE '%' + ilist.firstname + '%'
            WHERE (ilist.lastname LIKE '%' + alist.lastname + '%' OR alist.lastname LIKE '%' + ilist.lastname + '%') AND ilist.dob = alist.dob
            """
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.commit()
            self.disconnect()
        except sqlite3.Error as e:
            print(e)
    

    def getActiveNotInsurance(self):
        self.getOnBothLists()
        query = """INSERT INTO ActivePatientsOnly
            SELECT alist.* FROM ActivePatients alist LEFT JOIN Insurance ilist ON alist.firstname LIKE '%' + ilist.firstname + '%'
            WHERE (ilist.lastname LIKE '%' + alist.lastname + '%' OR alist.lastname LIKE '%' + ilist.lastname + '%') AND ilist.dob = alist.dob
            UNION
            SELECT alist.* FROM ActivePatients alist LEFT JOIN Insurance ilist ON ilist.firstname LIKE '%' + alist.firstname + '%'
            WHERE (ilist.lastname LIKE '%' + alist.lastname + '%' OR alist.lastname LIKE '%' + ilist.lastname + '%') AND ilist.dob = alist.dob
            """
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.commit()
            self.disconnect()
        except sqlite3.Error as e:
            print(e)






if __name__ == '__main__':
    database = DatabaseDriver()
    database.create_sqlite_db()
    database.create_tables()
    database.getInsuranceNotActive()
