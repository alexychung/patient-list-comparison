from tkinter import filedialog
import pandas as pd
from bs4 import BeautifulSoup
import ListApplication


@staticmethod
def import_file(labelToSet):
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        clonedpath = file_path
        labelToSet.config(text = file_path)
        if (labelToSet is ListApplication.insurance_text):
            print("hi")
            reading_spreadsheet(file_path)
        elif (labelToSet is ListApplication.patient_text):
            reading_spreadsheet(file_path)

def get_file_name_from_path(filepath):
    returnstring = filepath
    while (not returnstring.find("/") == -1 ):
        returnstring = returnstring[returnstring.find("/")+1, len(returnstring)]
    print(returnstring)
    return returnstring    
    

def reading_spreadsheet(spreadsheetpath):
    paths = []
    mySheet = 'Sheet Name'
    filename = spreadsheetpath
    data = BeautifulSoup()


@staticmethod
def generate_list(list1, list2):
    return list2-list1
