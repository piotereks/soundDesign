# Importing Tkinter module
from tkinter import *

# from tkinter.ttk import *

# Creating master Tkinter window
master = Tk()
master.geometry("175x175")

# Tkinter string variable
# able to store any string value
v = StringVar(master, "1")

# Dictionary to create multiple buttons
values = {"RadioButton 1": "1",
          "RadioButton 2": "2",
          "RadioButton 3": "3",
          "RadioButton 4": "4",
          "RadioButton 5": "5"}

# Loop is used to create multiple Radiobuttons
# rather than creating each button separately
# background_v=StringVar()
for (text, value) in values.items():
    if int(value)%2 == 0:
        print(value)
        background_v="light blue"
    else:
        print("sfdadf:",value)
        background_v="red"

    Radiobutton(master, text = text, variable = v,
        value = value, indicator = 1 ,
        background = background_v).pack(fill = X, ipady = 5)

# Infinite loop can be terminated by
# keyboard or mouse interrupt
# or by any predefined function (destroy())
mainloop()
