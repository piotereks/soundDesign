# # Importing Tkinter module
# from tkinter import *
# from tkinter.ttk import *
#
# # Creating master Tkinter window
# master = Tk()
# master.geometry('175x175')
#
# # Tkinter string variable
# # able to store any string value
# v = StringVar(master, "1")
#
# Radiobutton(master, text="text", variable=v,
#             value=123).pack(side=TOP, ipady=5)
#
# mainloop()
from tkinter import *

def sel():
   selection = "You selected the option " + str(var.get() ) + " + " + str(Checkbutton1.get())
   label.config(text = selection)

root = Tk()
var = IntVar()
Checkbutton1 = IntVar()

Button1 = Checkbutton(root, text="Tutorial",
                      variable=Checkbutton1,
                      onvalue=1,
                      offvalue=0,
                      height=2,
                      width=10)
Button1.pack( anchor = W )
R1 = Radiobutton(root, text="Option 1", variable=var, value=1,
                  command=sel)
R1.pack( anchor = W )

R2 = Radiobutton(root, text="Option 2", variable=var, value=2,
                  command=sel)
R2.pack( anchor = W )

R3 = Radiobutton(root, text="Option 3", variable=var, value=3,
                  command=sel)
R3.pack( anchor = W)

label = Label(root)
label.pack()
root.mainloop()