# Import Module
import tkinter as tk
# from tkinter.ttk import *
import tkinter.ttk as ttk

class SoundDesignGui(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

        self.is_on = True

        self.pack(side="top", fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.__label__()
        self.__button__()

    # def __label__(self):
    #     # Create Label
    #     self.my_label = tk.Label(self,
    #                      text="The Switch Is On!",
    #                      fg="green",
    #                      font=("Helvetica", 32))
    #
    #     self.my_label.pack(pady=20)

    def __button__(self):
        # Define Our Images
        # self.on = tk.PhotoImage(file="on.png")
        # self.off = tk.PhotoImage(file="off.png")

        # self.on_button = tk.Button(self, text ="Blah", bd=0, background = "light blue",
        #                            command=self.dummy_command)
        self.on_button = ttk.Button(self, text ="Blah", command=self.dummy_command)


        self.on_button.pack(pady=50)
        # ttk.Button()

    def dummy_command(self):
        pass
    def test_command(self, func : callable):
        print('before')
        func()
        print('after')
    # Define our switch function
    # def switch(self):
    #     # global is_on
    #
    #     # Determine is on or off
    #     if self.is_on:
    #         # self.on_button.config(image=self.off)
    #         self.on_button.config(text="Buu")
    #         self.my_label.config(text="The Switch is Off@",
    #                         fg="grey")
    #         self.is_on = False
    #     else:
    #
    #         # self.on_button.config(image=self.on)
    #         self.on_button.config(text="hivyhyh")
    #         self.my_label.config(text="The Switch is On@", fg="green")
    #         self.is_on = True

def ext_switch(appFrame):
    # global is_on

    # Determine is on or off
    if appFrame.is_on:
        # appFrame.on_button.config(image=appFrame.off)
        appFrame.on_button.config(text="Buu")
        # appFrame.my_label.config(text="The Switch is XOff@", fg="grey")
        appFrame.is_on = False
    else:

        # appFrame.on_button.config(image=appFrame.on)
        appFrame.on_button.config(text="hivyhyh")
        # appFrame.my_label.config(text="The Switch is On@", fg="green")
        appFrame.is_on = True
def main():
    root = tk.Tk()
    root.geometry("500x300")
    root.title("Om/Off Toggle")

    app = SoundDesignGui(root)
    # app.on_button.config(command= lambda : ext_switch(app))
    app.on_button.config(command= lambda : app.test_command(lambda:ext_switch(app)))
    app.mainloop()

if __name__=="__main__":
    main()

"""
Elements to place:
* Start/Stop button
* Randomize scale + labels with name

* print current notes (+future bold on current)


* print content of queue
"""
