import isobar
import json
from itertools import chain

from tracker import *
from patterns import *
from gui import *

# from keyboard import *
global IN_COLAB
IN_COLAB = 'google.colab' in sys.modules
global label_str
# global app


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import (StringProperty, ListProperty, ObjectProperty, NumericProperty)

from kivy.lang import Builder
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

# def sbtp():
#     my_tracker.beat = my_tracker.pplay


def rs():
    rand_scale()


def save_midi(on_exit=False):
    my_tracker.save_midi(on_exit=on_exit)
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


def tk_metro_on_off():
    log_call()
    app.metro_on.set((app.metro_on.get())+1%2)
    my_tracker.metro_start_stop(app.metro_on)





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


def tk_and_scale():
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


def tk_set_scale(event):
    log_call()
    scale_obj =  iso.Scale.byname(app.scale_combo.get())
    my_tracker.key = iso.Key(my_tracker.key.tonic, scale_obj)
    # my_tracker.meta_key_scale(key=app.keys_group.get(),scale=app.scale_combo.get())

def set_scale(scale_name):
    log_call()
    scale_obj =  iso.Scale.byname(scale_name)
    my_tracker.key = iso.Key(my_tracker.key.tonic, scale_obj)
    

def set_key():
    log_call()
    keys_scale_action(app.keys_group.get(), my_tracker.key.scale.name)
    # my_tracker.meta_key_scale(key=app.keys_group.get(),scale=app.scale_combo.get())
    # print(f"{app.keys_group.get()}")




def tk_set_tempo(tempo):
    log_call()
    my_tracker.set_tempo(tempo)
    my_tracker.meta_tempo(tempo=tempo)

def play_pause_tk():
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



def main():
    global my_tracker
    global keyboard
    log_call()
    # midi_out_flag = Tracker.MIDI_OUT_DEVICE
    midi_out_flag = Tracker.MIDI_OUT_MIX_FILE_DEVICE
    # midi_out_flag = Tracker.MIDI_OUT_FILE
    my_tracker = Tracker(midi_out_mode=midi_out_flag)
    # my_tracker.midi_out.program_change(program=22)


    # wrk cleanup
    # my_tracker.scale_name_action = lambda: print(None)
    # my_tracker.check_notes_action = lambda: print(None)
    # my_tracker.queue_content_action = lambda: print(None)
    # my_tracker.curr_notes_pair_action = lambda: print(None)
    # my_tracker.loop_play_queue_action = lambda: print(None)
    # my_tracker.fullq_content_action = lambda: print(None)


    # keyboard = Keyboard(lambda note: put_in_queue(note))
    # sbpq()
    # ts()  # make by  default not starting
    TrackerApp(parm_rows=7,parm_cols=3).run()
    ts()
    save_midi(on_exit=True)



class RadioButton(ToggleButtonBehavior, BoxLayout):
    text = StringProperty('')
    pass

class ScaleButton(ToggleButtonBehavior, BoxLayout):
    text = StringProperty('')
    raw_text = ListProperty('')
    pass

# class TrackerWidget(BoxLayout):
#     pass

class TrackerApp(App):

    
    # scale_init_text = StringProperty()
    scale_values = ListProperty()
    scale_set_name_txt = StringProperty()
    selected_root_note = StringProperty()
    func_init_text = StringProperty()
    func_values = ListProperty()

 
    check_notes_lbl_text = StringProperty('test1 test2')
    # check_notes_lbl_text = StringProperty()
    queue_content_lbl_text = StringProperty()
    curr_notes_pair_lbl_text = StringProperty()
    fullq_content_lbl_text = StringProperty()
    prev_key = None    

    selected_scale_button = StringProperty()
    parm_rows=NumericProperty()
    parm_cols=NumericProperty()
    prev_key = None



    # def build(self):
    #     return TrackerWidget()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_up(self, keyboard, keycode):
        self.prev_key=None
        key = keycode[1]
        print(f'{key} released')


    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        play_keys = "q2w3er5t6y7ui9o0p[=]"
        
        if keycode[1]==self.prev_key:
            return True
        print(f"{keycode[1]=} pressed")
        self.prev_key = keycode[1]
        if keycode[1] == 'z':
            self.inv_play_pause()
        elif keycode[1] == 'x':
            self.inv_metro_on_off()
        elif keycode[1] == 'b':
            self.rand_scale()
        elif keycode[1] == 'n':
            self.rand_key()
        elif keycode[1] == 'm':
            self.rand_play_funct()
        elif keycode[1] == 'escape':
            if self.root.current=='scales_option':
                self.root.current='main_screen'
                self.root.ids.scales_opt.rem_buttons()
                print('return to main screen')
            else:
                print('close application')
                self.close_application()
        elif keycode[1] in play_keys:
            put_in_queue(play_keys.index(keycode[1])+60)
            # self.note = self.play_keys.index(key.char)+60
            # self.func_on_note(self.note)
        return True

    #     if keycode[1] == self.prev_key:
    #         return True
    #     print(f"{keycode[1]=} pressed")
    #     self.prev_key = keycode[1]
    #     if keycode[1] == 'escape':
    #         if self.root.current=='scales_option':
    #             self.root.current='main_screen'
    #             self.root.ids.scales_opt.rem_buttons()
    #             print('return to main screen')
    #         else:
    #             print('close application')
    #             self.close_application()

    #     return True


    def close_application(self):
        # closing application
        App.get_running_app().stop()
        Window.close()

    def on_start(self):
       
        # self.keys_mapping_init()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, None)
        # self._keyboard = App.request_keyboard(self._keyboard_closed, self)

        
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.loop_play(instance=None, state=self.root.ids.main_scr.ids.loopq_button.state)
        my_tracker.metro_start_stop(self.root.ids.main_scr.ids.metronome.state)
        all_scales = sorted([scale.name for scale in iso.Scale.all()])
        # self.scale_init_text = my_tracker.key.scale.name
        self.selected_scale_button  = my_tracker.key.scale.name
        self.scale_values = all_scales
        self.func_values = my_tracker.note_patterns.pattern_methods_short_list
        self.func_init_text = my_tracker.note_patterns.pattern_methods_short_list[0]

        my_tracker.scale_name_action = lambda: self.set_scale_set_name_txt('set:' + my_tracker.key.scale.name)
        my_tracker.check_notes_action = lambda: self.set_check_notes_lbl_text(str(my_tracker.check_notes))
 
        my_tracker.queue_content_action = lambda: self.set_queue_content_lbl_text('queue: '+str(my_tracker.get_queue_content()))
        my_tracker.curr_notes_pair_action = lambda: self.set_curr_notes_pair_lbl_text('from to: '+str(my_tracker.notes_pair))
        my_tracker.fullq_content_action = lambda: self.set_fullq_content_lbl_text('full queue: '+str(my_tracker.get_queue_content_full()))

    def inv_play_pause(self):
        state=self.root.ids.main_scr.ids.start_stop_button.state
        to_state = 'normal' if state == 'down' else 'down'
        self.root.ids.main_scr.ids.start_stop_button.state=to_state
        # self.play_pause(None, to_state)
        
    def inv_metro_on_off(self):
        state=self.root.ids.main_scr.ids.metronome.state
        to_state = 'normal' if state == 'down' else 'down'
        self.root.ids.main_scr.ids.metronome.state=to_state
        # self.metro_on_off(None, to_state)

    def play_pause(self, instance, state):
        log_call()
        print(f"{instance=}, {state=}")
        tstart() if state=='down' else tstop()


    def metro_on_off(self, instance, state):
        log_call()
        my_tracker.metro_start_stop(state)


    def loop_play(self, instance, state):
        my_tracker.loopq = True if state == 'down' else False

    def save(self):
        my_tracker.save_midi()
        
    def set_scale(self, instance, scale_name):
        log_call()
        # print(instance)
        set_scale(scale_name) #TODO review this


    
    def set_scale_set_name_txt(self, value):
        self.scale_set_name_txt=value

        
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
        all_scales=[scale.name for scale in iso.Scale.all()]
        random_scale = random.choice(list(set(all_scales)-set([my_tracker.key.scale.name])))
        # my_tracker.key = iso.Key(my_tracker.key.tonic, iso.Scale.random())
        my_tracker.key = iso.Key(my_tracker.key.tonic, random_scale)
        # self.scale_init_text=my_tracker.key.scale.name
        self.selected_scale_button =my_tracker.key.scale.name

    def on_selected_root_note(self, instance, root_note):
        print(f'this is selected root note {root_note}')
        keys_scale_action(root_note, my_tracker.key.scale.name)

    def rand_key(self):
        keys = list({key.text for key in self.root.ids.main_scr.ids.scales_group.children}\
            -{ self.selected_root_note })
        randomized_key = random.choice(keys)
        print(f'this is {randomized_key=}')
        print(my_tracker.key)
        keys_scale_action(randomized_key, my_tracker.key.scale.name)
        for key in self.root.ids.main_scr.ids.scales_group.children:
            print(f"{key.text=} != {randomized_key}")
            if key.text != randomized_key:
                key.state = 'normal'
                continue
            key.state = 'down'
            print(my_tracker.key)
            # key.selected = True
            
        # self.names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    def set_play_func(self, instance, func_name):
        log_call()
        # print(instance)
        my_tracker.note_patterns.set_pattern_function(func_name)

    def rand_play_funct(self):
        log_call()
        selected_function=random.choice(
            list(set(my_tracker.note_patterns.pattern_methods_short_list) - set([self.func_init_text]))
        )
        self.func_init_text = selected_function
        my_tracker.note_patterns.set_pattern_function(selected_function)

    def set_tempo(self, instance, tempo):
        log_call()
        my_tracker.set_tempo(tempo)
        my_tracker.meta_tempo(tempo=tempo) 


# def set_play_func(event):
#     log_call()
#     my_tracker.note_patterns.set_pattern_function(app.play_func_combo.get())
    
    
    def test1(self, instance, state):
        print(f"test1: {instance=}, {state=}")

    def test2(self, instance, state):
        print(f"test2: {instance=}, {state=}")
        # app.loop_queue_chk_cmd_ext = lambda: my_tracker.loop_play_queue_action(app.loop_queue_on.get())
        # my_tracker.loopq = app.loop_queue_on.get()


    def on_selected_scale_button(self, instance, value):
        print(instance, value)
        print(self.selected_scale_button)
        self.set_scale(instance, value)

    # def _keyboard_closed(self):
    #     self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    #     self._keyboard.unbind(on_key_up=self._on_keyboard_up)
    #     self._keyboard = None

    # def _on_keyboard_up(self, keyboard, keycode):
    #     self.prev_key = None
    #     key = keycode[1]
    #     print(f'{key} released')

    # def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #     play_keys = "q2w3er5t6y7ui9o0p[=]"

    #     if keycode[1] == self.prev_key:
    #         return True
    #     print(f"{keycode[1]=} pressed")
    #     self.prev_key = keycode[1]
    #     if keycode[1] == 'escape':
    #         if self.root.current=='scales_option':
    #             self.root.current='main_screen'
    #             self.root.ids.scales_opt.rem_buttons()
    #             print('return to main screen')
    #         else:
    #             print('close application')
    #             self.close_application()

    #     return True



    # def on_start(self):

        # # self.keys_mapping_init()
        # self._keyboard = Window.request_keyboard(self._keyboard_closed, None)
        # # self._keyboard = App.request_keyboard(self._keyboard_closed, self)

        # self._keyboard.bind(on_key_down=self._on_keyboard_down)
        # self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def close_application(self):
        # closing application
        App.get_running_app().stop()
        Window.close()


class MainScreen(Screen):

    pass



class ScalesSelectScreen(Screen):


    # self.grid_rows=rows
    # self.grid_cols=cols
    # self.grid_len=rows*cols

    btn = ObjectProperty()
    button_matrix = ListProperty()
    # grid_rows=NumericProperty(13)
    # grid_cols=NumericProperty(4)
    # grid_len=NumericProperty(13*4)
    
    grid_rows=NumericProperty()
    grid_cols=NumericProperty()
    grid_len=NumericProperty()

    # pos_x = NumericProperty()
    grid_pos = ListProperty()
    last_grid_up_down = StringProperty()
    

    but_id_offset = 0
    # button_names = [ 'button_'+ str(i+1).rjust(3,'0')[-3:] for i in range(500)]
    # nbr_of_scales = len(button_names)   


    def __init__(self, **kwargs):
        super(ScalesSelectScreen, self).__init__(**kwargs)   
        print(f"{self.grid_cols=}, {self.grid_rows=},{self.grid_cols=}")

        self.__read_config_file__()
        # self.button_names = [button_id['name'][0] for button_id in self.patterns_config['scales'] if button_id['name'] ]
        self.button_names = [button_id['name'] for button_id in self.patterns_config['scales'] if button_id['name'] ]
        self.nbr_of_scales = len(self.button_names)

        
    def __read_config_file__(self):
        # print('reading config')
        config_file = 'reviewed_pattern_cfg.json'
        # config_file = '/workspaces/soundDesign/tracker/reviewed_pattern_cfg.json'


        with open(config_file, 'r') as file:
            # with open('reviewed_pattern_cfg.yaml', 'r') as file:
            # self.patterns_config = yaml.safe_load(file)
            self.patterns_config = json.load(file)


    def populate_button(self):
        
        # button_matix_len=self.grid_cols*self.grid_rows
        # self.root.ids.scales_opt.ids.button_grid.add_widget(RadioButton(text='World 2'))
        # self.button_matrix=[]
        # for button_id in range(self.but_id_offset,self.but_id_offset+10):
        # for button_id in self.button_names:

        for button_id in self.button_names[self.but_id_offset:self.but_id_offset+self.grid_len]:
        # for button_id in self.patterns_config['scales'][self.but_id_offset:self.but_id_offset+self.grid_len if button_id['name']!=[]]:
        #     button_text=f"{button_id}"
        #     button_text='\n'.join(button_id)
            button_text = button_id
            # btn = ScaleButton(text=button_text)
            btn = ScaleButton(raw_text=button_text)
            # if button_text == self.selected_scale:
            if self.selected_scale in button_text:
                btn.state='down'
                
            self.button_matrix.append(btn)
            # self.root.ids.scales_opt.ids.button_grid.add_widget(RadioButton(text=f'auto_{button_id}'))
            # self.root.ids.scales_opt.ids.button_grid.add_widget(btn)
            self.ids.button_grid.add_widget(btn)
            
        print('----------------')
    pass


    def rem_buttons(self):
        for button in self.button_matrix:
            # self.root.ids.scales_opt.remove_widget(button) 
            # self.root.ids.scales_opt.ids.button_grid.remove_widget(button)
            self.ids.button_grid.remove_widget(button)
        # self.but_id_offset+=self.grid_len
    


    def scale_page(self, direction=None, scale='major'):
        if direction in ('RL','prev'):
            self.rem_buttons()
            self.but_id_offset-=self.grid_len    
            if self.but_id_offset<0:
                self.but_id_offset=0
        elif direction in ('LR', 'next'):
            self.rem_buttons()
            if self.but_id_offset+self.grid_len<self.nbr_of_scales:
                self.but_id_offset+=self.grid_len
            
        else:
            for x in range(0,len(self.button_names),self.grid_len):
                # if scale  in self.button_names[x:x+self.grid_len]:
                if scale  in list(chain(*self.button_names[x:x+self.grid_len])):
                    self.but_id_offset=x
                    break
                    # return
            
# for button_id in self.button_names[self.but_id_offset:self.but_id_offset+self.grid_len]:            
            # return    
        self.populate_button()
        

     
    def on_touch_down(self,touch):
        self.last_grid_up_down='down'
        # print(f"down , {touch.__dict__=}, {touch.px=}, {touch.py=}, {touch.pos=}")
        print(f"down , {touch.px=}, {touch.py=}, {touch.pos=}")
        # self.pos_x=touch.px
        self.grid_pos = touch.pos
        # return super(ScalesSelectScreen, self).on_touch_down(touch)
        # touch.grab(self)
        
    def on_touch_up(self,touch):
        prev_last_grid_up_down=self.last_grid_up_down
        self.last_grid_up_down='up'

        if not self.grid_pos  or self.grid_pos == []:
            self.grid_pos = touch.pos
            return True
        # print(f"up, {touch.__dict__=}, {touch.px=}, {touch.py=}, {touch.pos=}")
        print(f"up,  {touch.px=}, {touch.py=}, {touch.pos=}")
        
        # if self.grid_pos[0]-touch.px > 50:
        print(f"{self.grid_pos[0]=},{touch.x=}, {self.grid_pos[0]-touch.x=}")
        if prev_last_grid_up_down=='down': # to filter out accidental up-up
            if self.grid_pos[0]-touch.x > 50:
                print('>>>>>>>next')
                self.scale_page(direction='next')
            # elif self.pos_x-touch.px <-50:
            if self.grid_pos[0]-touch.x <-50:
                print('prev<<<<<<<')
                self.scale_page(direction='prev')
                # return super(ScalesSelectScreen, self).on_touch_down(touch)
            # if self.pos == touch.pos:
            if pow(self.grid_pos[0]-touch.x,2)+pow(self.grid_pos[1]-touch.y,2) <=100:
                print('>>>>>>>equal<<<<<<<')
                self.grid_pos = touch.pos
                return super(ScalesSelectScreen, self).on_touch_down(touch)
            # touch.grab(self)
            self.grid_pos = touch.pos


if __name__ == '__main__':
    # print('Do we start?')
    # main_tk()
    main()
    print('Processing Done.')
