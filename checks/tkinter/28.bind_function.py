# Import all files from
# tkinter and overwrite
# all the tkinter files
# by tkinter.ttk
from tkinter import *
from tkinter.ttk import *

# creates tkinter window or root window
root = Tk()
root.geometry('200x100')

# function to be called when mouse enters in a frame
def enter(event):
	print('Button-2 pressed at x = % d, y = % d'%(event.x, event.y))

# function to be called when mouse exits the frame
def exit_(event):
	print('Button-3 pressed at x = % d, y = % d'%(event.x, event.y))

# frame with fixed geometry
frame1 = Frame(root, height = 100, width = 200)

# these lines are showing the
# working of bind function
# it is universal widget method
frame1.bind('<Enter>', enter)
frame1.bind('<Leave>', exit_)

frame1.pack()

mainloop()
