# Import Module
import tkinter as tk


class ButtonApp(tk.Tk):
# Create Object
# root = Tk()
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Add Title
        tk.Tk.title('On/Off Switch!')

        # Add Geometry
        tk.Tk.geometry("500x300")

        # Keep track of the button state on/off
        # global is_on
        self.is_on = True


        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.__label__()
        self.__button__()

        self.frames = {}
        frame = StartPage(self.container, self)
        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame(StartPage)

    def __label__(self):
        # Create Label
        self.my_label = tk.Label(self.container,
                         text="The Switch Is On!",
                         fg="green",
                         font=("Helvetica", 32))

        self.my_label.pack(pady=20)

    def __button__(self):
        # Define Our Images
        self.on = tk.PhotoImage(file="on.png")
        self.off = tk.PhotoImage(file="off.png")

        # Create A Button
        self.on_button = tk.Button(self.container, image=on, bd=0,
                           command=switch)
        self.on_button.pack(pady=50)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # Define our switch function
    def switch(self):
        # global is_on

        # Determine is on or off
        if self.is_on:
            self.on_button.config(image=self.off)
            self.my_label.config(text="The Switch is Off",
                            fg="grey")
            self.is_on = False
        else:

            self.on_button.config(image=self.on)
            self.my_label.config(text="The Switch is On", fg="green")
            self.is_on = True

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page")
        label.pack(pady=10, padx=10)


app = ButtonApp()
app.mainloop()





# Define Our Images
on = PhotoImage(file="on.png")
off = PhotoImage(file="off.png")

# Create A Button
on_button = Button(root, image=on, bd=0,
                   command=switch)
on_button.pack(pady=50)

# Execute Tkinter
root.mainloop()
