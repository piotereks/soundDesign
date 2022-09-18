import tkinter
from tkinter import *

top = Tk()
top.geometry("450x300")

# the label for user_name

username = tkinter.StringVar()
username.set("Blah User")
user_name = Label(top,textvariable=username
                   ,text="Username"
                  ).place(x=40,y=60)
username.set("Blah User2")

# the label for user_password
user_password = Label(top, underline = 5,
                      text="Password").place(x=40,
                                             y=100)

submit_button = Button(top,
                       text="Submit").place(x=40,
                                            y=130)

user_name_input_area = Entry(top,
                             width=30).place(x=110,
                                             y=60)

user_password_entry_area = Entry(top,
                                 width=30).place(x=110,
                                                 y=100)

top.mainloop()
