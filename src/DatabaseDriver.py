import sqlite3
from sqlalchemy import create_engine
import pandas as pd
import FileHelper

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
        query = """
                SELECT a.firstname, a.lastname, a.dob, a.attributedprovider FROM ActivePatients AS a LEFT JOIN Insurance AS i 
                ON (UPPER(a.firstname) LIKE UPPER(concat('%', i.firstname, '%')) OR UPPER(i.firstname) LIKE UPPER(concat('%', a.firstname, '%')))
                AND (UPPER(a.lastname) LIKE UPPER(concat('%', i.lastname, '%')) OR UPPER(i.lastname) LIKE UPPER(concat('%', a.lastname, '%')))
                AND a.dob = i.dob
                WHERE i.firstname IS NOT NULL
                """
        try:
            self.connect()
            df = pd.read_sql_query(query, self.connection)
            self.disconnect()
            return df
        except sqlite3.Error as e:
            print(e)

    def getInsuranceNotActive(self):
        query = """
                SELECT i.firstname, i.lastname, i.dob, i.attributedprovider FROM Insurance AS i LEFT JOIN ActivePatients AS a 
                ON (UPPER(a.firstname) LIKE UPPER(concat('%', i.firstname, '%')) OR UPPER(i.firstname) LIKE UPPER(concat('%', a.firstname, '%')))
                AND (UPPER(a.lastname) LIKE UPPER(concat('%', i.lastname, '%')) OR UPPER(i.lastname) LIKE UPPER(concat('%', a.lastname, '%')))
                AND a.dob = i.dob
                WHERE a.firstname IS NULL
                """
        try:
            self.connect()
            df = pd.read_sql_query(query, self.connection)
            self.disconnect()
            return df
        except sqlite3.Error as e:
            print(e)
    

    def getActiveNotInsurance(self):
        self.getOnBothLists()
        query = """
                SELECT a.firstname, a.lastname, a.dob, a.attributedprovider FROM ActivePatients AS a LEFT JOIN Insurance AS i 
                ON (UPPER(a.firstname) LIKE UPPER(concat('%', i.firstname, '%')) OR UPPER(i.firstname) LIKE UPPER(concat('%', a.firstname, '%')))
                AND (UPPER(a.lastname) LIKE UPPER(concat('%', i.lastname, '%')) OR UPPER(i.lastname) LIKE UPPER(concat('%', a.lastname, '%')))
                AND a.dob = i.dob
                WHERE i.firstname IS NULL
                """
        try:
            self.connect()
            df = pd.read_sql_query(query, self.connection)
            self.disconnect()
            return df
        except sqlite3.Error as e:
            print(e)

    def generateOutput(self, filepath):
        writer = pd.ExcelWriter(filepath)
        onBoth = self.getOnBothLists()
        activeOnly = self.getActiveNotInsurance()
        insuranceOnly = self.getInsuranceNotActive()
        onBoth.to_excel(writer, 'Overlap')
        activeOnly.to_excel(writer, 'Active Only')
        insuranceOnly.to_excel(writer, 'Insurance Only')
        writer.close()
    
    def setup(self):
        self.clearTables()
        self.create_sqlite_db()
        self.create_tables()

    def insertTables(self, activepatients, insurance):
        self.insertActivePatientDFIntoTable(activepatients)
        self.insertInsuranceDFIntoTable(insurance)

