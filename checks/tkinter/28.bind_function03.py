# Import all files from
# tkinter and overwrite
# all the tkinter files
# by tkinter.ttk
from tkinter import *
from tkinter.ttk import *

# function to be called when
# keyboard buttons are pressed
def key_press(event):
	key = event.char
	print(key, 'is pressed')

# creates tkinter window or root window
root = Tk()
root.geometry('200x100')

# here we are binding keyboard
# with the main window
root.bind('<Key>', key_press)

mainloop()
