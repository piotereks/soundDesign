# Python program to illustrate the usage
# of hierarchical treeview in python GUI
# application using tkinter

# Importing tkinter
from tkinter import *

# Importing ttk from tkinter
from tkinter import ttk

# Creating app window
app = Tk()

# Defining title of the app
app.title("GUI Application of Python")

# Defining label of the app and calling a geometry
# management method i.e, pack in order to organize
# widgets in form of blocks before locating them
# in the parent widget
ttk.Label(app, text ="Treeview(hierarchical)").pack()

# Creating treeview window
treeview = ttk.Treeview(app)

# Calling pack method on the treeview
treeview.pack()

# Inserting items to the treeview
# Inserting parent
treeview.insert('', '0', 'item1',
				text ='GeeksforGeeks')

# Inserting child
treeview.insert('', '1', 'item2',
				text ='Computer Science')
treeview.insert('', '2', 'item3',
				text ='GATE papers')
treeview.insert('', 'end', 'item4',
				text ='Programming Languages')

# Inserting more than one attribute of an item
treeview.insert('item2', 'end', 'Algorithm',
				text ='Algorithm')
treeview.insert('item2', 'end', 'Data structure',
				text ='Data structure')
treeview.insert('item3', 'end', '2018 paper',
				text ='2018 paper')
treeview.insert('item3', 'end', '2019 paper',
				text ='2019 paper')
treeview.insert('item4', 'end', 'Python',
				text ='Python')
treeview.insert('item4', 'end', 'Java',
				text ='Java')

# Placing each child items in parent widget
treeview.move('item2', 'item1', 'end')
treeview.move('item3', 'item1', 'end')
treeview.move('item4', 'item1', 'end')

# Calling main()
app.mainloop()
