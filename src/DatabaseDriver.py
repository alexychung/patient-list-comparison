import sqlite3
from sqlalchemy import create_engine
import pandas
import FileHelper
from IPython.display import display

class DatabaseDriver:

    connection = None
    helper = None
    
    def __init__(self, filehelper):
        self.helper = filehelper

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
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL, 
                dob TEXT, 
                attributedprovider TEXT
        );"""
        sql_activepatientslist = """CREATE TABLE IF NOT EXISTS ActivePatients (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL, 
                dob TEXT, 
                attributedprovider TEXT
        );"""
        sql_insuranceonly = """CREATE TABLE IF NOT EXISTS InsuranceOnly (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL, 
                dob TEXT, 
                attributedprovider TEXT
        );"""
        sql_activepatientsonly = """CREATE TABLE IF NOT EXISTS ActivePatientsOnly (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL, 
                dob TEXT, 
                attributedprovider TEXT
        );"""
        sql_onbothlists = """CREATE TABLE IF NOT EXISTS OnBothLists (
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

    def clearTables(self):
        try:
            self.connect()
            deletepatients = "DELETE FROM ActivePatients"
            deleteinsurance = "DELETE FROM Insurance"
            deletepatientsonly = "DELETE FROM ActivePatientsOnly"
            deleteinsuranceonly = "DELETE FROM InsuranceOnly"
            deleteonboth = "DELETE FROM OnBothLists"
            cursor = self.connection.cursor()
            cursor.execute(deletepatients)
            cursor.execute(deletepatientsonly)
            cursor.execute(deleteinsurance)
            cursor.execute(deleteinsuranceonly)
            cursor.execute(deleteonboth)
            self.commit()
            self.disconnect()
        except sqlite3.Error as e:
            print(e)

    def insertInsuranceDFIntoTable(self, dataframe):
        engine = create_engine('sqlite:///database.db', echo=False)
        dataframe.to_sql('Insurance', con = engine, if_exists='replace', index = False)
        engine.dispose()

    
    def insertActivePatientDFIntoTable(self, dataframe):
        engine = create_engine('sqlite:///database.db', echo=False)
        dataframe.to_sql('ActivePatients', con = engine, if_exists='replace', index = False)
        engine.dispose()




    def getOnBothLists(self):
        query = """INSERT INTO OnBothLists
                SELECT a.firstname, a.lastname, a.dob, a.attributedprovider FROM ActivePatients AS a LEFT JOIN Insurance AS i 
                ON UPPER(a.firstname) LIKE UPPER(concat('%', i.firstname, '%')) AND UPPER(a.lastname) LIKE UPPER(concat('%', i.lastname, '%')) AND a.dob = i.dob
                WHERE i.firstname IS NOT NULL
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
    fh = FileHelper.FileHelper()
    database = DatabaseDriver(fh)
    database.clearTables()
    database.create_sqlite_db()
    database.create_tables()
    adf = pandas.read_excel(io='ActivePatientTest.xlsx', names = ["firstname", "lastname", "dob", "attributedprovider"])
    idf = pandas.read_excel(io='InsuranceTest.xlsx', names = ["firstname", "lastname", "dob", "attributedprovider"])
    fh.rename_columns(idf)
    database.insertActivePatientDFIntoTable(adf)
    database.insertInsuranceDFIntoTable(idf)
    database.getOnBothLists()
