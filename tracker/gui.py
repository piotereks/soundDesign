# Import Module
import tkinter as tk
# from tkinter.ttk import *
import tkinter.ttk as ttk

class SoundDesignGui(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

        self.is_playing = True

        self.pack(side="top", fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.__label__()
        self.__button__()
        self.__scale_rnd_button__()


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
        self.pp_button = tk.Button(self, text ="Play", command=self.pp_button_command,
                                   height= 1, width=3)
        self.pp_button_command_ext = lambda: print('button_command_ext')

        self.pp_button.pack(pady=2, side='left', anchor='nw')
        # ttk.Button()

    def __scale_rnd_button__(self):
        # Define Our Images
        # self.on = tk.PhotoImage(file="on.png")
        # self.off = tk.PhotoImage(file="off.png")
        self.scale_rnd_button = tk.Button(self, text ="scale rnd", command=self.dummy_command,
                                          height= 1, width=7)
        self.pp_button_command_ext = lambda: print('button_command_ext')

        self.scale_rnd_button.pack(padx=5, pady=2, side='left', anchor='n')
        # ttk.Button()


    def dummy_command(self):
        print('dummy')
        pass
    def pp_button_command(self):
        self.__pp_button_switch__()
        self.pp_button_command_ext()
        pass

    def test_command(self, func : callable):
    # def test_command(self):
        print('before')
        # func()
        self.pp_button_command()
        print('after')
    # Define our switch function
    def __pp_button_switch__(self):
        # global is_on

        # Determine is on or off
        if self.is_playing:
            # self.on_button.config(image=self.off)
            self.pp_button.config(text="Pause")
            # self.my_label.config(text="The Switch is Off@", fg="grey")
            self.is_playing = False
        else:

            # self.on_button.config(image=self.on)
            self.pp_button.config(text="Play")
            # self.my_label.config(text="The Switch is On@", fg="green")
            self.is_playing = True

def ext_switch(appFrame):
    # global is_on

    # Determine is on or off
    if appFrame.is_playing:
        # appFrame.on_button.config(image=appFrame.off)
        appFrame.pp_button.config(text="Buu")
        # appFrame.my_label.config(text="The Switch is XOff@", fg="grey")
        appFrame.is_playing = False
    else:

        # appFrame.on_button.config(image=appFrame.on)
        appFrame.pp_button.config(text="hivyhyh")
        # appFrame.my_label.config(text="The Switch is On@", fg="green")
        appFrame.is_playing = True

def ext_pressed():
    print('ext pressed')
def main():
    root = tk.Tk()
    root.geometry("500x300")
    root.title("Om/Off Toggle")

    app = SoundDesignGui(root)
    app.pp_button_command_ext = lambda : ext_pressed()

    # app.button_command_ext = lambda : ext_switch(app)
    # app.on_button.config(command= lambda : ext_switch(app))
    # app.on_button.config(command= lambda : app.test_command(lambda:ext_switch(app)))
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
