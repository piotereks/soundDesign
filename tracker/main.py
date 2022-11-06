import isobar

from tracker import *
from patterns import *
from gui import *
# from pynput import keyboard
from keyboard import *
global IN_COLAB
IN_COLAB = 'google.colab' in sys.modules
global label_str
global app
# app = None


# <editor-fold desc="Interactive simplification functions">
def tracker_dec(func):
    def inner():
        global my_tracker
        # print(func.__name__)
        new_func = getattr(my_tracker, func.__name__)
        # print('new func: ',new_func)
        new_func()
    return inner

@tracker_dec
def ts():
    pass

@tracker_dec
def tstart():
    pass

def mstart():
    my_tracker.metronome_start()

def mstop():
    my_tracker.metronome_stop()



def sbt1():
    my_tracker.beat = my_tracker.beat1


def sbt2():
    my_tracker.beat = my_tracker.beat2


def sbtn():
    my_tracker.beat = my_tracker.beat_none


def sbtt():
    my_tracker.beat = my_tracker.beat_test

def sbtp():
    my_tracker.beat = my_tracker.pplay

def sbtn():
    my_tracker.pplay_new()

def sbpq():
    my_tracker.pplay_queue()

def rs():
    rand_scale()


def save_midi():
    my_tracker.save_midi()
    # my_tracker.midi_out.write()

# def xxxrand_scale():
#     # my_tracker.scale = iso.Scale.random()
#     my_tracker.key = iso.Key(iso.key.tonic, iso.Scale.random())

def sbft(note_from = 60, note_to = 64):
    my_tracker.beat = lambda: my_tracker.play_from_to(note_from, note_to)

# </editor-fold>

# <editor-fold desc="wrk functions">
def rel_pq():
    """
    Reload Play queue
    """
    notes_chain = [1, 4, 4, 2, 3, 4, 11, 5, 1, 0]
    # [63, 65, 65, 63, 63, 65, 70, 65, 63, 60]
    midi_notes_chain = list(np.array(notes_chain) + 60)
    print(midi_notes_chain)

    # to load queue
    dummy = [my_tracker.note_queue.put(note) for note in midi_notes_chain]

def cmp():
    # print('expected:\n', my_tracker.expected_array)
    print('expected:\n', [y for x in my_tracker.pattern_array for y in list(x['note'])])
    print('played:\n', [x.note for x in my_tracker.midi_out.miditrack if x.type == 'note_on'])
def put_in_queue(note):
    print('test_put_queue: ',note)
    # my_tracker.note_queue.put(note)
    my_tracker.put_to_queue(note)


def old_main():
    global my_tracker
    log_call()
    # iso.util.midi_note_to_note_name=midi_note_to_note_name  # Overwritte original function
    intervals_chain = [1, 3,    -2, 1, 1, 7, -6, -4, -1] # fix in random_pattern zero interval
                       # [3, 0, -2, 1, 1, 7, -6, -4, -1, 1]
                #[1, 3,  0,-2, 1, 1, 7, -6, -4, -1]
    # self.midi_note_array2:     [61, 64, 64, 62, 63, 64, 71, 65, 61, 60]
    # self.midi_note_array2 cvt: [62, 64, 64, 62, 64, 64, 70, 65, 62, 60]

    notes_chain = [1, 4, 4, 2, 3, 4, 11, 5, 1, 0]
                #[63, 65, 65, 63, 63, 65, 70, 65, 63, 60]
    midi_notes_chain = list(np.array(notes_chain)+60)
    print(midi_notes_chain)

    # to load queue
    # dummy = [my_tracker.note_queue.put(note) for note in midi_notes_chain]

    print(sum(intervals_chain))
    # midi_out_flag = Tracker.MIDI_OUT_FILE
    # midi_out_flag = Tracker.MIDI_OUT_DEVICE
    # midi_out_flag = Tracker.MIDI_OUT_DUMMY


    # my_tracker = Tracker(interval_array=intervals_chain, midi_out_flag=midi_out_flag)
    my_tracker = Tracker(midi_note_array=midi_notes_chain, note_array=notes_chain, midi_out_mode=midi_out_flag)
    dummy = [my_tracker.note_queue.put(note) for note in midi_notes_chain]

    # keys = "q2w3er5t6y7ui9o0p[=]"

    # notepad_scale()
    # uuu=[iso.Scale([int(aaa) - 1 for aaa in xxx[1].split()[:-1]], xxx[2]) for xxx in notepad if xxx[0] == "Scale"]
    # Collect events until released
    # with keyboard.Listener(
    #         on_press=on_press,
    #         on_release=on_release) as listener:
    #     listener.join()
    sbft(None,None)
    # Keyboard(lambda x : xxx(x))
    Keyboard(lambda note : put_in_queue(note))
# These are work in progress debug functions
def find_scale_dups():
    import itertools
    # cmp_scales = [(set(prd[0][1].semitones), set(prd[1][1].semitones)) for prd in itertools.product(enumerate(iso.Scale.all()), enumerate(iso.Scale.all()))
    #               if prd[0][0] > prd[1][0]]
    cmp_scales = [(prd[0][1].name, set(prd[0][1].semitones), prd[1][1].name, set(prd[1][1].semitones)) for prd in itertools.product(enumerate(iso.Scale.all()), enumerate(iso.Scale.all()))
                  if prd[0][0] > prd[1][0] and set(prd[0][1].semitones) == set(prd[1][1].semitones)]
    for cscale in cmp_scales:
        print(cscale)

    # for i, scale in enumerate(iso.Scale.all()):
    #     print(i,scale)
    # p.itertools.product(iso.scales.all())
    # [(x.name, x.semitones) for x in iso.Scale.all()]

def dump_scales():
    all_scales=[(scale.semitones, scale.name ) for scale in iso.Scale.all()]
    all_scales_sorted =sorted(all_scales, key=lambda i: i[0])
    print(*all_scales_sorted, sep='\n')

# </editor-fold>


# ...or, in a non-blocking fashion:
# listener = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)
# listener.start()
# print('processing Done')

def rand_play_funct():
    selected_function=random.choice(my_tracker.patterns.pattern_methods_short_list)
    # my_tracker.patterns.get_pattern.__name__ = selected_function
    # my_tracker.patterns.get_pattern = getattr(my_tracker.patterns, 'get_'+selected_function+'_pattern' )
    # my_tracker.patterns.get_pattern = getattr(my_tracker.patterns,
    #                                           'get_'+app.play_func_combo.get()+'_pattern')
    app.play_func_combo.set(selected_function)
    my_tracker.patterns.set_pattern_function(selected_function)

def metro_on_off():
    app.metro_on.set((app.metro_on.get())+1%2)
    my_tracker.metro_start_stop(app.metro_on)

def rand_key():
    app.keys_group.set(random.choice(app.names))
    keys_scale_action(app.keys_group.get(), my_tracker.key.scale.name)


def rand_scale():
    my_tracker.key = iso.Key(my_tracker.key.tonic, iso.Scale.random())
    app.scale_combo.set(my_tracker.key.scale.name)

def set_scale(event):
    scale_obj =  iso.Scale.byname(app.scale_combo.get())
    my_tracker.key = iso.Key(my_tracker.key.tonic, scale_obj)


def set_play_func(event):
    # my_tracker.patterns.get_pattern.__name__ = app.play_func_combo.get()
    # my_tracker.patterns.get_pattern = getattr(my_tracker.patterns,
    #                                           'get_'+app.play_func_combo.get()+'_pattern')
    my_tracker.patterns.set_pattern_function(app.play_func_combo.get())


def play_pause():
    global app
    log_call()

    if app.is_playing:
        ts()
    else:
        tstart()
    pass


def keys_scale_action(key, scale):
    log_call()
    scale_obj = iso.Scale.byname(scale)
    my_tracker.key = iso.Key(key,  scale_obj)
    # my_tracker.scale = scale_obj


def run_gui():
    global app
    root = tk.Tk()
    root.geometry("800x600")
    root.title("soundDesign - pattern player")

    # for t in range(600,0,-1):
    #     print(f"xx: {t}")
    #     my_tracker.set_tempo(t)

    app = SoundDesignGui(root)


    app.key_rnd_btn_cmd_ext = lambda: keys_scale_action(app.keys_group.get(), my_tracker.key.scale.name)
    app.key_radio_cmd_ext = lambda: keys_scale_action(app.keys_group.get(), my_tracker.key.scale.name)

    app.metro_btn_cmd_ext = lambda: my_tracker.metro_start_stop(app.metro_on)
    app.loop_queue_chk_cmd_ext = lambda: my_tracker.loop_play_queue_action(app.loop_queue_on.get())
    my_tracker.loopq = app.loop_queue_on.get()

    app.play_func_rnd_btn_cmd_ext = lambda: rand_play_funct()
    app.play_func_combo['values'] = my_tracker.patterns.pattern_methods_short_list
    app.play_func_combo.set(my_tracker.patterns.pattern_methods_short_list[0])
    app.play_func_combo.bind("<<ComboboxSelected>>", set_play_func)


    app.save_midi_btn_cmd_ext = lambda: save_midi()


    app.pp_btn_cmd_ext = lambda: play_pause()

    app.scale_rnd_btn_cmd_ext = lambda: rand_scale()
    app.scale_combo['values'] = sorted([scale.name for scale in iso.Scale.all()])
    app.scale_combo.set(my_tracker.key.scale.name)
    app.scale_combo.bind("<<ComboboxSelected>>", set_scale)


    app.tempo_h_scale_cmd_ext = lambda  tempo :  my_tracker.set_tempo(tempo)
    app.set_scale(app.tempo_h_scale, from_=40, to=300, value=120)


    my_tracker.scale_name_action = lambda: app.scale_set_name_txt.set('set:' + my_tracker.key.scale.name)
    my_tracker.check_notes_action = lambda: app.check_notes_lbl_text.set(my_tracker.check_notes)
    my_tracker.queue_content_action = lambda: app.queue_content_lbl_text.set('queue: '+str(my_tracker.get_queue_content())
                                            + ' from to: '+str(my_tracker.notes_pair))
    my_tracker.curr_notes_pair_action = lambda: app.curr_notes_pair_lbl_text.set('from to: '+str(my_tracker.notes_pair))
    my_tracker.fullq_content_action = lambda: app.fullq_content_lbl_text.set('full queue: '+str(my_tracker.get_queue_content_full()))

    keyboard.key_z_function = lambda : app.pp_btn_cmd()
    # keyboard.key_space_function = lambda : play_pause()
    keyboard.key_x_function = lambda: metro_on_off()
    keyboard.key_c_function = lambda : print("key c")
    keyboard.key_v_function = lambda : print("key v")
    keyboard.key_b_function = lambda : rand_scale()
    keyboard.key_n_function = lambda : rand_key()
    # keyboard.key_n_function = lambda : print("keyx n")
    keyboard.key_m_function = lambda : rand_play_funct()



    # print('---------------------'+ str(a_list))
    # my_tracker.check_notes_action =
    app.mainloop()
    #clearnup gui functions to prevent gui exceptions after its closing
    my_tracker.scale_name_action = lambda: print(None)
    my_tracker.check_notes_action = lambda: print(None)
    my_tracker.queue_content_action = lambda: print(None)
    my_tracker.curr_notes_pair_action = lambda: print(None)
    my_tracker.loop_play_queue_action = lambda: print(None)
    my_tracker.fullq_content_action = lambda: print(None)

# see for GUI layouts :https://www.pythonguis.com/faq/pack-place-and-grid-in-tkinter/

def main():
    global app
    global my_tracker
    global keyboard
    log_call()
    # midi_out_flag = Tracker.MIDI_OUT_DEVICE
    midi_out_flag = Tracker.MIDI_OUT_MIX_FILE_DEVICE
    # midi_out_flag = Tracker.MIDI_OUT_FILE
    my_tracker = Tracker(midi_out_mode=midi_out_flag)


    keyboard = Keyboard(lambda note: put_in_queue(note))
    # sbpq()
    # ts()  # make by  default not starting
    run_gui()
    ts()
    save_midi()



if __name__ == '__main__':
    # print('Do we start?')
    # old_main()
    main()
    print('Processing Done.')

"""
nice scales https://jguitar.com/scale/E/Ionian
"""