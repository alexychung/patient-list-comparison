from tkinter import messagebox, filedialog, ttk
import pandas as pd
import os
import DatabaseDriver
import sys
import tkinter as tk
import Spreadsheet

class FileHelper:

    def __init__(self):
        self.LISTONE = Spreadsheet.Spreadsheet()
        self.LISTTWO = Spreadsheet.Spreadsheet()


    def import_file(self, labelToSet, listname):
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            if (listname == "LISTONE"):
                self.LISTONE.dataframe = self.reading_spreadsheet(file_path, self.LISTONE)
                if (self.LISTONE.isFrame == True):
                    labelToSet.config(text = file_path)
            elif (listname == "LISTTWO"):
                self.LISTTWO.dataframe = self.reading_spreadsheet(file_path, self.LISTTWO)
                if (self.LISTTWO.isFrame == True):
                    labelToSet.config(text = file_path)
        

    def reading_spreadsheet(self, spreadsheetpath, list : Spreadsheet.Spreadsheet):
        data = pd.read_excel(io=spreadsheetpath)
        filename = "Only " + os.path.basename(spreadsheetpath)
        if (len(filename) > 31) :
            filename = filename[0:26] + "..."
        index = data.columns
        correctnames = ['Patient First Name', 'Patient Last Name', 'DOB', 'Attributed Provider', 'Phone Number']
        for i in range(len(correctnames)): 
             if (index[i] != correctnames[i]):
                messagebox.showerror("Invalid Format", "Please use the provided template and do not change the column names/order")
                return None
        list.isFrame = True
        data = data.rename(columns={'Patient First Name': 'firstname', 'Patient Last Name': 'lastname', 'DOB': 'dob', 'Attributed Provider': 'attributedprovider', 'Phone Number' : 'phonenumber'})
        data['dob'] = pd.to_datetime(data['dob']).dt.date
        list.name = filename
        return data

    def generate_lists(self, working_text: tk.Label):
        fln = self.getSaveFilePath()

        if self.checkHasLists() == False or fln == False:
            working_text.pack_forget()
            return False
        
        messagebox.showinfo("IMPORTANT", "Do not close the application, it will close itself when finished. Press OK to continue.")

        driver = DatabaseDriver.DatabaseDriver(self)
        driver.setup()
        driver.insertTables(self.LISTONE, self.LISTTWO)
        driver.generateOutput(fln, self.LISTONE, self.LISTTWO)
        messagebox.showinfo("Generation successful", "The program has finished running.")
        sys.exit()
    

    def checkHasLists(self):
        if self.LISTONE.isFrame == False or self.LISTTWO.isFrame == False:
            messagebox.showerror("Files Not Provided", "Please provide a .xlsx file for both lists ")
            return False
    
    def getSaveFilePath(self):
        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Excel File", filetypes=(("Excel File", ".xlsx"), ("All Files", ".*")))
        if fln == "": 
            return False
        fle = ".xlsx"
        fln = fln if fln[-len(fle):].lower() == fle else fln + fle
        return fln
    