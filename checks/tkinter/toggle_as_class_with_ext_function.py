# Import Module
import tkinter as tk


class ButtonApp(tk.Frame):
# Create Object
# root = Tk()
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # Add Title
        # self.title('On/Off Switch!')

        # Add Geometry
        # self.geometry("500x300")

        # Keep track of the button state on/off
        # global is_on
        self.is_on = True


        self.pack(side="top", fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.__label__()
        self.__button__()

    def __label__(self):
        # Create Label
        self.my_label = tk.Label(self,
                         text="The Switch Is On!",
                         fg="green",
                         font=("Helvetica", 32))

        self.my_label.pack(pady=20)

    def __button__(self):
        # Define Our Images
        self.on = tk.PhotoImage(file="on.png")
        self.off = tk.PhotoImage(file="off.png")

        self.on_button = tk.Button(self,  text ="Blah", bd=0,background = "light blue",
                           command=self.dummy_switch)
        self.on_button.pack(pady=50)
        tk.Button()
    def dummy_switch(self):
        pass
    # def show_frame(self, cont):
    #     frame = self.frames[cont]
    #     frame.tkraise()

    # Define our switch function
    def switch(self):
        # global is_on

        # Determine is on or off
        if self.is_on:
            self.on_button.config(image=self.off)
            # self.on_button.config(text="Buu")
            self.my_label.config(text="The Switch is Off@",
                            fg="grey")
            self.is_on = False
        else:

            self.on_button.config(image=self.on)
            # self.on_button.config(text="hivyhyh")
            self.my_label.config(text="The Switch is On@", fg="green")
            self.is_on = True

def ext_switch(wrk_Tk):
    # global is_on

    # Determine is on or off
    if wrk_Tk.is_on:
        wrk_Tk.on_button.config(image=wrk_Tk.off)
        # self.on_button.config(text="Buu")
        wrk_Tk.my_label.config(text="The Switch is XOff@",
                        fg="grey")
        wrk_Tk.is_on = False
    else:

        wrk_Tk.on_button.config(image=wrk_Tk.on)
        # self.on_button.config(text="hivyhyh")
        wrk_Tk.my_label.config(text="The Switch is On@", fg="green")
        wrk_Tk.is_on = True

root = tk.Tk()
root.geometry("500x300")
root.title("Om/Off Toggle")

app = ButtonApp(root)
app.on_button.config(command= lambda : ext_switch(app))
app.mainloop()



