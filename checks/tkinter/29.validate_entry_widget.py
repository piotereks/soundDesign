import tkinter
from tkinter import *


def callback(input):
    if input.isdigit():
        print(input)
        return True

    elif input == "":
        print(input)
        return True

    else:
        print(input)
        return False


root = Tk()

e = Entry(root)
e.place(x=50, y=50)
reg = root.register(callback)

e.config(validate="key",
         validatecommand=(reg, '% P'))

root.mainloop()
