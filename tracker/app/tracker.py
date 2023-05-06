# import os
from queue import Queue
import shutil
from datetime import datetime
from itertools import accumulate
# import mido

from .isobar_fixes import *
from .patterns import *
from .log_call import *
from .midi_dev import *

NO_MIDI_OUT = mido.get_output_names() == []
ACCENT_BIG_FACTOR = 1.5
ACCENT_MED_FACTOR = 1.25
ACCENT_DEFAULT = 45
ACCENT_BIG = int(ACCENT_DEFAULT * ACCENT_BIG_FACTOR)
ACCENT_MED = int(ACCENT_DEFAULT * ACCENT_MED_FACTOR)


class Tracker:
    # <editor-fold desc="Class init functions">
    MIDI_OUT_DUMMY = 0
    MIDI_OUT_FILE = 1
    MIDI_OUT_DEVICE = 2
    MIDI_OUT_MIX_FILE_DEVICE = 3

    def __init__(self, tracker_config=None,
                 midi_out_mode='dummy',
                 midi_mapping={},
                 filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "saved_midi_files",
                                       "xoutput.mid")):
        log_call()

        read_config_file_scales()
        self.midi_in = None
        self.key = iso.Key("C", "major")
        self.prev_key = None
        self.loopq = False
        self.midi_out = None
        self.track = None
        self.filename = filename

        # self.beat_count = -1 % 4
        self.diff_time = 0
        self.prev_time = 0
        self.timeline = None
        self.note_patterns = NotePatterns()
        self.prev_get_pattern_name = None
        self.root_note = 0
        self.last_note = None
        self.last_from_note = None
        self.notes_pair = [None, None]
        self.queue_content_wrk = None
        self.note_queue = Queue(maxsize=16)
        # self.amp_for_beat_factor = dict(zip([0, 2], [1.5, 1.25]))

        self.midi_mapping = midi_mapping

        self.pattern_idx = 0
        self.default_tracker_config = \
            {
                "midi_in_name": ["blah_blah_0", "sdfdsf123"],
                "midi_out_name": ["in_blah_blah_0", "ppp_sdfdsf123"],
                "default_channel": 1,
                "legato": 1.0,
                "program_change": 0,
                "time_signature": {"numerator": 4, "denominator": 4},
                "dummy_hardcoded_config": "asdfsdf"
            }
        if tracker_config:
            self.default_tracker_config.update(tracker_config)

        self.midi_in_name = self.default_tracker_config.get("midi_in_name")
        self.midi_out_name = self.default_tracker_config.get("midi_out_name")
        self.legato = self.default_tracker_config.get("legato")
        self.program_change = self.default_tracker_config.get("program_change")
        self.time_signature = self.default_tracker_config.get("time_signature")
        # self.beat_count = -1 % self.time_signature['numerator']
        # self.beat_count = -0 % self.time_signature['numerator']
        self.beat_count = -1%4
        # self.numerator_count = -1 % self.time_signature['numerator']

        self.amp_for_beat_factor = {
            1: dict(zip([0, 2], [1.5, 1.25])),
            2: dict(zip([0, 1], [1.5, 1.25])),
            3: dict(zip([0, 2], [1.5, 1.25])),
            4: dict(zip([0, 2], [1.5, 1.25])),
            5: dict(zip([0, 3], [1.5, 1.25])),
            6: dict(zip([0, 3], [1.5, 1.25])),
            7: dict(zip([0, 3, 5], [1.5, 1.25, 1.25])),
            8: dict(zip([0, 4], [1.5, 1.25])),
            9: dict(zip([0, 3, 6], [1.5, 1.25, 1.25])),
            10: dict(zip([0, 5], [1.5, 1.25])),
            11: dict(zip([0, 6], [1.5, 1.25])),
            12: dict(zip([0, 3, 6, 9], [1.5, 1.25, 1.25, 1.25]))
        }

        self.factors = {5: 1, 7: 1, 10: 2, 11: 3}
        self.amp_factors = {
            1: {0: ACCENT_BIG_FACTOR},
            2: {0: ACCENT_BIG_FACTOR, 1: ACCENT_MED_FACTOR},
            3: {0: ACCENT_BIG_FACTOR, 2: ACCENT_MED_FACTOR},
            4: {0: ACCENT_BIG_FACTOR, 2: ACCENT_MED_FACTOR},
            5: {0: ACCENT_BIG_FACTOR, 2: ACCENT_MED_FACTOR},
            6: {0: ACCENT_BIG_FACTOR, 3: ACCENT_MED_FACTOR},
            7: {0: ACCENT_BIG_FACTOR, 4: ACCENT_MED_FACTOR},
            8: {0: ACCENT_BIG_FACTOR, 4: ACCENT_MED_FACTOR},
            9: {0: ACCENT_BIG_FACTOR, 3: ACCENT_MED_FACTOR, 6: ACCENT_MED_FACTOR},
            10: {0: ACCENT_BIG_FACTOR, 4: ACCENT_MED_FACTOR},
            11: {0: ACCENT_BIG_FACTOR, 4: ACCENT_MED_FACTOR},
            12: {0: ACCENT_BIG_FACTOR, 3: ACCENT_MED_FACTOR, 6: ACCENT_MED_FACTOR, 9: ACCENT_MED_FACTOR},
        }
        self.factor = 0
        self.default_duration = None
        self.metro_seq = None
        self.metro_amp = None
        self.accents_dict = {}
        self.set_default_duration()
        self.set_metro_seq()

        self.current_program = None
        self.midi_out_mode = midi_out_mode
        self.init_timeline(midi_in_name=self.midi_in_name, midi_out_name=self.midi_out_name,
                           midi_out_mode=midi_out_mode)
        self.beat = lambda: self.play_from_to(None, None, in_pattern=True)
        self.metro_beat = lambda: print('metro_beat init')
        self.current_tempo = 0
        self.current_dur_variety = 0
        self.current_func = None
        self.quants_state = {}
        self.current_quants_state = {}
        self.align_state = 0
        self.current_align_state = 0
        self.dur_variety = 0
        self.func_name = None
        self.tmln = self.tracker_timeline()
        self.metro = self.metro_timeline()
        self.set_program_change_trk(program=self.program_change)

    def set_default_duration(self):
        self.factor = self.factors.get(self.time_signature['numerator'], 0)
        self.default_duration = [6 / self.time_signature['denominator']] * (2 * self.factor) + [
            4 / self.time_signature['denominator']] \
                                * (self.time_signature['numerator'] - 3 * self.factor)

        self.metro_amp = [ACCENT_DEFAULT] * (self.time_signature['numerator'] - self.factor)
        self.accents_dict = self.amp_factors.get(self.time_signature['numerator'], [ACCENT_DEFAULT])
        for a in self.accents_dict.keys():
            self.metro_amp[a] = int(self.accents_dict[a] * self.metro_amp[a])
        agg_duration = 0

    def set_metro_seq(self):
        self.metro_seq = [32] + [37] * (self.time_signature['numerator'] - 1 - self.factor)

    def save_midi(self, on_exit=False):
        date = datetime.now().strftime('%Y%m%d%H%M%S')
        if self.midi_out_mode == self.MIDI_OUT_DEVICE:
            return None
        if on_exit:
            self.mid_meta_message('end_of_track', time=0)

        self.midi_out.write()
        target_dir = os.path.dirname(self.filename)
        target_filename = os.path.splitext(os.path.basename(self.filename))
        target_path_file = os.path.join(target_dir, target_filename[0] + '_' + date + target_filename[1])
        shutil.copy(self.filename, target_path_file)

    def setup_midi_in(self, midi_in_name):

        def midi_in_callback(message):
            def get_knob_val(val, base):
                val -= base
                if val > 63:
                    val -= 128
                return val

            def get_button(mess=None):
                log_call()
                if not mess:
                    print("no message")

                    return None
                print(type(mess), mess.__dict__)
                btn = [(mid_k, self.midi_mapping[mid_k]) for mid_k in self.midi_mapping
                       if self.midi_mapping[mid_k].get("channel") == mess.channel
                       and self.midi_mapping[mid_k].get("note") == mess.note
                       ]
                if not btn:
                    return None
                btn = btn[0]
                button_name = btn[0]  # this is different knob[0] than above line

                print(f"{btn=},{btn[0]=},{btn[1]=}")
                if btn[1].get('gate'):
                    if mess.type == 'note_on':
                        return {'name': button_name,
                                'gate': True,
                                'state': 'down'
                                }
                    else:
                        return None
                if not btn[1].get("toggle"):
                    btn[1]['toggle'] = False
                if not btn[1].get("state"):
                    btn[1]['state'] = 'normal'
                print(f"{btn[1]['toggle']}")
                if btn[1]['toggle']:
                    print("x1")
                    if mess.type == 'note_on':
                        print("x2")
                        btn[1]['state'] = 'down'
                    else:
                        btn[1]['state'] = 'normal'
                        print("x3")
                else:
                    print("x4")
                    if mess.type == 'note_on':
                        print("x5")
                        if btn[1]['state'] == 'down':
                            print("x6")
                            btn[1]['state'] = 'normal'
                        else:
                            print("x7")
                            btn[1]['state'] = 'down'

                print(f"{btn[1]['state']=}")

                return {'name': button_name,
                        'toggle': btn[1]['toggle'],
                        'state': btn[1]['state']
                        }

            def get_knob(mess=None):
                if not mess:
                    return None
                type_base_conv = {"rel#1": 64, "rel#2": 0, "rel#3": 16}
                print(type(mess), mess.__dict__)

                knb = [(mid_k, self.midi_mapping[mid_k]) for mid_k in self.midi_mapping
                       if self.midi_mapping[mid_k].get("cc") == mess.control]

                if not knb:
                    return None

                knb = knb[0]
                knob_name = knb[0]  # this is different knob[0] than above line
                print(f"{knb=},{knb[0]=},{knb[1]=}")
                if not knb[1].get("value"):
                    knb[1]['value'] = 0.0
                if not knb[1].get("inc_value"):
                    knb[1]['inc_value'] = 0.0
                if not knb[1].get("ratio"):
                    knb[1]['ratio'] = 1.0

                knob_type = knb[1]['knob_type']
                if knob_type == 'abs':
                    knb[1]['value'] = mess.value
                else:
                    knob_base = type_base_conv.get(knob_type)
                    if knob_base is None:
                        return None
                    if mess.value != knob_base:
                        knb[1]['inc_value'] = get_knob_val(mess.value, knob_base)
                        knb[1]['value'] += knb[1]['inc_value'] * knb[1]['ratio']

                        print(f"{knb[1]['value']},{knb[1]['inc_value']}")
                return {'name': knob_name,
                        'type': knob_type,
                        'value': knb[1]['value'],
                        'inc_value': knb[1]['inc_value']
                        }

            print(" - Received MIDI: %s" % message)
            print(message.__dict__)
            # self.default_tracker_config['default_channel']
            print(f"{message=}")
            if message.type == 'note_on' or message.type == 'note_off':
                if message.channel == self.default_tracker_config['default_channel']:
                    if message.type == 'note_on':
                        self.put_to_queue(message.note)
                else:
                    button = get_button(mess=message)
                    print(f"{button=}")
                    oper_to_func = {
                        'play': self.set_play_action,
                        'metronome': self.set_metronome_action,
                        'loop': self.set_loop_action,
                        'clearq': self.set_clearq_action,
                        'rnd_scale': self.set_rnd_scale_action,
                        'rnd_key': self.set_rnd_key_action,
                        'rnd_func': self.set_rnd_func_action
                    }
                    # print(f"xxx:{button['name']}, {oper_to_func.get(button['name'])}")
                    if button:
                        func = oper_to_func.get(button.get('name'))
                        print(f"xxx:{func=}")
                        if func:
                            func()

            elif message.type == 'control_change':
                print(f"{message.control=}")
                knob = get_knob(mess=message)
                oper_to_func = {
                    'set_tempo_knob': self.set_tempo_action,
                    'set_dur_variety_knob': self.set_dur_variety_action
                }
                print(f"{knob=}")
                # if knob:
                #     if knob['name']=='set_tempo_knob':
                #         self.set_tempo_action()
                if knob:
                    func = oper_to_func.get(knob.get('name'))
                    print(f"xxx:{func=}")
                    if func:
                        func()
            elif message.type == 'program_change':
                # print(f"{message.__dict__=}")
                self.program_change = message.program
                # self.set_program_change(program=message.program)

        midi_in_name = [mids[0] for mids in itertools.product(mido.get_input_names(), midi_in_name) if
                        mids[1] in mids[0]]

        if midi_in_name:
            try:
                self.midi_in = ExtendedMidiInputDevice(midi_in_name[0])
            except iso.DeviceNotFoundException:
                print(f"Can't open midi in named'{midi_in_name[0]}. Possibly locked by other application'")
                return
            self.midi_in.callback = midi_in_callback
        else:
            print(f"No midi in with {midi_in_name}")

    def init_timeline(self, midi_in_name, midi_out_name, midi_out_mode='dummy', ):
        log_call()
        print(f" Device:{midi_out_mode}")
        print(f"{NO_MIDI_OUT=}")
        filename = self.filename
        midi_out_name = [mids[0] for mids in itertools.product(mido.get_output_names(), midi_out_name) if
                         mids[1] in mids[0]]

        if midi_out_name:
            self.midi_out_name = midi_out_name[0]
        else:
            self.midi_out_name = self.midi_out_name[0]

        if midi_out_mode == self.MIDI_OUT_FILE:
            self.midi_out = iso.MidiFileOutputDevice(filename)
            print("file mode")
        elif midi_out_mode == self.MIDI_OUT_DEVICE and not NO_MIDI_OUT:
            self.midi_out = iso.MidiOutputDevice(device_name=self.midi_out_name, send_clock=True)
            print("device mode")
        elif midi_out_mode == self.MIDI_OUT_MIX_FILE_DEVICE:
            self.midi_out = FileOut(filename=filename, device_name=self.midi_out_name, send_clock=True,
                                    virtual=NO_MIDI_OUT)
            # self.midi_out = FileOut(filename=filename, device_name=self.name, send_clock=True, virtual=True)
            print("device mode")
        else:
            # self.MIDI_OUT_DUMMY
            self.midi_out = iso.DummyOutputDevice()
            print("dummy mode")
        self.setup_midi_in(midi_in_name)
        # self.mid_meta_message('time_signature', numerator=3, denominator=4, time=0)
        self.mid_meta_message('time_signature', numerator=self.time_signature['numerator'],
                              denominator=self.time_signature['denominator'], time=0)
        print(f"----------- {MULTI_TRACK=}")
        self.timeline = iso.Timeline(120, output_device=self.midi_out)

    # </editor-fold>

    def get_amp_factor(self):
        xxx = self.amp_for_beat_factor.get(self.time_signature['numerator'])
        print(f"{xxx=},{self.time_signature['numerator']=}")
        accent = self.amp_for_beat_factor.get(self.time_signature['numerator'], {}).get(self.beat_count)
        # accent = self.amp_for_beat_factor.get(self.beat_count)
        return accent if accent else 1

    def log_and_schedule(func):
        def inner(self, *args, **kwargs):
            log_call()
            print(func.__name__)

            self.beat_count += 1
            # self.time_sig_beat_val=self.beat_count

            self.diff_time = self.timeline.current_time - self.prev_time
            self.prev_time = self.timeline.current_time
            print(f"{func.__name__} diff:{self.diff_time}, timeXX: {self.timeline.current_time},"
                  f" {round(self.timeline.current_time)} beat: {self.beat_count}\n")
            self.beat_count %= 4
            # self.beat_count %= self.time_signature['numerator']
            notes = func(self, *args, **kwargs)

            # xxx = notes[iso.EVENT_NOTE]
            notes[iso.EVENT_NOTE] = iso.PMap(notes[iso.EVENT_NOTE], lambda midi_note:
            (None if not midi_note else None if midi_note < 0 else None if midi_note > 127 else midi_note)
            if not midi_note or isinstance(midi_note, int)
            else tuple(map(lambda u: None if not u else None if u < 0 else None if u > 127 else u, midi_note)))

            # create accent depending on beat
            print("bbbb1: ", list(map(type, notes[iso.EVENT_AMPLITUDE].copy())))
            if notes[iso.EVENT_AMPLITUDE]:
                print(f"{list(map(type,notes[iso.EVENT_AMPLITUDE].copy()))=}")
                amplitudes = list(notes[iso.EVENT_AMPLITUDE].copy())
                durations = [0] + list(notes[iso.EVENT_DURATION].copy())
                acc_durations = list(accumulate(durations[:-1]))
                for key in self.accents_dict.keys():
                    try:
                        idx = acc_durations.index(key)
                        amplitudes[idx] = int(self.accents_dict[key]*amplitudes[idx])
                    except ValueError:
                        print("key not found")
                amplitudes = list(map(lambda midi_amp: 0 if not midi_amp else 0 if midi_amp < 0 else 127 if midi_amp > 127 else midi_amp ,amplitudes))
                notes[iso.EVENT_AMPLITUDE] = iso.PSequence(amplitudes, repeats=1)

                # Extra fix put just as sanity mod, right before trigerring play. Might be removed if well tested when without
                notes[iso.EVENT_DURATION] = iso.PSequence(list(map(lambda x: x - 0.000000000000002, notes[iso.EVENT_DURATION])), repeats=1)


            self.check_notes = list(notes[iso.EVENT_NOTE].copy())

            print('check notes: ', self.check_notes)
            self.check_notes_action()
            print(list(notes[iso.EVENT_AMPLITUDE].copy()))
            print("bbbb: ", list(map(type, notes[iso.EVENT_AMPLITUDE].copy())))

            _ = self.timeline.schedule(
                notes
            )

            print('post sched')

        return inner

    # <editor-fold desc="Base beat functions">
    @log_and_schedule
    def beat_none(self):
        return iso.PDict({
            # iso.EVENT_NOTE: iso.PSequence([None], repeats=4)})  # TODO check beat none for custom time sig
            iso.EVENT_NOTE: iso.PSequence([None], repeats=self.time_signature['numerator'])})

    # </editor-fold>

    # <editor-fold desc="Metro functions">

    def metro_timeline(self):
        log_call()
        print(f"{time.time()=}")
        print(f"{4*self.time_signature['numerator']/self.time_signature['denominator']=},{self.metro_beat=}")
        if MULTI_TRACK:
            self.midi_out.extra_track(9)  # for percussion channel 10 (or 9 when counting from 0).
        return self.timeline.schedule({
            "action": lambda: self.metro_beat(),
            # "duration": 3/2
            # "duration": 4
            "duration": 4 * (self.time_signature['numerator'] / self.time_signature['denominator'])
            # "duration": 5

        },
            remove_when_done=False
        )

    def metro_none(self):
        log_call()
        print(f"{time.time()=},{self.metro_beat=}")
        _ = self.timeline.schedule({
            iso.EVENT_NOTE: iso.PSequence([None], repeats=1),
            "duration": 1,
            "channel": 9,
        },
            remove_when_done=True)

        # @log_and_schedule

    def metro_play(self):
        log_call()
        print(f"{time.time()=},{self.metro_beat=}")
        metro_dur = self.default_duration
        metro_seq = self.metro_seq
        metro_amp = self.metro_amp

        print(f"{metro_dur=}")

        print(f"{self.time_signature['numerator']/self.time_signature['denominator']=}")
        print(f"{metro_seq=}, {metro_amp=}, {metro_dur=}")
        self.metro_play_patterns = {
            "note": iso.PSequence(metro_seq, repeats=1),
            "duration": iso.PSequence(metro_dur, repeats=1),
            "channel": 9,
            "amplitude": iso.PSequence(metro_amp, repeats=1)}

        _ = self.timeline.schedule(self.metro_play_patterns, remove_when_done=True)

    def metro_start_stop(self, state):
        if state == 'down':
            print('-----------metro on-----------------')
            self.metro_beat = self.metro_play
        else:
            print('-----------metro off-----------------')
            self.metro_beat = self.metro_none
        pass

    # </editor-fold>

    # <editor-fold desc="Gui actions">


    def check_notes_action(self):
        log_call()

    def scale_name_action(self):
        log_call()

    def queue_content_action(self):
        log_call()

    def curr_notes_pair_action(self):
        log_call()

    def fullq_content_action(self):
        log_call()

    def time_sig_beat_val_action(self):
        log_call()
    def set_tempo_action(self):
        log_call()

    def set_dur_variety_action(self):
        log_call()

    def set_play_action(self):
        log_call()

    def set_metronome_action(self):
        log_call()

    def set_loop_action(self):
        log_call()

    def set_clearq_action(self):
        log_call()

    def set_rnd_scale_action(self):
        log_call()

    def set_rnd_key_action(self):
        log_call()

    def set_rnd_func_action(self):
        log_call()

    # </editor-fold>

    # <editor-fold desc="Queue functions">
    def get_queue_content(self):
        return 'empty' if self.note_queue.empty() else list(self.note_queue.queue)

    def get_queue_content_full(self):
        queue_v = []

        print(f"{self.notes_pair[0]=} {queue_v}")
        if self.notes_pair[0]:
            queue_v += list([self.notes_pair[0]])
        if not self.note_queue.empty():
            queue_v += list(self.note_queue.queue)
        return 'Empty' if not queue_v else queue_v

    def get_queue_pair(self):
        v_queue = list(self.note_queue.queue)
        if len(v_queue) >= 2:
            return v_queue[0], v_queue[1]
        elif len(v_queue) == 1:
            return v_queue[0], None
        else:
            return None, None

    def put_to_queue(self, note, q_action=True):

        if not self.note_queue.full():
            self.note_queue.put(note)
            if q_action:
                self.queue_content_action()
                self.fullq_content_action()

    def clear_queue(self):
        self.last_from_note = None
        self.note_queue.queue.clear()
        pass

    def get_from_queue(self):

        note = None if self.note_queue.empty() else self.note_queue.get_nowait()
        print(f"{self.loopq=}")
        self.queue_content_action()
        self.fullq_content_action()
        return note

    # </editor-fold>

    # <editor-fold desc="play functions">

    # <editor-fold desc="play definitions">

    def tracker_timeline(self):
        log_call()
        print(f"{self.beat}")
        return self.timeline.schedule({
            "action": lambda: self.beat(),
            # "duration": 4
            "duration": 4 * self.time_signature['numerator'] / self.time_signature['denominator']
            # "quantize": 1
        },
            remove_when_done=False)

    def mid_meta_message(self, *args, **kwargs):
        # return None
        if self.midi_out_mode == self.MIDI_OUT_DEVICE:
            return None
        if MULTI_TRACK:
            self.midi_out.miditrack[0].append(mido.MetaMessage(*args, **kwargs))
        else:
            self.midi_out.miditrack.append(mido.MetaMessage(*args, **kwargs))

    def set_tempo_trk(self, new_tempo):
        log_call()
        print(f"{self.current_tempo=} == {new_tempo=}")
        if int(self.current_tempo) == int(new_tempo):
            print(f"tempo not changed {self.current_tempo=}")
            return
        self.current_tempo = int(new_tempo)
        print(f"b_read tempo: {self.timeline.get_tempo()=}, {new_tempo=}")
        # self.timeline.set_tempo(int(new_tempo))
        self.timeline.set_tempo(int(new_tempo))
        # print(f"{self.timeline.current_time=}")
        self.mid_meta_message('set_tempo', tempo=mido.bpm2tempo(int(new_tempo)), time=0)
        print(f"a_read tempo: {self.timeline.get_tempo()=}, {new_tempo=}")
        self.meta_tempo(tempo=round(new_tempo))

    def set_dur_variety_trk(self, new_dur_variety):
        log_call()
        print(f"{self.current_dur_variety=} == {new_dur_variety=}")
        if self.current_dur_variety == new_dur_variety:
            print(f"dur_variety not changed {self.current_dur_variety=}")
            return
        self.current_dur_variety = new_dur_variety
        self.meta_dur_variety(dur_variety=new_dur_variety)

    def set_func_trk(self, new_func):
        log_call()
        print(f"{self.current_func=} == {new_func=}")
        if self.current_func == new_func:
            print(f"func not changed {self.current_func=}")
            return
        self.current_func = new_func
        self.meta_func(func=new_func)

    def set_align_trk(self, new_align):
        log_call()
        print(f"{self.current_align_state=} == {new_align=}")
        if self.current_align_state == new_align:
            print(f"align not changed {self.current_func=}")
            return
        self.current_align_state = new_align
        self.meta_align(align=new_align)

    def set_quantize_trk(self, new_quants):
        log_call()
        print(f"{self.current_quants_state=} == {new_quants=}")
        if self.current_quants_state == new_quants:
            print(f"quants not changed {self.current_quants_state=}")
            return
        self.current_quants_state = new_quants
        self.meta_quants(quants=new_quants)

    def set_program_change_trk(self, program=0, channel=0):
        log_call()
        if self.current_program == program:
            print(f"program was not changed {self.current_program=}")
            return
        self.midi_out.program_change(program=int(program), channel=int(channel))
        print("blahblah")
        if MULTI_TRACK:
            self.midi_out.miditrack[0].append(
                mido.Message('program_change', program=int(program), channel=int(channel)))
        else:
            self.midi_out.miditrack.append(mido.Message('program_change', program=int(program), channel=int(channel)))
        self.current_program = program

    def write_mid_text_meta(self, message):
        self.mid_meta_message('text', text=message, time=0)

    def meta_key_scale(self, key, scale):
        log_call()
        key = iso.Note.names[key.tonic % 12]
        self.write_mid_text_meta(f"scale:{key}-{scale}")

        self.mid_meta_message('key_signature', key=key + 'm', time=0)

    def meta_func(self, func):
        log_call()
        self.write_mid_text_meta(f"func:{func}")

    def meta_align(self, align):
        log_call()
        self.write_mid_text_meta(f"align:{align}")

    def meta_quants(self, quants):
        log_call()
        q2 = quants.get('2') == 'down'
        q3 = quants.get('3') == 'down'
        q5 = quants.get('5') == 'down'
        quant_flag = 'x'
        if not (q2 or q3 or q5):
            quant_flag += '2/3/5/'
        else:
            if q2:
                quant_flag += '2/'
            if q3:
                quant_flag += '3/'
            if q5:
                quant_flag += '5/'

        quant_flag = quant_flag[1:-1]
        self.write_mid_text_meta(f"quantize:{quant_flag}")

    def meta_tempo(self, tempo):
        log_call()
        self.write_mid_text_meta(f"tempo:{tempo}")

    def meta_dur_variety(self, dur_variety):
        log_call()
        self.write_mid_text_meta(f"dur_variety:{dur_variety}")

    def tstop(self):
        log_call()
        self.timeline.stop()

    def ts(self):
        log_call()
        self.timeline.stop()

    def tstart(self):
        log_call()
        self.timeline.background()

        # @log_and_schedule

    # </editor-fold>

    @log_and_schedule
    def play_from_to(self, from_note, to_note, in_pattern=False):
        self.time_sig_beat_val_action()
        print('---------------------')
        # self.numerator_count += 1
        # self.numerator_count %= self.time_signature['numerator']
        # print(f"------------------------------{time.time()=},{self.numerator_count=}")
        print(f"in_pattern: {in_pattern} from_note:{from_note}, to_note: {to_note}")
        print(f"{self.key.scale.name=}, key={iso.Note.names[self.key.tonic % 12]}, {self.key.scale.name=}")

        loopq = self.loopq
        if self.prev_get_pattern_name != self.note_patterns.get_pattern.__name__:
            pass
        if (not self.prev_key and self.key) \
                or self.prev_key != self.key:
            self.meta_key_scale(key=self.key, scale=self.key.scale.name)
        self.set_dur_variety_trk(self.dur_variety)
        self.set_func_trk(self.func_name)
        self.set_align_trk(self.align_state)
        self.set_quantize_trk(self.quants_state)
        self.set_program_change_trk(self.program_change)

        self.prev_key = self.key
        print(f"============={self.prev_get_pattern_name=} {self.note_patterns.get_pattern.__name__=}")
        self.prev_get_pattern_name = self.note_patterns.get_pattern.__name__

        self.scale_name_action()
        # if  from_note == None:
        #     return None
        if in_pattern:
            if loopq and self.last_from_note is not None:
                print(f'note {self.last_from_note=} back to queue')
                self.put_to_queue(self.last_from_note, q_action=False)

            from_note, to_note = self.get_queue_pair()
            if loopq and not to_note:
                to_note = from_note
                self.put_to_queue(from_note)
            print("if in_pattern")
            # from_notex = self.last_note
            # self.last_notex = to_note
            # new_note = to_note
            print(f"in_pattern (next pattern for later):  from_note:{from_note} new_note:{to_note}")
            self.beat = lambda: self.play_from_to(from_note, to_note, in_pattern=True)
            _ = self.get_from_queue()
        else:
            print("else in_pattern")
            if to_note is not None:
                print('is not None', to_note)
                self.beat = lambda: self.play_from_to(to_note, None)
            else:
                print('else ', to_note)
                self.beat = self.beat_none
        self.notes_pair = [from_note, to_note]
        self.queue_content_wrk = [from_note, to_note] + [' '] + [
            list(self.get_queue_content())]
        self.curr_notes_pair_action()
        self.fullq_content_action()
        self.last_from_note = from_note

        if (to_note is None) or (from_note is None):

            from_note = None if not from_note else self.key.scale.indexOf(self.key.nearest_note(from_note))

            return iso.PDict({
                iso.EVENT_NOTE: iso.PDegree(iso.PSequence([from_note], repeats=1), self.key),
                iso.EVENT_DURATION: iso.PSequence(
                    [Fraction(4 * self.time_signature['numerator'], self.time_signature['denominator'])], repeats=1),
                iso.EVENT_AMPLITUDE: iso.PSequence([64], repeats=1),
                iso.EVENT_GATE: iso.PSequence([self.legato], repeats=1)
            })
        print('after_check')
        root_note = self.key.scale.indexOf(self.key.nearest_note(from_note - self.key.tonic % 12))
        note = self.key.scale.indexOf(self.key.nearest_note(to_note - self.key.tonic % 12))
        interval = note - root_note

        pattern = self.note_patterns.get_pattern(interval,
                                                 dur_variety=self.current_dur_variety,
                                                 quantize=self.current_quants_state,
                                                 align=self.current_align_state,
                                                 dot_beat=self.time_signature['numerator'] in (5, 7, 10, 11),
                                                 numerator=self.time_signature['numerator']
                                                 )

        print(f"type of pattern: {type(pattern)=}, {isinstance(pattern, np.ndarray)}")
        pattern_notes = None
        pattern_amplitude = None
        pattern_gate = None
        pattern_duration = None
        if isinstance(pattern, list):
            pattern_notes = pattern
            print(f"----debugx1----{pattern_notes}")
        elif isinstance(pattern, dict):
            pattern_notes = pattern[iso.EVENT_NOTE]
            pattern_amplitude = pattern.get(iso.EVENT_AMPLITUDE)
            pattern_gate = pattern.get(iso.EVENT_GATE)
            pattern_duration = pattern.get(iso.EVENT_DURATION)
            print(f"----debugx2----{pattern_notes}")
        elif not pattern:
            pattern_notes = None
        else:
            raise Exception("No notes returned!!!")
        print(f"----debug----{pattern_notes}, {root_note=}, {type(pattern_notes)=}")
        pattern_notes = [x + root_note if isinstance(x, np.int32) or isinstance(x, np.int64) or isinstance(x, int)
                         else None if not x
        else tuple(map(lambda u: u + root_note, x)) for x in pattern_notes]
        print(f"----debugz2----{pattern_notes}")
        pattern_notes = pattern_notes[:-1]
        len_pattern = len(pattern_notes)
        print(f"----debug----{pattern_notes} {len_pattern=}")

        if pattern_duration is None or pattern_duration == []:
            pattern_duration = [4 * (self.time_signature['numerator'] / self.time_signature['denominator'])
                                / len_pattern] * len_pattern

        if pattern_amplitude is None or pattern_amplitude == []:
            pattern_amplitude = [64]

        if pattern_gate is None or pattern_gate == []:
            pattern_gate = [self.legato]

        if len(pattern_duration) < len_pattern:
            pattern_duration = pattern_duration * int(len_pattern / pattern_duration.size) + 1

        pattern_duration = pattern_duration[:len_pattern]

        pattern_duration = list(map(lambda x: 4 * (
                self.time_signature['numerator'] / self.time_signature['denominator']) * x \
                                              / sum(pattern_duration), pattern_duration))

        print(f"{pattern_duration=}")

        print('Pseq:', list(iso.PSequence(pattern_notes, repeats=1)))
        print('Pseq + Degree - scale:', list(iso.PDegree(iso.PSequence(pattern_notes, repeats=1), self.key.scale)))
        print('Pseq + Degree - key:', list(iso.PDegree(iso.PSequence(pattern_notes, repeats=1), self.key)))
        print('bef Pdict2')
        print('=====================')

        return iso.PDict({
            iso.EVENT_NOTE: iso.PDegree(iso.PSequence(pattern_notes, repeats=1), self.key),
            iso.EVENT_DURATION: iso.PSequence(pattern_duration, repeats=1),
            iso.EVENT_AMPLITUDE: iso.PSequence(pattern_amplitude, repeats=len(pattern_duration)),
            iso.EVENT_GATE: iso.PSequence(pattern_gate, repeats=len(pattern_duration))
        })

    # </editor-fold>
