
# illustration of icon - Warning
from tkinter import *
from tkinter import messagebox

main = Tk()

def check():
    messagebox.askquestion("Form",
                            "Gender is empty?",
                            icon ='warning')

main.geometry("100x100")
B1 = Button(main, text = "check", command = check)
B1.pack()

main.mainloop()
