import tkinter as tk

HEIGHT = 700
WIDTH = 800

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="#ADD8E6")
canvas.pack()

frame = tk.Frame(root, bg="#FFD580")
frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

entry = tk.Entry(frame, bg='white')
entry.pack()

root.mainloop()