import math
from itertools import chain

from tracker import *
from patterns import *
from gui import *

global IN_COLAB
IN_COLAB = 'google.colab' in sys.modules
global label_str


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import (StringProperty, ListProperty, ObjectProperty, NumericProperty, OptionProperty)

from kivy.uix.screenmanager import (ScreenManager, Screen, NoTransition,
                                    SlideTransition, CardTransition, SwapTransition,
                                    FadeTransition, WipeTransition, FallOutTransition, RiseInTransition)
from kivy.core.window import Window


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
def tstop():
    pass


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



def save_midi(on_exit=False):
    my_tracker.save_midi(on_exit=on_exit)
    # my_tracker.midi_out.write()


def sbft(note_from=60, note_to=64):
    my_tracker.beat = lambda: my_tracker.play_from_to(note_from, note_to)


# </editor-fold>

# <editor-fold desc="wrk functions">


def cmp():
    # print('expected:\n', my_tracker.expected_array)
    print('expected:\n', [y for x in my_tracker.pattern_array for y in list(x['note'])])
    print('played:\n', [x.note for x in my_tracker.midi_out.miditrack if x.type == 'note_on'])


def put_in_queue(note):
    print('test_put_queue: ', note)
    # my_tracker.note_queue.put(note)
    my_tracker.put_to_queue(note)


def find_scale_dups():
    import itertools

    cmp_scales = [(prd[0][1].name, set(prd[0][1].semitones), prd[1][1].name, set(prd[1][1].semitones)) for prd in
                  itertools.product(enumerate(iso.Scale.all()), enumerate(iso.Scale.all()))
                  if prd[0][0] > prd[1][0] and set(prd[0][1].semitones) == set(prd[1][1].semitones)]
    for cscale in cmp_scales:
        print(cscale)



def dump_scales():
    all_scales = [(scale.semitones, scale.name) for scale in iso.Scale.all()]
    all_scales_sorted = sorted(all_scales, key=lambda i: i[0])
    print(*all_scales_sorted, sep='\n')


# </editor-fold>





def set_scale_mn(scale_name):
    log_call()
    scale_obj = iso.Scale.byname(scale_name)
    my_tracker.key = iso.Key(my_tracker.key.tonic, scale_obj)




def keys_scale_action(key, scale):
    log_call()
    scale_obj = iso.Scale.byname(scale)
    my_tracker.key = iso.Key(key, scale_obj)
    # my_tracker.scale = scale_obj


def main():
    global my_tracker
    # global keyboard
    log_call()
    config_file = 'main_config.json'

    with open(config_file, 'r') as file:
        loaded_config = json.load(file)
        app_config = loaded_config['app']
        tracker_config = loaded_config['tracker']
        midi_mapping = loaded_config.get('midi_mapping')

    # midi_out_flag = Tracker.MIDI_OUT_DEVICE
    midi_out_flag = Tracker.MIDI_OUT_MIX_FILE_DEVICE
    # midi_out_flag = Tracker.MIDI_OUT_FILE

    my_tracker = Tracker(tracker_config=tracker_config, midi_mapping=midi_mapping, midi_out_mode=midi_out_flag)
    # my_tracker.midi_out.program_change(program=22)


    TrackerApp(parm_rows=12, parm_cols=5, app_config=app_config).run()

    # cleanup attempt
    my_tracker.scale_name_action = lambda: print(None)
    my_tracker.check_notes_action = lambda: print(None)
    my_tracker.queue_content_action = lambda: print(None)
    my_tracker.curr_notes_pair_action = lambda: print(None)
    my_tracker.fullq_content_action = lambda: print(None)

    my_tracker.set_tempo_action = lambda: print(None)
    my_tracker.set_dur_variety_action = lambda: print(None)
    my_tracker.set_play_action = lambda: print(None)
    my_tracker.set_metronome_action = lambda: print(None)
    my_tracker.set_loop_action = lambda: print(None)
    my_tracker.set_clearq_action = lambda: print(None)

    my_tracker.set_rnd_scale_action = lambda: print(None)
    my_tracker.set_rnd_key_action = lambda: print(None)
    my_tracker.set_rnd_func_action= lambda: print(None)







    ts()
    save_midi(on_exit=True)


class RadioButton(ToggleButtonBehavior, BoxLayout):
    text = StringProperty('')
    def on_state(self, *args, **kwargs):
        print("overloaded on_state for RadioButton")
        # self.state='down'
    # state = StringProperty('normal')
    pass


class ScaleButton(ToggleButtonBehavior, BoxLayout):
    text = StringProperty('')
    raw_text = ListProperty('')
    pass


class TrackerApp(App):
    # to be inititalized from config.json
    parm_rows = NumericProperty()
    parm_cols = NumericProperty()

    parm_scale = StringProperty()
    parm_tempo = NumericProperty()
    parm_tempo_min = NumericProperty()
    parm_tempo_max = NumericProperty()

    parm_dur_variety = NumericProperty()
    parm_dur_variety_min = NumericProperty()
    parm_dur_variety_max = NumericProperty()

    path_queue_content = ListProperty()


    scale_values = ListProperty()
    scale_set_name_txt = StringProperty()
    selected_root_note = StringProperty()
    selected_quantize = StringProperty()
    selected_quantize_state = StringProperty()
    selected_align = StringProperty()
    func_init_text = StringProperty()
    func_values = ListProperty()

    check_notes_lbl_text = StringProperty('test1 test2')

    queue_content_lbl_text = StringProperty()
    curr_notes_pair_lbl_text = StringProperty()
    fullq_content_lbl_text = StringProperty()
    prev_key = None

    selected_scale_button = StringProperty()

    app_config = ObjectProperty()
    tempo_value = NumericProperty(120.0)
    tempo_min = NumericProperty(40)
    tempo_max = NumericProperty(300)

    dur_variety_value = NumericProperty(120.0)
    dur_variety_min = NumericProperty(40)
    dur_variety_max = NumericProperty(300)


    def on_start(self):
        self.__config_init_file__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, None)

        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.loop_play(instance=None, state=self.root.ids.main_scr.ids.loopq_button.state)
        my_tracker.metro_start_stop(self.root.ids.main_scr.ids.metronome.state)
        all_scales = sorted([scale.name for scale in iso.Scale.all()])
        self.selected_scale_button = my_tracker.key.scale.name

        self.scale_values = all_scales
        self.func_values = my_tracker.note_patterns.pattern_methods_short_list
        self.func_init_text = self.func_init_text if self.func_init_text else \
            my_tracker.note_patterns.pattern_methods_short_list[0]

        my_tracker.scale_name_action = lambda: self.set_scale_set_name_txt('set:' + my_tracker.key.scale.name)
        my_tracker.check_notes_action = lambda: self.set_check_notes_lbl_text(str(my_tracker.check_notes))

        my_tracker.queue_content_action = lambda: self.set_queue_content_lbl_text(
            'queue: ' + str(my_tracker.get_queue_content()))
        my_tracker.curr_notes_pair_action = lambda: self.set_curr_notes_pair_lbl_text(
            'from to: ' + str(my_tracker.notes_pair))
        my_tracker.fullq_content_action = lambda: self.set_fullq_content_lbl_text(
            'full queue: ' + str(my_tracker.get_queue_content_full()))

        my_tracker.set_tempo_action = lambda: self.set_tempo_f_main(None, tempo_knob=my_tracker.midi_mapping['set_tempo_knob'])
        my_tracker.set_dur_variety_action = lambda: self.set_dur_variety_f_main(None, dur_variety_knob=my_tracker.midi_mapping['set_dur_variety_knob'])
        my_tracker.set_play_action = lambda: self.set_play_pause_state(
            play_pause_button=my_tracker.midi_mapping['play'])
        my_tracker.set_metronome_action = lambda: self.set_metronome_state(
            metronome_button=my_tracker.midi_mapping['metronome'])
        my_tracker.set_loop_action = lambda: self.set_loop_state(loop_button=my_tracker.midi_mapping['loop'])
        my_tracker.set_clearq_action = lambda: self.set_clearq_state(clearq_button=my_tracker.midi_mapping['clearq'])

        my_tracker.set_rnd_scale_action = lambda: self.rand_scale()
        my_tracker.set_rnd_key_action = lambda: self.rand_key()
        my_tracker.set_rnd_func_action= lambda: self.rand_play_func()

        self.tempo_value = self.parm_tempo
        self.tempo_min = self.parm_tempo_min
        self.tempo_max = self.parm_tempo_max

        self.dur_variety_value = self.parm_dur_variety
        self.dur_variety_min = self.parm_dur_variety_min
        self.dur_variety_max = self.parm_dur_variety_max

    def __config_init_file__(self):
        default_app_config = \
            {
                "key": "C",
                "scale": "major",
                "tempo": 110,
                "tempo_min": 15,
                "tempo_max": 312,
                "play_func": "one_note",
                "rows": 8,
                "cols": 4
            }


        default_app_config.update(self.app_config)

        self.app_config = default_app_config


        self.set_kv_key(self.app_config.get("key"), self.app_config.get("scale"))
        self.selected_scale_button = self.app_config.get("scale")


        if self.app_config.get("tempo"):
            self.parm_tempo = self.app_config.get("tempo")
        if self.app_config.get("tempo_min"):
            self.parm_tempo_min = self.app_config.get("tempo_min")
        if self.app_config.get("tempo_max"):
            self.parm_tempo_max = self.app_config.get("tempo_max")

        if self.app_config.get("dur_variety"):
            self.parm_dur_variety = self.app_config.get("dur_variety")
        if self.app_config.get("dur_variety_min"):
            self.parm_dur_variety_min = self.app_config.get("dur_variety_min")
        if self.app_config.get("dur_variety_max"):
            self.parm_dur_variety_max = self.app_config.get("dur_variety_max")


        if self.app_config.get("play_func"):
            self.func_init_text = self.app_config.get("play_func")
        if self.app_config.get("queue_content"):
            self.path_queue_content = self.app_config.get("queue_content")

        if self.app_config.get("rows"):
            self.parm_rows = self.app_config.get("rows")

        if self.app_config.get("cols"):
            self.parm_cols = self.app_config.get("cols")

        for note in self.path_queue_content or []:
            put_in_queue(note)



    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_up(self, keyboard, keycode):
        self.prev_key = None
        key = keycode[1]
        print(f'{key} released')

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        play_keys = "q2w3er5t6y7ui9o0p[=]"

        if keycode[1] == self.prev_key:
            return True
        print(f"{keycode[1]=} pressed {keycode}")
        self.prev_key = keycode[1]
        if not keycode[1]:
            pass
        elif keycode[1] == 'z':
            self.inv_play_pause()
        elif keycode[1] == 'x':
            self.inv_metro_on_off()
        elif keycode[1] == 'c':
            self.clear_q()
        elif keycode[1] == 'v':
            self.inv_loop_play()
        elif keycode[1] == 'b':
            self.rand_scale()
        elif keycode[1] == 'n':
            self.rand_key()
        elif keycode[1] == 'm':
            self.rand_play_func()
        elif keycode[1] == 'escape':
            if self.root.current == 'scales_option':
                # self.root.transition.direction = 'down'
                self.root.current = 'main_screen'
                self.root.ids.scales_opt.rem_buttons()
                print('return to main screen')
            else:
                print('close application')
                self.close_application()
        elif keycode[1] in play_keys:
            put_in_queue(play_keys.index(keycode[1]) + 60)

        return True



    def close_application(self):
        # closing application
        App.get_running_app().stop()
        Window.close()

    def inv_play_pause(self):
        state = self.root.ids.main_scr.ids.start_stop_button.state
        to_state = 'normal' if state == 'down' else 'down'
        self.root.ids.main_scr.ids.start_stop_button.state = to_state


    def inv_metro_on_off(self):
        state = self.root.ids.main_scr.ids.metronome.state
        to_state = 'normal' if state == 'down' else 'down'
        self.root.ids.main_scr.ids.metronome.state = to_state

    def inv_loop_play(self):
        state = self.root.ids.main_scr.ids.loopq_button.state
        to_state = 'normal' if state == 'down' else 'down'
        self.root.ids.main_scr.ids.loopq_button.state = to_state


    def set_loop_state(self, loop_button=None):
        if not loop_button:
            return
        state = loop_button.get('state')
        if state:
            self.root.ids.main_scr.ids.loopq_button.state = state

    def set_clearq_state(self, clearq_button=None):
        if not clearq_button:
            return
        my_tracker.clear_queue()

    def set_metronome_state(self, metronome_button=None):
        if not metronome_button:
            return
        state = metronome_button.get('state')
        if state:
            self.root.ids.main_scr.ids.metronome.state = state

    def set_play_pause_state(self, play_pause_button=None):
        if not play_pause_button:
            return
        state = play_pause_button.get('state')
        if state:
            self.root.ids.main_scr.ids.start_stop_button.state = state

    def play_pause(self, instance, state=None, play_pause_button=None):
        log_call()
        if play_pause_button:
            state = play_pause_button['state']
        print(f"{instance=}, {state=}")
        tstart() if state == 'down' else tstop()


    def metro_on_off(self, instance, state):
        log_call()
        my_tracker.metro_start_stop(state)

    def loop_play(self, instance, state):
        my_tracker.loopq = True if state == 'down' else False


    def clear_q(self):
        log_call()
        my_tracker.clear_queue()

    def save(self):
        my_tracker.save_midi()

    def set_scale_app(self, instance, scale_name):
        log_call()
        set_scale_mn(scale_name)  # TODO review this

    def set_scale_set_name_txt(self, value):
        self.scale_set_name_txt = value

    def set_check_notes_lbl_text(self, value):
        self.check_notes_lbl_text = value

    def set_queue_content_lbl_text(self, value):
        self.queue_content_lbl_text = value

    def set_curr_notes_pair_lbl_text(self, value):
        self.curr_notes_pair_lbl_text = value

    def set_fullq_content_lbl_text(self, value):
        self.fullq_content_lbl_text = value

    def rand_scale(self):
        log_call()
        all_scales = [scale.name for scale in iso.Scale.all()]
        random_scale = random.choice(list(set(all_scales) - set([my_tracker.key.scale.name])))
        my_tracker.key = iso.Key(my_tracker.key.tonic, random_scale)
        self.selected_scale_button = my_tracker.key.scale.name

    def on_selected_root_note(self, instance, root_note):
        log_call()
        print(f'this is selected root note {root_note}, {instance=}')
        keys_scale_action(root_note, my_tracker.key.scale.name)

    def selected_quantize_and_state(self, instance, quantize):
        log_call()
        print(f'this is selected quantize {quantize}, {instance=}')
        print("-----------------==========-: ", self.root.quants_state)
        print("-----------------==========-x-: ",  {x.text: x.children[0].state for x in self.root.quant_buttons})

        my_tracker.quants_state = {x.text: x.children[0].state for x in self.root.quant_buttons}
        # my_tracker.quants_state = self.root.quants_state
        # keys_scale_action(quantize, my_tracker.key.scale.name)

    def on_selected_quantize(self, instance, quantize):
        log_call()
        self.selected_quantize_and_state(instance, quantize)


    def on_selected_quantize_state(self, instance, quantize):
        log_call()
        self.selected_quantize_and_state(instance, quantize)


    def on_selected_align(self, instance, align):
        log_call()
        print(f'xxxxxxxxxxxxxxxxx this is selected align {align}, {instance=}')
        my_tracker.align_state = align
        # keys_scale_action(align, my_tracker.key.scale.name)

    def set_kv_key(self, new_key, new_scale = None):
        if not new_scale:
            new_scale = my_tracker.key.scale.name
        for key in self.root.ids.main_scr.ids.scales_group.children:
            print(f"{key.text=} != {new_key}  {key.text != new_key=}")
            if key.text != new_key:
                key.children[0].state = 'normal'
                key.state =  'normal'
                print("key set normal")
                continue

            key.children[0].state = 'down'
            key.state = 'down'
            print("key set down")
            print(my_tracker.key)

        self.selected_root_note = new_key




    def rand_key(self):
        keys = list({key.text for key in self.root.ids.main_scr.ids.scales_group.children} \
                    - {self.selected_root_note})
        randomized_key = random.choice(keys)
        print(f'this is {randomized_key=}')
        print(my_tracker.key)
        self.set_kv_key(randomized_key)

    def set_play_func(self, instance, func_name):
        log_call()
        print('func_name:', func_name)
        # print(instance)
        my_tracker.note_patterns.set_pattern_function(func_name)
        my_tracker.func_name = func_name
        # my_tracker.meta_func(func=f"{func_name}")

    def rand_play_func(self):
        log_call()
        selected_function = random.choice(
            list(set(my_tracker.note_patterns.pattern_methods_short_list) - set([self.func_init_text]))
        )
        self.func_init_text = selected_function
        my_tracker.note_patterns.set_pattern_function(selected_function)

    def set_tempo_f_main(self, instance, tempo=None, tempo_knob=None):
        log_call()

        if not tempo:
            if tempo_knob['knob_type']=='abs':
                tempo = tempo_knob['value']
                tempo = self.tempo_min+tempo*(self.tempo_max-self.tempo_min)/127
            else:
                # tempo_increment = tempo_knob['inc_value']
                tempo_increment = tempo_knob['inc_value'] * tempo_knob['ratio'] if tempo_knob['ratio'] \
                    else tempo_knob['inc_value']
                # tempo = int(round(self.tempo_value + tempo_increment))
                tempo = self.tempo_value + tempo_increment

            print(f"bef: {self.tempo_value}")
            if tempo > self.tempo_max:
                tempo = self.tempo_max
            elif tempo < self.tempo_min:
                tempo = self.tempo_min
        self.tempo_value = tempo
        print(f"aft: {self.tempo_value=}")
        my_tracker.set_tempo_trk(round(tempo))

    def set_dur_variety_f_main(self, instance, dur_variety=None, dur_variety_knob=None):
        log_call()
        print(f"{dur_variety=},{dur_variety_knob=}")
        if dur_variety is None:
            if dur_variety_knob['knob_type'] == 'abs':
                dur_variety = dur_variety_knob['value']
                dur_variety = self.dur_variety_min+dur_variety*(self.dur_variety_max-self.dur_variety_min)/127
            else:
                # dur_variety_increment = dur_variety_knob['inc_value']
                dur_variety_increment = dur_variety_knob['inc_value'] * dur_variety_knob['ratio'] if dur_variety_knob['ratio'] \
                    else dur_variety_knob['inc_value']
                # dur_variety = int(round(self.dur_variety_value + dur_variety_increment))
                dur_variety = self.dur_variety_value + dur_variety_increment

            print(f"bef: {self.dur_variety_value}")
            if dur_variety > self.dur_variety_max:
                dur_variety = self.dur_variety_max
            elif dur_variety < self.dur_variety_min:
                dur_variety = self.dur_variety_min
        self.dur_variety_value = dur_variety
        print(f"aft: {self.dur_variety_value=}")
        my_tracker.dur_variety = dur_variety
        # my_tracker.set_dur_variety_trk(dur_variety)


    def on_selected_scale_button(self, instance, value):
        print(instance, value)
        print(self.selected_scale_button)
        self.set_scale_app(instance, value)



    def close_application(self):
        # closing application
        App.get_running_app().stop()
        Window.close()


class MainScreen(Screen):
    pass


class ScalesSelectScreen(Screen):


    btn = ObjectProperty()
    button_matrix = ListProperty()


    grid_rows = NumericProperty()
    grid_cols = NumericProperty()
    grid_len = NumericProperty()


    grid_pos = ListProperty()
    last_grid_up_down = StringProperty()

    but_id_offset = 0



    def __init__(self, **kwargs):
        super(ScalesSelectScreen, self).__init__(**kwargs)
        print(f"{self.grid_cols=}, {self.grid_rows=},{self.grid_cols=}")

        self.__read_config_file__()
        self.button_names = [button_id['name'] for button_id in self.patterns_config['scales'] if button_id['name']]
        self.nbr_of_scales = len(self.button_names)

    def __read_config_file__(self):
        # print('reading config')
        config_file = 'reviewed_pattern_cfg.json'


        with open(config_file, 'r') as file:

            self.patterns_config = json.load(file)

    def populate_button(self):


        for button_id in self.button_names[self.but_id_offset:self.but_id_offset + self.grid_len]:

            button_text = button_id
            btn = ScaleButton(raw_text=button_text)
            if self.selected_scale in button_text:
                btn.state = 'down'

            self.button_matrix.append(btn)
            self.ids.button_grid.add_widget(btn)

        print('----------------')

    pass

    def rem_buttons(self):
        for button in self.button_matrix:
            self.ids.button_grid.remove_widget(button)

    def scale_page(self, direction=None, scale='major'):
        if direction in ('RL', 'prev'):
            self.rem_buttons()
            self.but_id_offset -= self.grid_len
            if self.but_id_offset < 0:
                self.but_id_offset = 0
        elif direction in ('LR', 'next'):
            self.rem_buttons()
            if self.but_id_offset + self.grid_len < self.nbr_of_scales:
                self.but_id_offset += self.grid_len

        else:
            for x in range(0, len(self.button_names), self.grid_len):
                # if scale  in self.button_names[x:x+self.grid_len]:
                if scale in list(chain(*self.button_names[x:x + self.grid_len])):
                    self.but_id_offset = x
                    break


        self.populate_button()

    def on_touch_down(self, touch):
        self.last_grid_up_down = 'down'
        print(f"down , {touch.px=}, {touch.py=}, {touch.pos=}")
        self.grid_pos = touch.pos


    def on_touch_up(self, touch):
        prev_last_grid_up_down = self.last_grid_up_down
        self.last_grid_up_down = 'up'

        if not self.grid_pos or self.grid_pos == []:
            self.grid_pos = touch.pos
            return True
        print(f"up,  {touch.px=}, {touch.py=}, {touch.pos=}")

        print(f"{self.grid_pos[0]=},{touch.x=}, {self.grid_pos[0]-touch.x=}")
        if prev_last_grid_up_down == 'down':  # to filter out accidental up-up
            if self.grid_pos[0] - touch.x > 50:
                print('>>>>>>>next')
                self.scale_page(direction='next')
            if self.grid_pos[0] - touch.x < -50:
                print('prev<<<<<<<')
                self.scale_page(direction='prev')
            if pow(self.grid_pos[0] - touch.x, 2) + pow(self.grid_pos[1] - touch.y, 2) <= 100:
                print('>>>>>>>equal<<<<<<<')
                self.grid_pos = touch.pos
                return super(ScalesSelectScreen, self).on_touch_down(touch)
            self.grid_pos = touch.pos


if __name__ == '__main__':
    main()
    print('Processing Done.')
