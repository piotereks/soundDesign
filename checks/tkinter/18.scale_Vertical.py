from tkinter import *

root = Tk()
root.geometry("400x300")
v2 = DoubleVar()


def show2():
    sel = "Vertical Scale Value = " + str(v2.get())
    l2.config(text=sel, font=("Courier", 14))


s2 = Scale(root, variable=v2,
           from_=50, to=1,
           orient=VERTICAL)

l4 = Label(root, text="Vertical Scaler")

b2 = Button(root, text="Display Vertical",
            command=show2,
            bg="purple",
            fg="white")

l2 = Label(root)

s2.pack(anchor=CENTER)
l4.pack()
b2.pack()
l2.pack()

root.mainloop()
