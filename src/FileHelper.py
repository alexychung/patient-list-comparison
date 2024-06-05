from tkinter import messagebox, filedialog
import pandas as pd
import os
import csv

from pymongo import MongoClient


INSURANCELIST = None
ACTIVEPATIENTLIST = None
isInsurance = False
isPatients = False

@staticmethod
def import_file(labelToSet, listname):
    global INSURANCELIST, ACTIVEPATIENTLIST, isInsurance, isPatients
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        labelToSet.config(text = file_path)
        if (listname == "insurance"):
            INSURANCELIST = reading_spreadsheet(file_path)
            isInsurance = True
        elif (listname == "activepatient"):
            ACTIVEPATIENTLIST = reading_spreadsheet(file_path)
            isPatients = True

@staticmethod
def get_file_name_from_path(filepath):
    returnstring = filepath
    while (not returnstring.find("/") == -1):
        returnstring = returnstring[returnstring.find("/")+1:len(returnstring)]
    return returnstring    
    

@staticmethod
def reading_spreadsheet(spreadsheetpath):
    data = pd.read_excel(spreadsheetpath, index_col = 0)
    return data


@staticmethod
def generate_lists():
    global ACTIVEPATIENTLIST, INSURANCELIST, isInsurance, isPatients
    print(INSURANCELIST.head(n=5))
    if isInsurance == False or isPatients == False:
        messagebox.showerror("Files Not Provided", "Please provide a .xlsx file for both lists ")
        return False
    
    fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Excel File", filetypes=(("Excel File", ".xlsx"), ("All Files", ".*")))
    fle = ".xlsx"
    fln = fln if fln[-len(fle):].lower() == fle else fln + fle
    print(fln)
    with pd.ExcelWriter(fln) as writer:
        INSURANCELIST.to_excel(writer, sheet_name='List')


    # file_name = 'data.xlsx'

    # with pd.ExcelWriter(file_name) as writer:
    #     INSURANCELIST.to_excel(writer, sheet_name='List', index = False)
