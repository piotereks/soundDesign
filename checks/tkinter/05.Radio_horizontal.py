# Importing Tkinter module
from tkinter import *
from tkinter.ttk import *

# Creating master Tkinter window
master = Tk()
master.geometry('600x175')

# Tkinter string variable
# able to store any string value
v = StringVar(master, "1")

# Style class to add style to Radiobutton
# it can be used to style any ttk widget
style = Style(master)
style.configure("TRadiobutton", background = "light green",
				foreground = "red", font = ("arial", 10, "bold"))

class Note(object):
    names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

note = Note()

values = {x[0]:x[1] for x in enumerate(note.names)}

# Dictionary to create multiple buttons
# values = {"RadioButton 1" : "1",
# 		"RadioButton 2" : "2",
# 		"RadioButton 3" : "3",
# 		"RadioButton 4" : "4",
# 		"RadioButton 5" : "5"}

# Loop is used to create multiple Radiobuttons
# rather than creating each button separately
for (value, text) in enumerate(note.names):
	Radiobutton(master, text = text, variable = v,
				value = value).grid(row=0, column = value)

# Infinite loop can be terminated by
# keyboard or mouse interrupt
# or by any predefined function (destroy())
mainloop()
