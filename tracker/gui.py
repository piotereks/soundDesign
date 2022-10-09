# Import Module
import datetime
import tkinter as tk
# from tkinter.ttk import *
import tkinter.ttk as ttk
import inspect

class WrappingLabel(tk.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width(), width=self.winfo_width()))

class SoundDesignGui(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)


        self.pack(side="top", fill="both", expand=True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=3)
        self.grid_rowconfigure(3, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=2)
        self.grid_columnconfigure(3, weight=2)

        # self.top_frame = tk.Frame(self, width=450, height=200, bg ="green")
        # self.top_frame.grid_columnconfigure(0, weight=1)
        # self.top_frame.grid_columnconfigure(1, weight=2)
        # # self.top_frame.pack(side='top', fill='both', padx=10, pady=5, expand=True)
        # self.top_frame.grid(row=0, column=0, padx=5, pady=5)
        #
        # self.top_right_frame = tk.Frame(self.top_frame, width=266, height=200)
        # self.top_right_frame.grid(row=0, column=1, padx=5, pady=5)

        # self.mid_frame = tk.Frame(self, width=450, height=300, bg ="yellow")
        # self.mid_frame.grid_rowconfigure(0, weight=1)
        # self.mid_frame.grid_rowconfigure(1, weight=3)
        #
        # self.mid_frame.grid_columnconfigure(0, weight=1)
        # # self.mid_frame.pack(side='top', fill='both', padx=10, pady=5, expand=True)
        # self.mid_frame.grid(row=1, column=0, padx=5, pady=5)
        # self.test_frame = tk.Frame(self, padx=10, pady=5, bg ="blue")

        self.is_playing = False
        self.metro_on = False


        # self.__label__()
        self.__pp_btn__()
        self.__metro_btn__()
        self.__scale_rnd_btn__()


    # def __label__(self):
    #     # Create Label
    #     self.my_label = tk.Label(self,
    #                      text="The Switch Is On!",
    #                      fg="green",
    #                      font=("Helvetica", 32))
    #
    #     self.my_label.pack(pady=20)

    def __metro_btn__(self):
        self.metro_btn_cmd_ext = lambda: print('metro_btn_cmd_ext')

        def __metro_btn_cmd__(self_in):
            self_in.metro_btn_cmd_ext()
            # self_in.__metro_btn_switch_cmd_int__()
            pass
        self.metro_on = tk.IntVar()
        self.metro_btn = tk.Checkbutton(self, text="Metronome",
                                        variable=self.metro_on,
                                        onvalue=1, offvalue=0, height=2, width=10,
                                        command=lambda: __metro_btn_cmd__(self))


        self.metro_btn.grid(row=0, column=4, padx=5, pady=5, sticky ='W')

    def __pp_btn__(self):
        self.pp_btn_cmd_ext = lambda: print('pp_btn_cmd_ext')

        def __pp_btn_cmd__(self_in):
            self_in.pp_btn_cmd_ext()
            self_in.__pp_btn_switch_cmd_int__()
            pass

        self.pp_btn = tk.Button(self, text ="Play", command=lambda: __pp_btn_cmd__(self),
                                   height= 1, width=3)
        # self.pp_btn.pack(padx=3, pady=2, side='left', anchor='nw')
        self.pp_btn.grid(row=0, column=0, padx=5, pady=5,sticky = 'W')


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

        self.scale_rnd_btn = tk.Button(self, text ="rand() scale", command=lambda: __scale_rnd_btn_cmd__(self),
                                       height= 1, width=8)
        self.scale_rnd_btn.grid(row=0, column=1, padx=5, pady=5, ipadx=10,sticky = 'W')
        # self.scale_rnd_btn.pack(padx=3, pady=2, side='left', anchor = 'w')


        self.scale_name_text = tk.StringVar()
        self.scale_name_text.set("scale name")
        self.scale_name_lbl = tk.Label(self, textvariable=self.scale_name_text, height= 1)
        self.scale_name_lbl.grid(row=0, column=2, padx=5, pady=5, ipadx=10,sticky = 'WE')
        # self.scale_name_lbl.pack(padx=3, pady=2, side='left', anchor = 'w')

        self.scale_name_text2 = tk.StringVar()
        self.scale_name_text2.set("scale name")
        self.scale_name_lbl2 = tk.Label(self, textvariable=self.scale_name_text2, height= 1)
        self.scale_name_lbl2.grid(row=0, column=3, padx=5, pady=5, ipadx=10,sticky = 'WE')
        # self.scale_name_lbl2.pack(padx=3, pady=2, side='left', anchor = 'w')

        self.curr_notes_pair_lbl_text = tk.StringVar()
        self.curr_notes_pair_lbl_text.set("curr_notes_pair_lbl_text")
        self.curr_notes_pair_lbl = tk.Label(self, textvariable=self.curr_notes_pair_lbl_text, height= 1)
        self.curr_notes_pair_lbl.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky='E')

        self.queue_content_lbl_text = tk.StringVar()
        self.queue_content_lbl_text.set("queue_content_lbl_text")
        self.queue_content_lbl = tk.Label(self, textvariable=self.queue_content_lbl_text, height= 1)
        self.queue_content_lbl.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='W')

        # self.test_frame.grid(row=2, column=0, columnspan=4, rowspan=2, padx=5, pady=5)
        self.check_notes_lbl_text = tk.StringVar()
        self.check_notes_lbl_text.set("check notes here")
        # self.check_notes_lbl = WrappingLabel(self.test_frame, textvariable=self.check_notes_lbl_text, height= 4)
        self.check_notes_lbl = WrappingLabel(self, textvariable=self.check_notes_lbl_text, height= 4)
        self.check_notes_lbl.grid(row=3, column=0, columnspan=4, rowspan=2, padx=5, pady=5)
        # self.check_notes_lbl.pack(fill='both', padx=10, pady=5, expand=True )
        # .pack(side='top', fill='both', padx=10, pady=5, expand=True)
        # ttk.Button()

        # self.__scale_rnd_btn_cmd_int__ = lambda: self.scale_name_text.set(datetime.datetime.now().strftime('_X_%H%M%S'))

    def dummy_command(self):
        print('dummy')
        pass

def ext_pressed():
    print('ext pressed')
def main():
    root = tk.Tk()
    root.geometry("400x250")
    root.title("On/Off Toggle")

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
* metronome start/stop (ensure sync) - change to radio


* Start/Stop button
* Randomize scale + labels with name
^^^^ done

* print current notes
^^^^ done

* (+future bold on current)
* future current notes to log (or rolling widget, but with some limited buffor)

* print content of queue
^^^ done
"""
