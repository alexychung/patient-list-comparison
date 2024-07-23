from tkinter import messagebox, filedialog
import pandas as pd
import os
import sqlite3

from pymongo import MongoClient

class FileHelper:

    INSURANCELIST = None
    ACTIVEPATIENTLIST = None
    isInsurance = None
    isPatients = None

    def __init__(self):
        self.INSURANCELIST = None
        self.ACTIVEPATIENTLIST = None
        self.isInsurance = False
        self.isPatients = None


    def import_file(self, labelToSet, listname):
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            labelToSet.config(text = file_path)
            if (listname == "insurance"):
                self.INSURANCELIST = self.reading_spreadsheet(file_path)
                print("insurance:")
                print(self.INSURANCELIST.head())
                self.isInsurance = True
            elif (listname == "activepatient"):
                self.ACTIVEPATIENTLIST = self.reading_spreadsheet(file_path)
                print("activepatient:")
                print(self.ACTIVEPATIENTLIST.head())
                self.isPatients = True

    def get_file_name_from_path(self, filepath):
        returnstring = filepath
        while (not returnstring.find("/") == -1):
            returnstring = returnstring[returnstring.find("/")+1:len(returnstring)]
        return returnstring    
        

    def reading_spreadsheet(self, spreadsheetpath):
        data = pd.read_excel(spreadsheetpath)
        return data
    
    def rename_columns(self, dataframe):
        dataframe.rename(columns={'First Name': 'firstname', 'Last Name': 'lastname', 'DOB': 'dob', 'Attributed Provider': 'attributedprovider'})

    def generate_lists(self):
        print(self.INSURANCELIST.head(n=5))
        if self.isInsurance == False or self.isPatients == False:
            messagebox.showerror("Files Not Provided", "Please provide a .xlsx file for both lists ")
            return False
        
        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Excel File", filetypes=(("Excel File", ".xlsx"), ("All Files", ".*")))
        fle = ".xlsx"
        fln = fln if fln[-len(fle):].lower() == fle else fln + fle
        print(fln)
        with pd.ExcelWriter(fln) as writer:
            self.INSURANCELIST.to_excel(writer, sheet_name='List')
