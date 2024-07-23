from tkinter import messagebox, filedialog
import pandas as pd
import os
import DatabaseDriver

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
                self.isInsurance = True
            elif (listname == "activepatient"):
                self.ACTIVEPATIENTLIST = self.reading_spreadsheet(file_path)
                self.isPatients = True

    def get_file_name_from_path(self, filepath):
        returnstring = filepath
        while (not returnstring.find("/") == -1):
            returnstring = returnstring[returnstring.find("/")+1:len(returnstring)]
        return returnstring    
        

    def reading_spreadsheet(self, spreadsheetpath):
        data = pd.read_excel(io=spreadsheetpath, names = ["firstname", "lastname", "dob", "attributedprovider"])
        data['dob'] = pd.to_datetime(data['dob']).dt.date
        return data

    def generate_lists(self):
        if self.checkHasLists() == False:
            return False
        
        fln = self.getSaveFilePath()

        driver = DatabaseDriver.DatabaseDriver(self)
        driver.setup()
        driver.insertTables(self.ACTIVEPATIENTLIST, self.INSURANCELIST)
        driver.generateOutput(fln)

    def checkHasLists(self):
        if self.isInsurance == False or self.isPatients == False:
            messagebox.showerror("Files Not Provided", "Please provide a .xlsx file for both lists ")
            return False
    
    def getSaveFilePath(self):
        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Excel File", filetypes=(("Excel File", ".xlsx"), ("All Files", ".*")))
        fle = ".xlsx"
        fln = fln if fln[-len(fle):].lower() == fle else fln + fle
        return fln
    