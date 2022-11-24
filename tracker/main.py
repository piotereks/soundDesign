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

# def sbtp():
#     my_tracker.beat = my_tracker.pplay


def rs():
    rand_scale()


def save_midi():
    my_tracker.save_midi()
    # my_tracker.midi_out.write()


def sbft(note_from = 60, note_to = 64):
    my_tracker.beat = lambda: my_tracker.play_from_to(note_from, note_to)

# </editor-fold>

# <editor-fold desc="wrk functions">
# def rel_pq():
#     """
#     Reload Play queue
#     """
#     notes_chain = [1, 4, 4, 2, 3, 4, 11, 5, 1, 0]
#     # [63, 65, 65, 63, 63, 65, 70, 65, 63, 60]
#     midi_notes_chain = list(np.array(notes_chain) + 60)
#     print(midi_notes_chain)
#
#     # to load queue
#     dummy = [my_tracker.note_queue.put(note) for note in midi_notes_chain]

def cmp():
    # print('expected:\n', my_tracker.expected_array)
    print('expected:\n', [y for x in my_tracker.pattern_array for y in list(x['note'])])
    print('played:\n', [x.note for x in my_tracker.midi_out.miditrack if x.type == 'note_on'])
def put_in_queue(note):
    print('test_put_queue: ',note)
    # my_tracker.note_queue.put(note)
    my_tracker.put_to_queue(note)


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


def metro_on_off():
    log_call()
    app.metro_on.set((app.metro_on.get())+1%2)
    my_tracker.metro_start_stop(app.metro_on)


def rand_play_funct():
    log_call()
    selected_function=random.choice(
        list(set(my_tracker.patterns.pattern_methods_short_list) - set([app.play_func_combo.get()]))
    )
    app.play_func_combo.set(selected_function)
    my_tracker.patterns.set_pattern_function(selected_function)
    # my_tracker.midi_out.miditrack.append(mido.MetaMessage('text', text=f"funcR: {app.play_func_combo.get()}"))
    # my_tracker.meta_func(func=app.play_func_combo.get())



def rand_key():
    log_call()
    # app.keys_group.set(random.choice(app.names))
    app.keys_group.set(random.choice(
        list(set(app.names)-set([app.keys_group.get()]))
        ))
    keys_scale_action(app.keys_group.get(), my_tracker.key.scale.name)
    # my_tracker.meta_key_scale(key=app.keys_group.get(),scale=app.scale_combo.get())


def rand_scale():
    log_call()
    all_scales=[scale.name for scale in iso.Scale.all()]
    random_scale = random.choice(list(set(all_scales)-set([my_tracker.key.scale.name])))
    # my_tracker.key = iso.Key(my_tracker.key.tonic, iso.Scale.random())
    my_tracker.key = iso.Key(my_tracker.key.tonic, random_scale)
    # app.keys_group.set(random.choice(
    #     set(app.names)-set(app.keys_group.get())
    #     ))

    app.scale_combo.set(my_tracker.key.scale.name)
    # my_tracker.meta_key_scale(key=app.keys_group.get(),scale=app.scale_combo.get())


def set_scale(event):
    log_call()
    scale_obj =  iso.Scale.byname(app.scale_combo.get())
    my_tracker.key = iso.Key(my_tracker.key.tonic, scale_obj)
    # my_tracker.meta_key_scale(key=app.keys_group.get(),scale=app.scale_combo.get())


def set_key():
    log_call()
    keys_scale_action(app.keys_group.get(), my_tracker.key.scale.name)
    # my_tracker.meta_key_scale(key=app.keys_group.get(),scale=app.scale_combo.get())
    # print(f"{app.keys_group.get()}")


def set_play_func(event):
    log_call()
    # my_tracker.patterns.get_pattern.__name__ = app.play_func_combo.get()
    # my_tracker.patterns.get_pattern = getattr(my_tracker.patterns,
    #                                           'get_'+app.play_func_combo.get()+'_pattern')
    my_tracker.patterns.set_pattern_function(app.play_func_combo.get())
    # my_tracker.midi_out.miditrack.append(mido.MetaMessage('text', text=f"func: {app.play_func_combo.get()}"))
    # my_tracker.meta_func(func=app.play_func_combo.get())


def set_tempo(tempo):
    log_call()
    my_tracker.set_tempo(tempo)
    my_tracker.meta_tempo(tempo=tempo)

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


    # app.key_rnd_btn_cmd_ext = lambda: keys_scale_action(app.keys_group.get(), my_tracker.key.scale.name)
    # app.key_radio_cmd_ext = lambda: keys_scale_action(app.keys_group.get(), my_tracker.key.scale.name)
    app.key_rnd_btn_cmd_ext = lambda: set_key()
    app.key_radio_cmd_ext = lambda: set_key()

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


    app.tempo_h_scale_cmd_ext = lambda  tempo :  set_tempo(tempo)
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