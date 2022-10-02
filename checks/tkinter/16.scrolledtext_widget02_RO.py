# Importing required modules

import tkinter as tk
import tkinter.scrolledtext as st

# Creating tkinter window
win = tk.Tk()
win.title("ScrolledText Widget")

# Title Label
tk.Label(win,
		text = "ScrolledText Widget Example",
		font = ("Times New Roman", 15),
		background = 'green',
		foreground = "white").grid(column = 0,
									row = 0)

# Creating scrolled text area
# widget with Read only by
# disabling the state
text_area = st.ScrolledText(win,
							width = 30,
							height = 8,
							font = ("Times New Roman",
									15))

text_area.grid(column = 0, pady = 10, padx = 10)

# Inserting Text which is read only
text_area.insert(tk.INSERT,
"""\
This is a scrolledtext widget to make tkinter text read only.
Hi
Geeks !!!
Geeks !!!
Geeks !!!
Geeks !!!
Geeks !!!
Geeks !!!
Geeks !!!
""")

# Making the text read only
text_area.configure(state ='disabled')
win.mainloop()
