from tkinter import *

root = Tk()
root.geometry("300x200")

w = Label(root, text='GeeksForGeeks', font="50")
w.pack()

msg = Message(root, text="A computer science portal for geeks")

msg.pack()

root.mainloop()
