# Import Module
import tkinter as tk
# from tkinter.ttk import *
import tkinter.ttk as ttk
import inspect

class SoundDesignGui(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

        self.is_playing = True

        self.pack(side="top", fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.__label__()
        self.__pp_btn__()
        self.__scale_rnd_btn__()
        self.__test_button__()


    # def __label__(self):
    #     # Create Label
    #     self.my_label = tk.Label(self,
    #                      text="The Switch Is On!",
    #                      fg="green",
    #                      font=("Helvetica", 32))
    #
    #     self.my_label.pack(pady=20)


    def cmd_wrapper(func):
        def inner(self, *args, **kwargs):
            cmd_int = '__' + func.__name__ + '_cmd_int__'
            cmd_ext = func.__name__ + '_cmd_ext'
            cmd_full = func.__name__ + '_cmd'

            locals()[cmd_int] = lambda: print(cmd_int)
            locals()[cmd_ext] = lambda: print(cmd_ext)
            locals()[cmd_full] = lambda: print(cmd_full)

            def cmd(self_in):
                print(cmd.__name__)
                func_cmd_int = getattr(SoundDesignGui, cmd_int)
                func_cmd_ext = getattr(SoundDesignGui, cmd_ext)
                func_cmd_int()
                func_cmd_ext()

            func(self)
            setattr(SoundDesignGui, cmd_full, cmd.__name__)
        return inner


    def __pp_btn__(self):
        self.pp_btn_cmd_ext = lambda: print('pp_btn_cmd_ext')

        def __pp_btn_cmd__(self_in):
            self_in.__pp_btn_switch_cmd_int__()
            self_in.pp_btn_cmd_ext()
            pass

        self.pp_btn = tk.Button(self, text ="Play", command=lambda: __pp_btn_cmd__(self),
                                   height= 1, width=3)
        self.pp_btn.pack(padx=3, pady=2, side='left', anchor='nw')

    def __pp_btn_switch_cmd_int__(self):
        if self.is_playing:
            self.pp_btn.config(text="Pause")
            self.is_playing = False
        else:
            self.pp_btn.config(text="Play")
            self.is_playing = True


    def __scale_rnd_btn__(self):
        self.__scale_rnd_btn_cmd_int__ = lambda: print('__scale_rnd_btn_cmd_int__')
        self.scale_rnd_btn_cmd_ext = lambda: print('scale_rnd_btn_cmd_ext')

        def __scale_rnd_btn_cmd__(self_in):
            self_in.__scale_rnd_btn_cmd_int__()
            self_in.scale_rnd_btn_cmd_ext()
            pass


        self.scale_rnd_btn = tk.Button(self, text ="scale rnd", command=lambda: __scale_rnd_btn_cmd__(self),
                                          height= 1, width=7)
        self.scale_rnd_btn.pack(padx=4, pady=2, side='left', anchor='n')
        # ttk.Button()


    @cmd_wrapper
    def __test_button__(self):

        cmd_full = inspect.stack()[1][3] + '_cmd'
        cmd_func = getattr(SoundDesignGui, cmd_full)
        self.scale_rnd_btn = tk.Button(self, text ="xxx", command=lambda: cmd_func(self),
                                          height= 1, width=7)
        self.scale_rnd_btn.pack(padx=4, pady=2, side='left', anchor='n')


    def dummy_command(self):
        print('dummy')
        pass


    def test_command(self, func : callable):
    # def test_command(self):
        print('before')
        # func()
        self.pp_btn_cmd()
        print('after')
    # Define our switch function

def ext_switch(appFrame):
    # global is_on

    # Determine is on or off
    if appFrame.is_playing:
        # appFrame.on_btn.config(image=appFrame.off)
        appFrame.pp_btn.config(text="Buu")
        # appFrame.my_label.config(text="The Switch is XOff@", fg="grey")
        appFrame.is_playing = False
    else:

        # appFrame.on_btn.config(image=appFrame.on)
        appFrame.pp_btn.config(text="hivyhyh")
        # appFrame.my_label.config(text="The Switch is On@", fg="green")
        appFrame.is_playing = True

def ext_pressed():
    print('ext pressed')
def main():
    root = tk.Tk()
    root.geometry("500x300")
    root.title("Om/Off Toggle")

    app = SoundDesignGui(root)
    app.pp_btn_cmd_ext = lambda : ext_pressed()

    # app.btn_cmd_ext = lambda : ext_switch(app)
    # app.on_btn.config(command= lambda : ext_switch(app))
    # app.on_btn.config(command= lambda : app.test_command(lambda:ext_switch(app)))
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
