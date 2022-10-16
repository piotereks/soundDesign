# Import Module
import datetime
import tkinter as tk
# from tkinter.ttk import *
import tkinter.ttk as ttk
import inspect
from typing import Callable


class WrappingLabel(tk.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width(), width=self.winfo_width()))

class SoundDesignGui(ttk.Frame):
    # scale_rnd_btn_cmd_ext: Callable[[], None]
    scale_rnd_btn_cmd_ext: None

    def __init__(self, *args, **kwargs):

        self.is_playing = False
        self.metro_on = False

        ttk.Frame.__init__(self, *args, **kwargs)

        self.pack(side="top", fill="both", expand=True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=3)
        self.grid_columnconfigure(3, weight=3)
        # </editor-fold>

        self.__pp_btn__()
        self.__metro_btn__()
        self.__scale_rnd_btn__()
        self.__notes_and_queue__()
        self.__scale_combo__()
        self.__loop_queue_chk__()

        # <editor-fold desc="Description">
        col = 0
        row = 0

        self.pp_btn.grid(row=row, column= col , padx=5, pady=5,sticky = 'w')
        col += 1

        self.scale_rnd_btn.grid(row=row, column= col, padx=5, pady=5,sticky = 'W')
        col += 1

        self.scale_combo.grid(row=row, column=col , padx=5, pady=5, sticky = 'W')
        col += 1

        # self.scale_name_lbl.grid(row=row, column=col, padx=5, pady=5, ipadx=10,sticky = 'WE')
        # col += 1

        self.scale_set_name_lbl.grid(row=row, column=col,  pady=5, sticky ='W')
        col +=1

        row+=1
        col = 0

        self.metro_btn.grid(row=row, column=col, padx=5, pady=5, sticky ='w')
        col += 1

        row+=1
        col = 0

        self.loop_queue_chk.grid(row=row, column=col, padx=5, pady=5, sticky ='w')
        col += 1

        colsp = 1
        self.curr_notes_pair_lbl.grid(row=row, column=col, columnspan=colsp, padx=5, pady=5, sticky='E')
        col += colsp

        colsp =4
        self.queue_content_lbl.grid(row=row, column=col, columnspan=colsp, padx=5, pady=5, sticky='W')
        col += colsp

        row+=1
        col = 0

        colsp = 5
        self.check_notes_lbl.grid(row=row, column=col, columnspan=colsp, rowspan=2, padx=5, pady=5)
        col += colsp

        # </editor-fold>

    def __loop_queue_chk__(self):
        self.loop_queue_chk_cmd_ext = lambda: print('loop_queue_chk_cmd_ext')

        def __loop_queue_chk_cmd__(self_in):
            self_in.loop_queue_chk_cmd_ext()
            # self_in.__loop_queue_chk_switch_cmd_int__()
            pass
        self.loop_queue_on = tk.IntVar(self, 1)  # Default on

        self.loop_queue_chk = tk.Checkbutton(self, text="Loop Q",
                                        variable=self.loop_queue_on,
                                        onvalue=1, offvalue=0, height=2, width=10,
                                        command=lambda: __loop_queue_chk_cmd__(self))


    def __metro_btn__(self):
        self.metro_btn_cmd_ext = lambda: print('metro_btn_cmd_ext')

        def __metro_btn_cmd__(self_in):
            self_in.metro_btn_cmd_ext()
            # print('metro value:' ,self.metro_on.get())
            # self_in.__metro_btn_switch_cmd_int__()
            pass
        self.metro_on = tk.IntVar()
        self.metro_btn = tk.Checkbutton(self, text="Metronome",
                                        variable=self.metro_on,
                                        onvalue=1, offvalue=0, height=2, width=10,
                                        command=lambda: __metro_btn_cmd__(self))



    def __pp_btn__(self):
        self.pp_btn_cmd_ext = lambda: print('pp_btn_cmd_ext')

        def __pp_btn_switch_cmd_int__(self):

            if self.is_playing:
                # when was playing change to paused (is playing False) state now
                self.pp_btn.config(text="Play")
                self.is_playing = False
            else:
                self.pp_btn.config(text="Pause")
                self.is_playing = True

        def __pp_btn_cmd__(self_in):
            self_in.pp_btn_cmd_ext()
            __pp_btn_switch_cmd_int__(self)
            pass

        self.pp_btn = tk.Button(self, text ="Play", command=lambda: __pp_btn_cmd__(self),
                                   height= 1, width=10)
        # self.pp_btn.pack(padx=3, pady=2, side='left', anchor='nw')

    def __scale_combo__(self):
        self.__sscale_combo_cmd_int__ = lambda: print('_sscale_combo_cmd_int__')
        self.scale_combo_cmd_ext = lambda: print('scale_combo_cmd_ext')
        def __scale_combo_cmd__(self_in):
            # self_in.__scale_combo_cmd_int__()
            self_in.scale_combo_cmd_ext()
            pass

        self.scale_combo  = ttk.Combobox(self,
            state="readonly",
            values=["Python", "C", "C++", "Java"],
            postcommand=lambda : print('scale postcommand')
            ,width=25
        )
        # self.scale_combo.set('gurusuruz')
        print(self.scale_combo.get())

    def __scale_rnd_btn__(self):
        self.__scale_rnd_btn_cmd_int__ = lambda: print('__scale_rnd_btn_cmd_int__')
        self.scale_rnd_btn_cmd_ext = lambda: print('scale_rnd_btn_cmd_ext')

        def __scale_rnd_btn_cmd__(self_in):
            # self_in.__scale_rnd_btn_cmd_int__()
            self_in.scale_rnd_btn_cmd_ext()
            pass


        self.scale_rnd_btn = tk.Button(self, text ="rand() scale", command=lambda: __scale_rnd_btn_cmd__(self),
                                       height= 1, width=8)



        # self.scale_name_text = tk.StringVar()
        # self.scale_name_text.set("scale name")
        # self.scale_name_lbl = tk.Label(self, textvariable=self.scale_name_text, height= 1)

        self.scale_set_name_txt = tk.StringVar()
        self.scale_set_name_txt.set("scale name")
        self.scale_set_name_lbl = tk.Label(self, textvariable=self.scale_set_name_txt, height= 1, width=25)

    def __notes_and_queue__(self):
        self.curr_notes_pair_lbl_text = tk.StringVar()
        self.curr_notes_pair_lbl_text.set("curr_notes_pair_lbl_text")
        self.curr_notes_pair_lbl = tk.Label(self, textvariable=self.curr_notes_pair_lbl_text, height= 1)

        self.queue_content_lbl_text = tk.StringVar()
        self.queue_content_lbl_text.set("queue_content_lbl_text")
        self.queue_content_lbl = tk.Label(self, textvariable=self.queue_content_lbl_text, height= 1)

        self.check_notes_lbl_text = tk.StringVar()
        self.check_notes_lbl_text.set("check notes here")
        self.check_notes_lbl = WrappingLabel(self, textvariable=self.check_notes_lbl_text, height= 4)


def ext_pressed():
    print('ext pressed')
def main():
    root = tk.Tk()
    root.geometry("800x600")
    root.title("On/Off Toggle")

    app = SoundDesignGui(root)
    app.pp_btn_cmd_ext = lambda : ext_pressed()
    app.scale_rnd_btn_cmd_ext = lambda : app.scale_name_text.set(datetime.datetime.now().strftime('_%H%M%S'))


    app.mainloop()




if __name__=="__main__":
    main()

"""
Elements to place:
* select scale key (dropdown) + rand key
* (+future bold on current)
* future current notes to log (or rolling widget, but with some limited buffor)

* Align elements so they do not skip, when resize
* readonly combo

* rewrite functions to bind events
"""
