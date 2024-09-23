import sqlite3
from sqlalchemy import create_engine
import pandas as pd
import spire.xls as spire
from spire.xls.common import *
from tkinter import messagebox
import Spreadsheet

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
        sql_listone = """CREATE TABLE IF NOT EXISTS ListOne (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL, 
                dob TEXT, 
                attributedprovider TEXT,
                phonenumber TEXT
        );"""
        sql_listtwo = """CREATE TABLE IF NOT EXISTS ListTwo (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL, 
                dob TEXT, 
                attributedprovider TEXT,
                phonenumber TEXT
        );"""
        sql_listoneonly = """CREATE TABLE IF NOT EXISTS ListOneOnly (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL, 
                dob TEXT, 
                attributedprovider TEXT,
                phonenumber TEXT
        );"""
        sql_listtwoonly = """CREATE TABLE IF NOT EXISTS ListTwoOnly (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL, 
                dob TEXT, 
                attributedprovider TEXT
                phonenumber TEXT
        );"""
        sql_onbothlists = """CREATE TABLE IF NOT EXISTS OnBothLists (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL, 
                dob TEXT, 
                attributedprovider TEXT
                phonenumber TEXT
        );"""
        try: 
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(sql_listone)
            cursor.execute(sql_listtwo)
            cursor.execute(sql_listoneonly)
            cursor.execute(sql_listtwoonly)
            cursor.execute(sql_onbothlists)
            self.commit()
            self.disconnect()
        except sqlite3.Error as e:
            print(e)

    def clearTables(self):
        try:
            self.connect()
            deletelisttwo = "DELETE FROM ListTwo"
            deletelistone = "DELETE FROM ListOne"
            deletelisttwoonly = "DELETE FROM ListTwoOnly"
            deletelistoneonly = "DELETE FROM ListOneOnly"
            deleteonboth = "DELETE FROM OnBothLists"
            cursor = self.connection.cursor()
            cursor.execute(deletelisttwo)
            cursor.execute(deletelisttwoonly)
            cursor.execute(deletelistone)
            cursor.execute(deletelistoneonly)
            cursor.execute(deleteonboth)
            self.commit()
            self.disconnect()
        except sqlite3.Error as e:
            print(e)

    def insertListOneDFIntoTable(self, spreadsheet : Spreadsheet.Spreadsheet):
        engine = create_engine('sqlite:///database.db', echo=False)
        spreadsheet.dataframe.to_sql('ListOne', con = engine, if_exists='replace', index = False)
        engine.dispose()

    
    def insertListTwoDFIntoTable(self, spreadsheet : Spreadsheet.Spreadsheet):
        engine = create_engine('sqlite:///database.db', echo=False)
        spreadsheet.dataframe.to_sql('ListTwo', con = engine, if_exists='replace', index = False)
        engine.dispose()




    def getOnBothLists(self):
        query = """
                SELECT a.firstname, a.lastname, a.dob, i.attributedprovider AS iattributedprovider, a.attributedprovider AS aattributedprovider, a.phonenumber FROM ListTwo AS a LEFT JOIN ListOne AS i 
                ON (UPPER(a.firstname) LIKE UPPER(concat('%', i.firstname, '%')) OR UPPER(i.firstname) LIKE UPPER(concat('%', a.firstname, '%')))
                AND (UPPER(a.lastname) LIKE UPPER(concat('%', i.lastname, '%')) OR UPPER(i.lastname) LIKE UPPER(concat('%', a.lastname, '%')))
                AND a.dob = i.dob
                WHERE i.firstname IS NOT NULL
                ORDER BY a.lastname, a.firstname;
                """
        try:
            self.connect()
            df = pd.read_sql_query(query, self.connection)
            self.disconnect()
            return df.rename(columns={'firstname': 'First Name', 'lastname': 'Last Name', 'dob': 'DOB', 'iattributedprovider': 'List One Attributed Provider', 'aattributedprovider': 'List Two Attributed Provider', 'phonenumber' : "Phone Number"})
        except sqlite3.Error as e:
            print(e)

    def getInsuranceNotActive(self):
        query = """
                SELECT i.firstname, i.lastname, i.dob, i.attributedprovider, i.phonenumber FROM ListOne AS i LEFT JOIN ListTwo AS a 
                ON (UPPER(a.firstname) LIKE UPPER(concat('%', i.firstname, '%')) OR UPPER(i.firstname) LIKE UPPER(concat('%', a.firstname, '%')))
                AND (UPPER(a.lastname) LIKE UPPER(concat('%', i.lastname, '%')) OR UPPER(i.lastname) LIKE UPPER(concat('%', a.lastname, '%')))
                AND a.dob = i.dob
                WHERE a.firstname IS NULL
                ORDER BY i.lastname, i.firstname;
                """
        try:
            self.connect()
            df = pd.read_sql_query(query, self.connection)
            self.disconnect()
            return df.rename(columns={'firstname': 'First Name', 'lastname': 'Last Name', 'dob': 'DOB', 'attributedprovider': 'Attributed Provider', 'phonenumber' : 'Phone Number'})
        except sqlite3.Error as e:
            print(e)
    

    def getActiveNotInsurance(self):
        query = """
                SELECT a.firstname, a.lastname, a.dob, a.attributedprovider, a.phonenumber FROM ListTwo AS a LEFT JOIN ListOne AS i 
                ON (UPPER(a.firstname) LIKE UPPER(concat('%', i.firstname, '%')) OR UPPER(i.firstname) LIKE UPPER(concat('%', a.firstname, '%')))
                AND (UPPER(a.lastname) LIKE UPPER(concat('%', i.lastname, '%')) OR UPPER(i.lastname) LIKE UPPER(concat('%', a.lastname, '%')))
                AND a.dob = i.dob
                WHERE i.firstname IS NULL
                ORDER BY a.lastname, a.firstname;
                """
        try:
            self.connect()
            df = pd.read_sql_query(query, self.connection)
            self.disconnect()
            return df.rename(columns={'firstname': 'Patient First Name', 'lastname': 'Patient Last Name', 'dob': 'DOB', 'attributedprovider': 'Attributed Provider', 'phonenumber' : 'Phone Number'})
        except sqlite3.Error as e:
            print(e)

    def generateOutput(self, filepath, listone : Spreadsheet.Spreadsheet, listtwo : Spreadsheet.Spreadsheet):
        try:
            writer = pd.ExcelWriter(filepath)
        except PermissionError as e:
            messagebox.showinfo("Error", "Please make sure that you do not have the desired save file currently opened.")
            return False
        onBoth = self.getOnBothLists()
        activeOnly = self.getActiveNotInsurance()
        insuranceOnly = self.getInsuranceNotActive()
        onBoth.to_excel(writer, 'Overlap')
        activeOnly.to_excel(writer, listtwo.name)
        insuranceOnly.to_excel(writer, listone.name)
        writer.close()
    
    def setup(self):
        self.clearTables()
        self.create_sqlite_db()
        self.create_tables()

    def insertTables(self, listtwo, listone):
        self.insertListTwoDFIntoTable(listtwo)
        self.insertListOneDFIntoTable(listone)

