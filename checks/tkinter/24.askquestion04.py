# illustration of icon - question
from tkinter import *
from tkinter import messagebox

main = Tk()

def check():
    messagebox.askquestion("Form",
                            "are you 18+",
                            icon ='question')

main.geometry("100x100")
B1 = Button(main, text = "check", command = check)
B1.pack()

main.mainloop()
