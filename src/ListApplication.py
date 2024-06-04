import tkinter as tk
from tkinter import filedialog
from FileHelper import *
from functools import partial

class MyWindow:
    def __init__(self, parent):
        self.parent = parent

        self.HEIGHT = 300
        self.WIDTH = 500

        canvas = tk.Canvas(root, height=self.HEIGHT, width=self.WIDTH, bg="#ADD8E6")
        canvas.pack(fill="both", expand = True)

        upframe = tk.Frame(root, bg="#FFD580")
        upframe.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.5)

        downframe = tk.Frame(root, bg="#FFD580")
        downframe.place(relx= 0.05, rely=0.6, relwidth=0.9, relheight = 0.35)

        buttonframe = tk.Frame(upframe, bg="#FFD580")
        buttonframe.pack(side="left")

        insuranceframe = tk.Frame(buttonframe)
        insuranceframe.pack(fill = "x")

        patientframe = tk.Frame(buttonframe)
        patientframe.pack(fill = "x")

        insurance_text = tk.Label(insuranceframe)
        insurance_button = tk.Button(insuranceframe, text="Select Insurance List File", command=partial(import_file, insurance_text, "insurance"))
        insurance_button.pack(side = "left")
        insurance_text.pack(side = "left")

        patient_text = tk.Label(patientframe)
        patient_button = tk.Button(patientframe, text="Select Patient List File", command=partial(import_file, patient_text, "activepatient"))
        patient_button.pack(side = "left")
        patient_text.pack(side = "left")

        generate_button = tk.Button(downframe, text="Generate Lists", command=generate_lists)
        generate_button.pack(side = "top")

if __name__ == '__main__':
    root = tk.Tk()
    top =  MyWindow(root)
    root.mainloop()