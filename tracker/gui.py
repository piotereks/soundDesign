# Import Module
import datetime
import tkinter as tk
# from tkinter.ttk import *
import tkinter.ttk as ttk
import inspect

class SoundDesignGui(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

        self.pack(side="top", fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.top_frame = ttk.Frame(self, width=400, height=200)
        self.top_frame.pack(side='top', fill='both', padx=10, pady=5, expand=True)

        self.mid_frame = ttk.Frame(self, width=450, height=300)
        self.mid_frame.pack(side='top', fill='both', padx=10, pady=5, expand=True)

        self.is_playing = False


        # self.__label__()
        self.__pp_btn__()
        self.__scale_rnd_btn__()


    # def __label__(self):
    #     # Create Label
    #     self.my_label = tk.Label(self,
    #                      text="The Switch Is On!",
    #                      fg="green",
    #                      font=("Helvetica", 32))
    #
    #     self.my_label.pack(pady=20)


    def __pp_btn__(self):
        self.pp_btn_cmd_ext = lambda: print('pp_btn_cmd_ext')

        def __pp_btn_cmd__(self_in):
            self_in.pp_btn_cmd_ext()
            self_in.__pp_btn_switch_cmd_int__()
            pass

        self.pp_btn = tk.Button(self.top_frame, text ="Play", command=lambda: __pp_btn_cmd__(self),
                                   height= 1, width=3)
        self.pp_btn.pack(padx=3, pady=2, side='left', anchor='nw')

    def __pp_btn_switch_cmd_int__(self):

        if self.is_playing:
            # when was playing change to paused (is playing False) state now
            self.pp_btn.config(text="Play")
            self.is_playing = False
        else:
            self.pp_btn.config(text="Pause")
            self.is_playing = True


    def __scale_rnd_btn__(self):
        self.__scale_rnd_btn_cmd_int__ = lambda: print('__scale_rnd_btn_cmd_int__')
        self.scale_rnd_btn_cmd_ext = lambda: print('scale_rnd_btn_cmd_ext')

        def __scale_rnd_btn_cmd__(self_in):
            # self_in.__scale_rnd_btn_cmd_int__()
            self_in.scale_rnd_btn_cmd_ext()
            pass

        # datetime.datetime.now().strftime('_%H%M%S')

        self.scale_rnd_btn = tk.Button(self.top_frame, text ="rand() scale", command=lambda: __scale_rnd_btn_cmd__(self),
                                          height= 1, width=8)
        self.scale_rnd_btn.pack(padx=3, pady=2, side='left', anchor='nw')

        self.scale_name_text = tk.StringVar()
        self.scale_name_text.set("scale name")
        self.scale_name_lbl = tk.Label(self.top_frame, textvariable=self.scale_name_text, height= 1)
        self.scale_name_lbl.pack(padx=3, pady=8, side='left', anchor='nw')

        self.scale_name_text2 = tk.StringVar()
        self.scale_name_text2.set("scale name")
        self.scale_name_lbl2 = tk.Label(self.top_frame, textvariable=self.scale_name_text2, height= 1)
        self.scale_name_lbl2.pack(padx=3, pady=8, side='left', anchor='nw')

        self.check_notes_lbl_text = tk.StringVar()
        self.check_notes_lbl_text.set("check notes here")
        self.check_notes_lbl = tk.Label(self.mid_frame, textvariable=self.check_notes_lbl_text, height= 1)
        self.check_notes_lbl.pack(padx=3, pady=8, side='top', anchor='w')


        # ttk.Button()

        # self.__scale_rnd_btn_cmd_int__ = lambda: self.scale_name_text.set(datetime.datetime.now().strftime('_X_%H%M%S'))

    def dummy_command(self):
        print('dummy')
        pass

def ext_pressed():
    print('ext pressed')
def main():
    root = tk.Tk()
    root.geometry("400x100")
    root.title("Om/Off Toggle")

    app = SoundDesignGui(root)
    app.pp_btn_cmd_ext = lambda : ext_pressed()
    app.scale_rnd_btn_cmd_ext = lambda : app.scale_name_text.set(datetime.datetime.now().strftime('_%H%M%S'))

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
^^^^ done

* print current notes (+future bold on current)
* future currnt notes to log (or rolling widget, but with some limited buffor)

* print content of queue
"""
