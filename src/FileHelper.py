from tkinter import filedialog

@staticmethod
def import_file(labelToSet):
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        labelToSet.config(text = file_path)
