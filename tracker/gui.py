# Import Module
import datetime
import tkinter as tk
# from tkinter.ttk import *
import tkinter.ttk as ttk
import inspect
import random
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
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=3)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
        # </editor-fold>

        self.__pp_btn_init__()
        self.__metro_btn_init__()
        self.__scale_rnd_btn_init__()
        self.__notes_and_queue_init__()
        self.__scale_combo_init__()
        self.__loop_queue_chk_init__()
        self.__keys__rad_btn_init__()
        self.__tempo_h_scale_init__()
        self.__play_func_combo_init__()


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
        colsp=5
        self.keys_frm.grid(row=row, column=col, columnspan=colsp,  pady=5, sticky='N')

        row+=1
        col = 0

        self.metro_rad.grid(row=row, column=col, padx=5, pady=5, sticky ='wn')
        col += 1

        self.tempo_frm.grid(row=row, column=col, padx=5, pady=5, sticky ='wn')
        col += 1

        self.play_funct_frm.grid(row=row, column=col, padx=5, pady=5, sticky ='wn')
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

        row += 1
        col = 0
        colsp =4
        self.fullq_content_lbl.grid(row=row, column=col, columnspan=colsp, padx=5, pady=1, sticky='N')
        col += colsp


        row+=1
        col = 0

        colsp = 5
        self.check_notes_lbl.grid(row=row, column=col, columnspan=colsp, rowspan=2, padx=5, pady=1, sticky='N')
        col += colsp

        # </editor-fold>

    def __loop_queue_chk_init__(self):
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


    def __metro_btn_init__(self):
        self.metro_btn_cmd_ext = lambda: print('metro_btn_cmd_ext')

        def __metro_btn_cmd__(self_in):
            self_in.metro_btn_cmd_ext()
            # print('metro value:' ,self.metro_on.get())
            # self_in.__metro_btn_switch_cmd_int__()
            pass
        self.metro_on = tk.IntVar()
        self.metro_rad = tk.Checkbutton(self, text="Metronome",
                                        variable=self.metro_on,
                                        onvalue=1, offvalue=0, height=2, width=10,
                                        command=lambda: __metro_btn_cmd__(self))

    def __keys__rad_btn_init__(self):
        def __key_rnd_btn__(self_in):
            self.__key_rnd_btn_cmd_int__ = lambda: print('__key_rnd_btn_cmd_int__')
            self.key_rnd_btn_cmd_ext = lambda: print('key_rnd_btn_cmd_ext')

            def __key_rnd_btn_cmd__(self_in_2):
                # self_in.__key_rnd_btn_cmd_int__()
                self.keys_group.set(random.choice(names))
                self.key_rnd_btn_cmd_ext()
                pass

            self.key_rnd_btn = tk.Button(self_in, text ="rnd key", command=lambda: __key_rnd_btn_cmd__(self),
                                           height= 1, width=8)

        self.__key_radio_cmd_int__ = lambda: print('__key_radio_cmd_int__')
        self.key_radio_cmd_ext = lambda: print('key_radio_cmd_ext')

        def __key_radio_cmd__(self_in):
            # self_in.__key_radio_cmd_int__()
            self_in.key_radio_cmd_ext()
            pass

        names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self.keys_frm = ttk.Frame(self)
        __key_rnd_btn__(self.keys_frm)
        self.key_rnd_btn.grid(row=0, column=0, padx=10)
        label = ttk.Label(self.keys_frm, text='keys:').grid(row=0, column=1, ipadx=2)
        self.keys_group = tk.StringVar(self.keys_frm, names[0])

        for (value, text) in enumerate(names):
            ttk.Radiobutton(self.keys_frm, text=text, variable=self.keys_group,
                            value=text, command=lambda: __key_radio_cmd__(self) ).grid(row=0, column=value+2, padx=2)





    def __pp_btn_init__(self):
        self.pp_btn_cmd_ext = lambda: print('pp_btn_cmd_ext')

        def __pp_btn_switch_cmd_int__():

            if self.is_playing:
                # when was playing change to paused (is playing False) state now
                self.pp_btn.config(text="Play")
                self.is_playing = False
            else:
                self.pp_btn.config(text="Pause")
                self.is_playing = True

        def __pp_btn_cmd__():
            self.pp_btn_cmd_ext()
            __pp_btn_switch_cmd_int__()
            pass

        self.pp_btn = tk.Button(self, text ="Play", command=lambda: __pp_btn_cmd__(),
                                   height= 1, width=10)
        # self.pp_btn.pack(padx=3, pady=2, side='left', anchor='nw')

    def __scale_combo_init__(self):
        self.__sscale_combo_cmd_int__ = lambda: print('__scale_combo_cmd_int__')
        self.scale_combo_cmd_ext = lambda: print('scale_combo_cmd_ext')
        def __scale_combo_cmd__(self_in):
            # self_in.__scale_combo_cmd_int__()
            self_in.scale_combo_cmd_ext()
            pass

        self.scale_combo  = ttk.Combobox(self,
            state="readonly",
            values=["Python", "C", "C++", "Java"],
            postcommand=lambda: print('scale postcommand')
            ,width=25
        )
        # self.scale_combo.set('gurusuruz')
        print(self.scale_combo.get())


    def __scale_rnd_btn_init__(self):
        # self.__scale_rnd_btn_cmd_int__ = lambda: print('__scale_rnd_btn_cmd_int__')
        self.scale_rnd_btn_cmd_ext = lambda: print('scale_rnd_btn_cmd_ext')

        def __scale_rnd_btn_cmd__():
            # self_in.__scale_rnd_btn_cmd_int__()
            self.scale_rnd_btn_cmd_ext()
            pass


        self.scale_rnd_btn = tk.Button(self, text ="rnd scale", command=lambda: __scale_rnd_btn_cmd__(),
                                       height= 1, width=8)

        # def __pp_btn_cmd__():
        #     self.pp_btn_cmd_ext()
        #     __pp_btn_switch_cmd_int__()
        #     pass
        #
        # self.pp_btn = tk.Button(self, text ="Play", command=lambda: __pp_btn_cmd__(),
        #                            height= 1, width=10)

        # self.scale_name_text = tk.StringVar()
        # self.scale_name_text.set("scale name")
        # self.scale_name_lbl = tk.Label(self, textvariable=self.scale_name_text, height= 1)

        self.scale_set_name_txt = tk.StringVar()
        self.scale_set_name_txt.set("scale name")
        self.scale_set_name_lbl = tk.Label(self, textvariable=self.scale_set_name_txt, height= 1, width=25)

    def __notes_and_queue_init__(self):
        self.curr_notes_pair_lbl_text = tk.StringVar()
        self.curr_notes_pair_lbl_text.set("curr_notes_pair_lbl_text")
        self.curr_notes_pair_lbl = tk.Label(self, textvariable=self.curr_notes_pair_lbl_text, height= 1)

        self.queue_content_lbl_text = tk.StringVar()
        self.queue_content_lbl_text.set("queue_content_lbl_text")
        self.queue_content_lbl = tk.Label(self, textvariable=self.queue_content_lbl_text, height= 1)

        self.fullq_content_lbl_text = tk.StringVar()
        self.fullq_content_lbl_text.set("fullq_content_lbl_text")
        self.fullq_content_lbl = tk.Label(self, textvariable=self.fullq_content_lbl_text, height= 1)

        self.check_notes_lbl_text = tk.StringVar()
        self.check_notes_lbl_text.set("check notes here")
        self.check_notes_lbl = WrappingLabel(self, textvariable=self.check_notes_lbl_text, height= 3)

    def __tempo_h_scale_init__(self):
        self.tempo_h_scale_cmd_ext = lambda x: print('tempo_h_scale_cmd_ext')

        def __tempo_h_scale_switch_cmd_int__(position):
            print("__tempo_h_scale_switch_cmd_int__")


        def __tempo_h_scale_cmd__(position):
            # print(position)
            self.tempo_h_scale_cmd_ext(position)
            # __tempo_h_scale_switch_cmd_int__(position)
            pass
        self.tempo_frm = ttk.Frame(self)
        # tempo_val = tk.DoubleVar()
        # tempo_val.set(50)
        self.tempo_h_scale = tk.Scale(self.tempo_frm, command=lambda pos: __tempo_h_scale_cmd__(pos),
                                      #variable=tempo_val,
                   from_=1, to=100, orient=tk.HORIZONTAL)
        self.tempo_h_scale.set(22)
        self.tempo_h_scale.pack(side="top")

        print(self.tempo_h_scale.config)

    def set_scale(self, scale : ttk.Scale, from_=None, to=None, value=None):
        if from_:
            scale.config(from_=from_)
        if to:
            scale.config(to= to)
        if value:
            scale.set(value)

    def __play_func_combo_init__(self):
        self.play_funct_frm = ttk.Frame(self)

        self.play_func_combo_lbl = tk.Label(self.play_funct_frm, text="play func", height=1)
        self.play_func_combo_lbl.pack(side="top")

        self.play_func_combo = ttk.Combobox(self.play_funct_frm,
            state="readonly",
            values=["func1", "func2", "func3", "func4"],
            postcommand=lambda: print('play func postcommand')
            ,width=25
        )
        self.play_func_combo.set("func1")
        self.play_func_combo.pack(side="top")



def ext_pressed():
    print('ext pressed')
def main():
    root = tk.Tk()
    root.geometry("800x600")
    root.title("On/Off Toggle")

    app = SoundDesignGui(root)
    app.pp_btn_cmd_ext = lambda: ext_pressed()
    app.scale_rnd_btn_cmd_ext = lambda: app.scale_set_name_txt.set(datetime.datetime.now().strftime('_%H%M%S'))


    app.mainloop()




if __name__=="__main__":
    main()

"""
Elements to place:
* tempo knob
* dropdown for play functions
* save midi functionality on exit

* select scale key (dropdown) + rand key - done
* (+future bold on current)
* future current notes to log (or rolling widget, but with some limited buffer)

* Align elements so they do not skip, when resize
* readonly combo - done
* combo - is it possible with search?

* rewrite functions to bind events

Play functions
* duration patterns
* velocity patterna
* different modes of play (not only random)  - (later make it selectable)
    * shortest way (by my self or via existing function)
    * fixed length 
    * different lengths (combined)
    *      
"""
