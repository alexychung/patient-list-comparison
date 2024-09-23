import tkinter as tk
from tkinter import ttk
from FileHelper import *
from functools import partial

class MyWindow:

    helper = None

    def __init__(self, parent):

        self.helper = FileHelper()

        self.parent = parent

        BACKGROUNDCOLOR = "#B85042"
        FRAMECOLOR = "#E7E8D1"
        BUTTONCOLOR = "#EDF4F2"
        
        instructionwrap = 450

        self.HEIGHT = 350
        self.WIDTH = 500

        root.title("List Comparison Application")

        canvas = tk.Canvas(root, height=self.HEIGHT, width=self.WIDTH, bg=BACKGROUNDCOLOR)
        canvas.pack(fill="both", expand = True)

        upframe = tk.Frame(root, bg=FRAMECOLOR)
        upframe.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.65)

        downframe = tk.Frame(root, bg=FRAMECOLOR)
        downframe.place(relx= 0.05, rely=0.75, relwidth=0.9, relheight = 0.2)

        instructions_text = tk.Label(upframe, bg = FRAMECOLOR, font = ("bold"), text = "Instructions:")

        step1_text = tk.Label(upframe, bg = FRAMECOLOR, text = "1. Copy and paste the information into the template provided.This needs to be done for both lists. Each list should be in it's own separate file.", wraplength = instructionwrap, anchor = "w")
        step2_text = tk.Label(upframe, bg = FRAMECOLOR, text = "2. Upload the template files using the upper two buttons.", wraplength = instructionwrap, anchor = "w")
        step3_text = tk.Label(upframe, bg = FRAMECOLOR, text = "3. Press the generate button to run the program and save the new spreadsheet.", wraplength = instructionwrap, anchor = "w")

        instructions_text.pack(side = "top")
        step1_text.pack(side = "top", anchor = "w")
        step2_text.pack(side = "top")
        step3_text.pack(side = "top")

        buttonframe = tk.Frame(upframe, bg=FRAMECOLOR)
        buttonframe.pack(side="left")

        listoneframe = tk.Frame(buttonframe, bg=FRAMECOLOR)
        listoneframe.pack(fill = "x")

        listtwoframe = tk.Frame(buttonframe, bg=FRAMECOLOR)
        listtwoframe.pack(fill = "x")


        listone_text = tk.Label(listoneframe, background = FRAMECOLOR)
        listone_button = tk.Button(listoneframe, background = BUTTONCOLOR, width=20, height = 1, font = ('Arial', 9), text="Select List One File", command=partial(self.helper.import_file, listone_text, "LISTONE"))
        listone_button.pack(side = "left")
        listone_text.pack(side = "left")

        listtwo_text = tk.Label(listtwoframe, background = FRAMECOLOR)
        listtwo_button = tk.Button(listtwoframe, background = BUTTONCOLOR, width = 20, height = 1, font = ('Arial', 9), text="Select List Two File", command=partial(self.helper.import_file, listtwo_text, "LISTTWO"))
        listtwo_button.pack(side = "left")
        listtwo_text.pack(side = "left")

        generate_button = tk.Button(downframe, background = BUTTONCOLOR, text="Generate Excel File", command=self.generate_lists)
        generate_button.pack(side = "top")

        self.working_text = tk.Label(downframe, background = FRAMECOLOR, text = "Please wait for the program to finish. Do not close the application.", foreground = "red")
    
    def generate_lists(self):
        self.helper.generate_lists(self.working_text)


if __name__ == '__main__':
    root = tk.Tk()
    top =  MyWindow(root)
    root.mainloop()