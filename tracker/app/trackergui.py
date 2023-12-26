from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import (StringProperty, ListProperty, ObjectProperty, NumericProperty)
from kivy.uix.screenmanager import (Screen)
from kivy.core.window import Window

import isobar as iso
import random
import os
import json
from itertools import chain

from .log_call import *


class RadioButton(ToggleButtonBehavior, BoxLayout):
    text = StringProperty('')
    child_state = StringProperty('')

    def on_state(self, *args, **kwargs):
        print("overloaded on_state for RadioButton")
        print(*args)
        print(**kwargs)
        print(f"{self.child_state=}")
    pass


class ScaleButton(ToggleButtonBehavior, BoxLayout):
    text = StringProperty('')
    raw_text = ListProperty('')
    pass


class TrackerGuiApp(App):

    # <editor-fold desc="Properties">
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

    time_sig_beat_val = StringProperty('time sig/beat')
    tempo_value = NumericProperty(120.0)
    tempo_min = NumericProperty(40)
    tempo_max = NumericProperty(300)

    dur_variety_value = NumericProperty(120.0)
    dur_variety_min = NumericProperty(40)
    dur_variety_max = NumericProperty(300)

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
    selected_scale_button = StringProperty()

    app_config = ObjectProperty()
    tracker_ref = ObjectProperty()

    prev_key = None
    # </editor-fold>

    # <editor-fold desc="Initialization">
    def __set_prop__(self, variable, file_property):
        if self.app_config.get(file_property) is not None:
            setattr(self, variable, self.app_config.get(file_property))

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

        self.set_key_state(self.app_config.get("key"), self.app_config.get("scale"))
        # print("al: ",  [al.children[0].text for al in self.root.align_buttons if al.children[0].state == 'down'][0])
        self.on_selected_align(None,  [al.text for al in self.root.align_buttons if al.children[0].state == 'down'][0])
        self.on_selected_quantize(None, {q.text:q.children[0].state for q in self.root.quant_buttons})
        self.selected_scale_button = self.app_config.get("scale")

        properties = \
            [
                ('parm_tempo', "tempo"),
                ('parm_tempo_min', "tempo_min"),
                ('parm_tempo_max', "tempo_max"),
                ('parm_dur_variety', "dur_variety"),
                ('parm_dur_variety_min', "dur_variety_min"),
                ('parm_dur_variety_max', "dur_variety_max"),
                ('func_init_text', "play_func"),
                ('path_queue_content', "queue_content"),
                ('parm_rows', "rows"),
                ('parm_cols', "cols")
            ]
        # xxx = [self.__set_prop__(prop[0],prop[1]) for prop in properties]
        list(map(lambda prop: self.__set_prop__(prop[0],prop[1]), properties))
        if hasattr(self.tracker_ref, 'patterns_from_file'):
            if self.tracker_ref.patterns_from_file:
                print(self.tracker_ref.patterns_from_file)
                setattr(self, 'path_queue_content', [None]*4)

        for note in self.path_queue_content or []:
            self.tracker_ref.put_to_queue(note)

    def on_start(self):
        self.__config_init_file__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, None)

        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)



        # Play Button
        self.tracker_ref.set_play_action = lambda: self.set_play_pause_state(
            play_pause_button=self.tracker_ref.midi_mapping['play'])

        # Save Button
        # Scales
        all_scales = sorted([scale.name for scale in iso.Scale.all()])
        self.selected_scale_button = self.tracker_ref.key.scale.name
        self.scale_values = all_scales
        self.tracker_ref.scale_name_action = lambda: self.set_scale_set_name_txt('set:' + self.tracker_ref.key.scale.name)
        self.tracker_ref.set_rnd_scale_action = lambda: self.rand_scale()

        # Key
        self.tracker_ref.set_rnd_key_action = lambda: self.rand_key()

        # Metronome
        self.tracker_ref.metro_start_stop(self.root.metronome.state)
        self.tracker_ref.set_metronome_action = lambda: self.set_metronome_state(
            metronome_button=self.tracker_ref.midi_mapping['metronome'])
        # time signature
        self.time_sig_beat_val=f"ts: {self.tracker_ref.time_signature['numerator']}/{self.tracker_ref.time_signature['denominator']}, beat:0"

        # Tempo
        self.tracker_ref.set_tempo_action = lambda: self.set_tempo_f_main(None, tempo_knob=self.tracker_ref.midi_mapping['set_tempo_knob'])
        # self.tracker_ref.set_tempo_ui =  self.set_tempo_f_main
        # self.tracker_ref.set_tempo_val_ui = lambda: self.set_tempo_val_ui(None, tempo_knob=self.tracker_ref.midi_mapping['set_tempo_knob'])
        self.tempo_value = self.parm_tempo
        self.tempo_min = self.parm_tempo_min
        self.tempo_max = self.parm_tempo_max
        # self.tracker_ref.set_tempo_callback =  self.tracker_ref.set_tempo_ui
        # self.tracker_ref.file_input_device.set_tempo_callback = lambda tempo: print(f"this is tempo for callbackx {tempo=}")
        if hasattr(self.tracker_ref, 'file_input_device'):
            self.tracker_ref.file_input_device.set_tempo_callback = lambda tempo: self.set_tempo_f_main(instance=None, tempo=tempo)
        #
        # Time signature and beat action
        self.tracker_ref.time_sig_beat_val_action \
            = lambda: self.set_time_sig_beat_lbl(self.tracker_ref.time_signature, self.tracker_ref.beat_count+1)

        # Play functions
        self.func_values = self.tracker_ref.note_patterns.pattern_methods_short_list
        self.func_init_text = self.func_init_text if self.func_init_text else \
            self.tracker_ref.note_patterns.pattern_methods_short_list[0]
        self.tracker_ref.set_rnd_func_action = lambda: self.rand_play_func()

        # Duration variety
        self.tracker_ref.set_dur_variety_action = lambda: self.set_dur_variety_f_main(None, dur_variety_knob=self.tracker_ref.midi_mapping['set_dur_variety_knob'])
        self.dur_variety_value = self.parm_dur_variety
        self.dur_variety_min = self.parm_dur_variety_min
        self.dur_variety_max = self.parm_dur_variety_max

        # Quantize
        self.tracker_ref.set_clearq_action = lambda: self.set_clearq_state(clearq_button=self.tracker_ref.midi_mapping['clearq'])

        # Align
        # LoopQ
        self.loopq_action(instance=None, state=self.root.loopq.state)
        self.tracker_ref.set_loopq_action = lambda: self.set_loopq_state(
            loopq_button=self.tracker_ref.midi_mapping['loop'])

        # ClearQ
        # Queue
        self.tracker_ref.check_notes_action = lambda: self.set_check_notes_lbl_text(str(self.tracker_ref.check_notes))
        self.tracker_ref.queue_content_action = lambda: self.set_queue_content_lbl_text(
            'queue: ' + str(self.tracker_ref.get_queue_content()))
        self.set_queue_content_lbl_text(
            'queue: ' + str(self.tracker_ref.get_queue_content()))
        self.tracker_ref.curr_notes_pair_action = lambda: self.set_curr_notes_pair_lbl_text(
            'from to: ' + str(self.tracker_ref.notes_pair))
        self.tracker_ref.fullq_content_action = lambda: self.set_fullq_content_lbl_text(
            'full queue: ' + str(self.tracker_ref.get_queue_content_full()))
        self.set_fullq_content_lbl_text(
            'full queue: ' + str(self.tracker_ref.get_queue_content_full()))


    def close_application(self):
        # cleanup attempt
        self.tracker_ref.set_play_action = lambda: print(None)
        self.tracker_ref.scale_name_action = lambda: print(None)
        self.tracker_ref.set_rnd_scale_action = lambda: print(None)
        self.tracker_ref.set_rnd_key_action = lambda: print(None)

        self.tracker_ref.set_metronome_action = lambda: print(None)
        self.tracker_ref.time_sig_beat_val_action = lambda: print(None)
        self.tracker_ref.set_tempo_action = lambda: print(None)
        self.tracker_ref.set_rnd_func_action = lambda: print(None)
        if hasattr(self.tracker_ref, 'file_input_device'):
            self.tracker_ref.file_input_device.set_tempo_callback = lambda: print(None)

        self.tracker_ref.set_dur_variety_action = lambda: print(None)

        self.tracker_ref.set_loopq_action = lambda: print(None)
        self.tracker_ref.set_clearq_action = lambda: print(None)

        self.tracker_ref.check_notes_action = lambda: print(None)
        self.tracker_ref.queue_content_action = lambda: print(None)
        self.tracker_ref.curr_notes_pair_action = lambda: print(None)
        self.tracker_ref.fullq_content_action = lambda: print(None)

        self.tracker_ref.tstop()
        self.tracker_ref.save_midi(on_exit=True)

        # closing application
        App.get_running_app().stop()
        Window.close()
    # </editor-fold>

    # <editor-fold desc="Keyboard functions">
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
            self.inv_play_pause_state()
        elif keycode[1] == 'x':
            self.inv_metro_on_off_state()
        elif keycode[1] == 'c':
            self.clearq_action()
        elif keycode[1] == 'v':
            self.inv_loopq_play_state()
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
            self.tracker_ref.put_to_queue(play_keys.index(keycode[1]) + 60)

        return True
    # </editor-fold>

    # <editor-fold desc="Play Pause Button">
    def inv_play_pause_state(self):
        state = self.root.start_stop.state
        to_state = 'normal' if state == 'down' else 'down'
        self.root.start_stop.state = to_state
    def set_play_pause_state(self, play_pause_button=None):
        if not play_pause_button:
            return
        state = play_pause_button.get('state')
        if state:
            self.root.start_stop.state = state

    def play_pause_action(self, instance, state=None, play_pause_button=None):
        log_call()
        if play_pause_button:
            state = play_pause_button['state']
        print(f"{instance=}, {state=}")
        self.tracker_ref.tstart() if state == 'down' else self.tracker_ref.tstop()
    # </editor-fold>

    def set_time_sig_beat_lbl(self, time_sig, value):
        label = f"ts: {time_sig['numerator']}/{time_sig['denominator']} beat:{value}"
        self.time_sig_beat_val = label

    # <editor-fold desc="Save Button">
    def save_midi(self, on_exit=False):
        self.tracker_ref.save_midi(on_exit=on_exit)
    # </editor-fold>

    # <editor-fold desc="Scales functionality">
    def on_selected_scale_button(self, instance, value):
        print(instance, value)
        print(self.selected_scale_button)
        self.set_scale_nm(value)
    def rand_scale(self):
        log_call()
        all_scales = [scale.name for scale in iso.Scale.all()]
        random_scale = random.choice(list(set(all_scales) - {self.tracker_ref.key.scale.name}))
        self.tracker_ref.key = iso.Key(self.tracker_ref.key.tonic, random_scale)
        self.selected_scale_button = self.tracker_ref.key.scale.name
    def keys_scale_action(self, key, scale):
        log_call()
        scale_obj = iso.Scale.byname(scale)
        self.tracker_ref.key = iso.Key(key, scale_obj)

    def set_scale_nm(self, scale_name):
        log_call()
        scale_obj = iso.Scale.byname(scale_name)
        self.tracker_ref.key = iso.Key(self.tracker_ref.key.tonic, scale_obj)

    def set_scale_set_name_txt(self, value):
        self.scale_set_name_txt = value


    # </editor-fold>

    # <editor-fold desc="Key functionality">
    def on_selected_root_note(self, instance, root_note):
        log_call()
        print(f'this is selected root note {root_note}, {instance=}')
        self.keys_scale_action(root_note, self.tracker_ref.key.scale.name)

    def set_key_state(self, new_key, new_scale = None):
        if not new_scale:
            new_scale = self.tracker_ref.key.scale.name
        for key in self.root.scales_buttons:
            print(f"{key.text=} != {new_key}  {key.text != new_key=}")
            if key.text != new_key:
                key.children[0].state = 'normal'
                key.state = 'normal'
                print("key set normal")
                continue

            key.children[0].state = 'down'
            key.state = 'down'
            print("key set down")
            print(self.tracker_ref.key)

        self.selected_root_note = new_key
    def rand_key(self):
        keys = list({key.text for key in self.root.scales_buttons} \
                    - {self.selected_root_note})
        randomized_key = random.choice(keys)
        print(f'this is {randomized_key=}')
        print(self.tracker_ref.key)
        self.set_key_state(randomized_key)
    # </editor-fold>

    # <editor-fold desc="Metronome">
    def set_metronome_state(self, metronome_button=None):
        if not metronome_button:
            return
        state = metronome_button.get('state')
        if state:
            self.root.metronome.state = state

    def inv_metro_on_off_state(self):
        state = self.root.metronome.state
        to_state = 'normal' if state == 'down' else 'down'
        self.root.metronome.state = to_state

    def metro_on_off_action(self, instance, state):
        log_call()
        self.tracker_ref.metro_start_stop(state)
    # </editor-fold>

    # <editor-fold desc="Tempo">
    # @snoop
    def set_tempo_f_main(self, instance, tempo=None, tempo_knob=None):
        log_call()

        if not tempo:
            if tempo_knob['knob_type']=='abs':
                tempo = tempo_knob['value']
                tempo = self.tempo_min+tempo*(self.tempo_max-self.tempo_min)/127
            else:
                tempo_increment = tempo_knob['inc_value'] * tempo_knob['ratio'] if tempo_knob['ratio'] \
                    else tempo_knob['inc_value']
                tempo = self.tempo_value + tempo_increment

            print(f"bef: {self.tempo_value}")
            if tempo > self.tempo_max:
                tempo = self.tempo_max
            elif tempo < self.tempo_min:
                tempo = self.tempo_min
        self.tempo_value = tempo
        print(f"aft: {self.tempo_value=}")
        self.tracker_ref.set_tempo_trk(round(tempo))
    # </editor-fold>

    # <editor-fold desc="Play functions">
    def set_play_func(self, instance, func_name):
        log_call()
        print('func_name:', func_name)
        # print(instance)
        if func_name not in  self.tracker_ref.note_patterns.pattern_methods_short_list:
            func_name = self.tracker_ref.note_patterns.pattern_methods_short_list[0]
        self.tracker_ref.note_patterns.set_pattern_function(func_name)
        self.tracker_ref.func_name = func_name
        self.func_init_text = func_name

    def rand_play_func(self):
        log_call()
        selected_function = random.choice(
            # list(set(self.tracker_ref.note_patterns.pattern_methods_short_list) - set([self.func_init_text]))
            list(set(self.tracker_ref.note_patterns.pattern_methods_short_list) - {self.func_init_text})
        )
        self.set_play_func(None, selected_function)


    # </editor-fold>

    # <editor-fold desc="Duration Variety">
    def set_dur_variety_f_main(self, instance, dur_variety=None, dur_variety_knob=None):
        log_call()
        print(f"{dur_variety=},{dur_variety_knob=}")
        if dur_variety is None:
            if dur_variety_knob['knob_type'] == 'abs':
                dur_variety = dur_variety_knob['value']
                dur_variety = self.dur_variety_min+dur_variety*(self.dur_variety_max-self.dur_variety_min)/127
            else:
                dur_variety_increment = dur_variety_knob['inc_value'] * dur_variety_knob['ratio'] if dur_variety_knob['ratio'] \
                    else dur_variety_knob['inc_value']
                dur_variety = self.dur_variety_value + dur_variety_increment

            print(f"bef: {self.dur_variety_value}")
            if dur_variety > self.dur_variety_max:
                dur_variety = self.dur_variety_max
            elif dur_variety < self.dur_variety_min:
                dur_variety = self.dur_variety_min
        self.dur_variety_value = dur_variety
        print(f"aft: {self.dur_variety_value=}")
        self.tracker_ref.dur_variety = dur_variety

    # </editor-fold>

    # <editor-fold desc="Quantize">
    def on_selected_quantize(self, instance, quantize):
        log_call()
        self.selected_quantize_and_state(instance, quantize)

    def on_selected_quantize_state(self, instance, quantize):
        log_call()
        self.selected_quantize_and_state(instance, quantize)

    def selected_quantize_and_state(self, instance, quantize):
        log_call()
        print(f'this is selected quantize {quantize}, {instance=}')
        print("-----------------==========-x-: ",  {x.text: x.children[0].state for x in self.root.quant_buttons})

        self.tracker_ref.quants_state = {x.text: x.children[0].state for x in self.root.quant_buttons}

    # </editor-fold>

    # <editor-fold desc="Align">
    def on_selected_align(self, instance, align):
        log_call()
        print(f'align {align}, {instance=}')
        self.tracker_ref.align_state = align
    # </editor-fold>

    # <editor-fold desc="Loop Queue">
    def inv_loopq_play_state(self):
        state = self.root.loopq.state
        to_state = 'normal' if state == 'down' else 'down'
        self.root.loopq.state = to_state

    def set_loopq_state(self, loopq_button=None):
        if not loopq_button:
            return
        state = loopq_button.get('state')
        if state:
            self.root.loopq.state = state

    def loopq_action(self, instance, state):
        self.tracker_ref.loopq = True if state == 'down' else False
    # </editor-fold>

    # <editor-fold desc="Clear Queue">
    def set_clearq_state(self, clearq_button=None):
        if not clearq_button:
            return
        self.tracker_ref.clear_queue()

    def clearq_action(self):
        log_call()
        self.tracker_ref.clear_queue()
    # </editor-fold>

    # <editor-fold desc="Notes Pair">
    def set_curr_notes_pair_lbl_text(self, value):
        self.curr_notes_pair_lbl_text = value
    # </editor-fold>

    # <editor-fold desc="Queue content">
    def set_queue_content_lbl_text(self, value):
        self.queue_content_lbl_text = value

    def set_fullq_content_lbl_text(self, value):
        self.fullq_content_lbl_text = value


    def set_check_notes_lbl_text(self, value):
        self.check_notes_lbl_text = value
    # </editor-fold>


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
        this_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(this_dir, '../config/note_patterns.json')

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
