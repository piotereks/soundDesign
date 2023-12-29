# import os
import contextlib
import shutil
from datetime import datetime
from itertools import accumulate
from queue import Queue

from .isobar_fixes import *
from .log_call import *
from .midi_dev import *
from .patterns import *

# import pysnooper

NO_MIDI_OUT = mido.get_output_names() == []
ACCENT_BIG_FACTOR = 1.5
ACCENT_MED_FACTOR = 1.25
ACCENT_DEFAULT = 45
ACCENT_BIG = int(ACCENT_DEFAULT * ACCENT_BIG_FACTOR)
ACCENT_MED = int(ACCENT_DEFAULT * ACCENT_MED_FACTOR)

snoop.install(out='output.log', overwrite=True)


# snoop.install(enabled=True)
# snoop.install(enabled=False)

class Tracker:
    # <editor-fold desc="Class init functions">
    MIDI_OUT_DUMMY = 0
    MIDI_OUT_FILE = 1
    MIDI_OUT_DEVICE = 2
    MIDI_OUT_MIX_FILE_DEVICE = 3

    def __init__(self, tracker_config=None,
                 midi_out_mode='dummy',
                 midi_mapping=None,
                 filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "saved_midi_files",
                                       "xoutput.mid")
                 ):
        if midi_mapping is None:
            midi_mapping = {}
        self.notes_at_beat = None
        log_call()

        read_config_file_scales()
        filename_in = tracker_config.get("filename_in")
        if filename_in:
            filename_in = os.path.join(os.path.dirname(os.path.abspath(__file__)), *filename_in)
        self.midi_dev_in = None
        self.midi_file_in = None
        if filename_in:
            self.file_input_device = iso.MidiFileInputDevice(filename_in) if filename_in else None
            self.patterns_from_file = self.file_input_device.read()
            if not isinstance(self.patterns_from_file, list):
                self.patterns_from_file = [self.patterns_from_file]
                # self.file_input_device.midi_reader.tracks
            try:
                if msg := next(m for t in self.file_input_device.midi_reader.tracks
                               for m in t if m.type == 'time_signature'):
                    tracker_config['time_signature'] = {'numerator': msg.numerator, 'denominator': msg.denominator}
            except StopIteration:
                # if time_singature not writtent to file then 4/4 is default
                tracker_config['time_signature'] = {'numerator': 4, 'denominator': 4}

            self.patterns_from_file_duration = max(
                sum(pat[iso.EVENT_DURATION].sequence)
                for pat in self.patterns_from_file
                if pat.get(iso.EVENT_DURATION, None)
            )
            with contextlib.suppress(StopIteration):
                track = next(f for f in self.patterns_from_file if f.get(EVENT_NOTE))
                self._init_notes_at_beat(track=track, time_signature=tracker_config['time_signature'])
                if self.notes_at_beat is not None:
                    pass
                # app_config['queue_content'] = self.notes_at_beat
        else:
            self.patterns_from_file = None

        if self.midi_file_in:
            self.available_channels = (
                set(range(16))
                - { m.channel
                    for t in self.midi_file_in.tracks
                    for m in t
                    if hasattr(m, 'channel')
                }
            ) - {9}
            self.min_channel = min(self.available_channels)
            self.available_channels.remove(self.min_channel)

        self.filename_in_volume = tracker_config.get("filename_in_volume")
        if self.filename_in_volume < 0:
            self.filename_in_volume = 0
        elif self.filename_in_volume >= 127:
            self.filename_in_volume = 127
        self.generated_notes_volume = tracker_config.get("generated_notes_volume")
        if self.generated_notes_volume < 0:
            self.generated_notes_volume = 0
        elif self.generated_notes_volume >= 127:
            self.generated_notes_volume = 127

        self.generated_notes_volume = tracker_config.get("generated_notes_volume")
        self.key = iso.Key("C", "major")
        self.prev_key = None
        self.loopq = False
        self.midi_out = None
        self.track = None
        self.filename = filename

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
        self.beat_count = -1 % 4

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

        self.file_in_timeline()  # file_in_timeline
        self.tracker_timeline()
        self.metro_timeline()
        self.set_program_change_trk(program=self.program_change)

    def _init_notes_at_beat(self, track, time_signature):
        durs = list(track[EVENT_DURATION].copy())
        notes = list(track[EVENT_NOTE].copy())
        self.notes_at_beat = get_notes_at_beat(notes=notes, durations=durs,
                                               quantize=0.5 / time_signature['denominator'],
                                               time_signature=time_signature)

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
            for idx in range(len(self.midi_out.miditrack)):
                self.mid_meta_message(type='end_of_track', time=0, track_idx=idx)

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
                    return None
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
                    if mess.type == 'note_on':
                        btn[1]['state'] = 'down'
                    else:
                        btn[1]['state'] = 'normal'
                else:
                    if mess.type == 'note_on':
                        if btn[1]['state'] == 'down':
                            btn[1]['state'] = 'normal'
                        else:
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

            if message.type in ['note_on', 'note_off']:
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
                    if button:
                        func = oper_to_func.get(button.get('name'))
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
                if knob:
                    func = oper_to_func.get(knob.get('name'))
                    if func:
                        func()
            elif message.type == 'program_change':
                self.program_change = message.program

        midi_in_name = [m[0] for m in itertools.product(mido.get_input_names(), midi_in_name) if
                        m[1] in m[0]]

        if midi_in_name:
            try:
                self.midi_dev_in = ExtendedMidiInputDevice(midi_in_name[0])
            except iso.DeviceNotFoundException:
                print(f"Can't open midi in named'{midi_in_name[0]}. Possibly locked by other application'")
                return
            self.midi_dev_in.callback = midi_in_callback
        else:
            print(f"No midi in with {midi_in_name}")

    # def xplay_mid_file(self):
    #     time_division = self.midi_file_in.ticks_per_beat
    #     start_time = time.time()
    #     elapsed_time = start_time
    #     while not self.midi_file_in.break_flag.is_set():
    #         for msg, msg_track in self.midi_file_in.play(meta_messages=True):
    #             elapsed_time = time.time() - elapsed_time
    #             wait_time = msg.time - elapsed_time
    #
    #             if self.midi_file_in.break_flag.is_set():
    #                 break
    #             if msg.type in ('note_on', 'note_off'):
    #                 if msg.type == 'note_on':
    #                     self.midi_out.note_on(channel=msg.channel, note=msg.note,
    #                                           velocity=int(msg.velocity * self.filename_in_volume / 100))
    #                 else:
    #                     self.midi_out.note_off(channel=msg.channel, note=msg.note)
    #             elif msg.type == 'program_change':
    #                 self.midi_out.program_change(program=msg.program, channel=msg.channel)
    #                 self.mid_meta_message(msg=msg)
    #
    #                 for idx in range(len(self.midi_out.miditrack)):
    #                     self.mid_meta_message(type='end_of_track', time=0, track_idx=idx)
    #
    #             else:
    #                 if msg.type == 'set_tempo':
    #                     self.set_tempo_ui(instance=None, tempo=mido.tempo2bpm(msg.tempo))
    #
    #                 self.mid_meta_message(msg=msg)
    #
    #         else:
    #             self.midi_out.write()
    #             break
    #         break

    # def mid_file_start(self):
    #     print("start of mid file")
    #     if not self.player_thread.is_alive():
    #         self.player_thread.start()
    #     if self.midi_file_in:
    #         self.midi_file_in.run_event.set()
    #         self.midi_file_in.break_flag.clear()

    # def mid_file_pause(self):
    #     if self.midi_file_in:
    #         self.midi_file_in.run_event.clear()

    # def mid_file_stop_end(self):
    #     if self.midi_file_in:
    #         self.midi_file_in.run_event.clear()
    #         self.midi_file_in.break_flag.set()

    def init_timeline(self, midi_in_name, midi_out_name, midi_out_mode='dummy', ):
        log_call()
        filename = self.filename
        if midi_out_name := [
            m[0]
            for m in itertools.product(mido.get_output_names(), midi_out_name)
            if m[1] in m[0]
        ]:
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
            print("device mode")
        else:
            self.midi_out = iso.DummyOutputDevice()
            print("dummy mode")
        self.setup_midi_in(midi_in_name)
        self.mid_meta_message(type='time_signature', numerator=self.time_signature['numerator'],
                              denominator=self.time_signature['denominator'], time=0)
        self.timeline = iso.Timeline(120, output_device=self.midi_out)

    # </editor-fold>

    def get_amp_factor(self):
        accent = self.amp_for_beat_factor.get(self.time_signature['numerator'], {}).get(self.beat_count)
        return accent or 1

    def log_and_schedule(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            log_call()
            print(func.__name__)

            self.beat_count += 1

            self.diff_time = self.timeline.current_time - self.prev_time
            self.prev_time = self.timeline.current_time
            self.beat_count %= 4
            notes = func(self, *args, **kwargs)

            if notes[iso.EVENT_AMPLITUDE]:
                amplitudes = list(notes[iso.EVENT_AMPLITUDE].copy())
                durations = [0] + list(notes[iso.EVENT_DURATION].copy())
                acc_durations = list(accumulate(durations[:-1]))
                for k in self.accents_dict.keys():
                    try:
                        idx = acc_durations.index(k)
                        amplitudes[idx] = int(self.accents_dict[k] * amplitudes[idx])
                    except ValueError:
                        print("key not found")
                amplitudes = list(map(lambda midi_amp: int(midi_amp * self.generated_notes_volume / 100), amplitudes))
                amplitudes = list(map(lambda
                                          midi_amp: 0 if not midi_amp else 0 if midi_amp < 0 else 127 if midi_amp > 127 else midi_amp,
                                      amplitudes))
                notes[iso.EVENT_AMPLITUDE] = iso.PSequence(amplitudes, repeats=1)

                notes[iso.EVENT_DURATION] = iso.PSequence(
                    list(map(lambda x: x - 0.000000000000002, notes[iso.EVENT_DURATION])), repeats=1)

            self.check_notes = list(notes[iso.EVENT_NOTE].copy())

            self.check_notes_action()

            self.timeline.schedule(
                notes
            )
            return notes

        return inner

    # <editor-fold desc="Base beat functions">
    @log_and_schedule
    def beat_none(self):
        return iso.PDict({
            iso.EVENT_NOTE: iso.PSequence([None], repeats=self.time_signature['numerator'])})

    # </editor-fold>

    # <editor-fold desc="Metro functions">

    def metro_timeline(self):
        log_call()
        return self.timeline.schedule({
            "action": lambda track_idx: self.metro_beat(),
            "duration": 4 * (self.time_signature['numerator'] / self.time_signature['denominator'])
        },
            remove_when_done=False
        )

    def metro_none(self):
        log_call()
        self.timeline.schedule({iso.EVENT_ACTION: lambda track_idx: None,
                                iso.EVENT_DURATION: 1
                                },
                               remove_when_done=True)

    def metro_play(self):
        log_call()
        metro_dur = self.default_duration
        metro_seq = self.metro_seq
        metro_amp = self.metro_amp
        self.metro_play_patterns = {
            "note": iso.PSequence(metro_seq, repeats=1),
            "duration": iso.PSequence(metro_dur, repeats=1),
            "channel": 9,
            "amplitude": iso.PSequence(metro_amp, repeats=1)}

        self.timeline.schedule(self.metro_play_patterns, remove_when_done=True)

    def metro_start_stop(self, state):
        if state == 'down':
            print('-----------metro on-----------------')
            self.metro_beat = self.metro_play
        else:
            print('-----------metro off-----------------')
            self.metro_beat = self.metro_none

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

    def set_tempo_ui(self):
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

        if self.notes_pair[0]:
            queue_v += [self.notes_pair[0]]
        if not self.note_queue.empty():
            queue_v += list(self.note_queue.queue)
        return queue_v or 'Empty'

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

    def clear_queue(self, q_action=True):
        self.last_from_note = None
        self.note_queue.queue.clear()
        if q_action:
            self.queue_content_action()
            self.fullq_content_action()

    def get_from_queue(self):

        note_int = None if self.note_queue.empty() else self.note_queue.get_nowait()
        self.queue_content_action()
        self.fullq_content_action()
        return note_int

    # </editor-fold>

    # <editor-fold desc="play functions">

    # <editor-fold desc="play definitions">

    def file_beat(self):
        log_call()
        if not self.patterns_from_file:
            return None
        self.timeline.schedule(copy.deepcopy(self.patterns_from_file), remove_when_done=True)

    def file_in_timeline(self):
        def flatten(lst):
            for item in lst:
                if isinstance(item, (list, tuple)):
                    yield from flatten(item)
                else:
                    yield item

        log_call()

        factor = self.time_signature['numerator'] * 4 / self.time_signature['denominator']
        if self.patterns_from_file:
            dur = self.patterns_from_file_duration
            dur = dur / factor
            if dur > int(dur):
                dur = int(dur) + 1
            dur = dur * factor
        else:
            dur = factor

        return self.timeline.schedule({"action": lambda track_idx: self.file_beat(),
                                       iso.EVENT_DURATION: dur
                                       },
                                      remove_when_done=False)

    def tracker_timeline(self):
        log_call()
        return self.timeline.schedule({
            "action": lambda track_idx: self.beat(),
            "duration": 4 * self.time_signature['numerator'] / self.time_signature['denominator']
        },
            remove_when_done=False)

    def mid_meta_message(self, msg: mido.MetaMessage = None, *args, **kwargs):
        if self.midi_out_mode == self.MIDI_OUT_DEVICE:
            return None
        track_idx = min(kwargs.pop('track_idx', 0), len(self.midi_out.miditrack) - 1)

        if not msg:
            msg = mido.MetaMessage(*args, **kwargs)
        self.midi_out.miditrack[track_idx].append(msg)

    def set_tempo_trk(self, new_tempo):
        log_call()
        if int(self.current_tempo) == int(new_tempo):
            return
        self.current_tempo = int(new_tempo)
        self.timeline.set_tempo(int(new_tempo))
        self.mid_meta_message(type='set_tempo', tempo=mido.bpm2tempo(int(new_tempo)), time=0)
        self.meta_tempo(tempo=round(new_tempo))

    def set_dur_variety_trk(self, new_dur_variety):
        log_call()
        if self.current_dur_variety == new_dur_variety:
            return
        self.current_dur_variety = new_dur_variety
        self.meta_dur_variety(dur_variety=new_dur_variety)

    def set_func_trk(self, new_func):
        log_call()
        if self.current_func == new_func:
            return
        self.current_func = new_func
        self.meta_func(func=new_func)

    def set_align_trk(self, new_align):
        log_call()
        if self.current_align_state == new_align:
            return
        self.current_align_state = new_align
        self.meta_align(align=new_align)

    def set_quantize_trk(self, new_quants):
        log_call()
        if self.current_quants_state == new_quants:
            return
        self.current_quants_state = new_quants
        self.meta_quants(quants=new_quants)

    def set_program_change_trk(self, program=0, channel=0):
        log_call()
        if self.current_program == program:
            return
        self.midi_out.program_change(program=int(program), channel=int(channel))
        self.midi_out.miditrack[0].append(
            mido.Message('program_change', program=int(program), channel=int(channel)))
        self.current_program = program

    def write_mid_text_meta(self, message, track_idx=0):
        self.mid_meta_message(type='text', text=message, time=0, track_idx=track_idx)

    def meta_key_scale(self, key, scale):
        log_call()
        key = iso.Note.names[key.tonic % 12]
        self.write_mid_text_meta(f"scale:{key}-{scale}")

        self.mid_meta_message(type='key_signature', key=f'{key}m', time=0)

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
        # self.mid_file_pause()
        self.timeline.stop()

    def ts(self):
        log_call()
        # self.mid_file_pause()
        self.timeline.stop()

    def tstart(self):
        log_call()
        self.timeline.background()

        # @log_and_schedule

    # </editor-fold>

    @log_and_schedule
    def play_from_to(self, from_note, to_note, in_pattern=False):
        self.time_sig_beat_val_action()
        loopq = self.loopq
        if (not self.prev_key and self.key) \
                or self.prev_key != self.key:
            self.meta_key_scale(key=self.key, scale=self.key.scale.name)
        self.set_dur_variety_trk(self.dur_variety)
        self.set_func_trk(self.func_name)
        self.set_align_trk(self.align_state)
        self.set_quantize_trk(self.quants_state)
        self.set_program_change_trk(self.program_change)

        self.prev_key = self.key
        self.prev_get_pattern_name = self.note_patterns.get_pattern.__name__

        self.scale_name_action()
        to_note_exists = False
        if in_pattern:
            if loopq and self.last_from_note is not None:
                self.put_to_queue(self.last_from_note, q_action=False)

            from_note, to_note = self.get_queue_pair()
            to_note_exists = to_note is not None
            if loopq and not to_note:
                to_note = from_note
                self.put_to_queue(from_note)
            self.beat = lambda: self.play_from_to(from_note, to_note, in_pattern=True)
            self.get_from_queue()
        else:
            if to_note is not None:
                self.beat = lambda: self.play_from_to(to_note, None)
            else:
                self.beat = self.beat_none
        self.notes_pair = [from_note, to_note]
        self.queue_content_wrk = [from_note, to_note] + [' '] + [
            list(self.get_queue_content())]
        self.curr_notes_pair_action()
        self.fullq_content_action()
        self.last_from_note = from_note if to_note_exists else None
        if (to_note is None) or (from_note is None):
            from_note = self.key.scale.indexOf(
                self.key.nearest_note(from_note) - self.key.tonic % 12) if from_note else None

            return iso.PDict({
                iso.EVENT_NOTE: iso.PDegree(iso.PSequence([from_note], repeats=1), self.key),
                iso.EVENT_DURATION: iso.PSequence(
                    [Fraction(4 * self.time_signature['numerator'], self.time_signature['denominator'])], repeats=1),
                iso.EVENT_AMPLITUDE: iso.PSequence([64], repeats=1),
                iso.EVENT_GATE: iso.PSequence([self.legato], repeats=1)
            })
        scale_down = from_note > to_note
        root_note = self.key.scale.indexOf(self.key.nearest_note(from_note, scale_down=scale_down) - self.key.tonic,
                                           scale_down=scale_down)
        note_int = self.key.scale.indexOf(self.key.nearest_note(to_note, scale_down=scale_down) - self.key.tonic,
                                          scale_down=scale_down)

        interval = note_int - root_note
        scale_interval = to_note - from_note

        pattern_int = self.note_patterns.get_pattern(interval,
                                                     dur_variety=self.current_dur_variety,
                                                     quantize=self.current_quants_state,
                                                     align=self.current_align_state,
                                                     dot_beat=self.time_signature['numerator'] in (5, 7, 10, 11),
                                                     numerator=self.time_signature['numerator'],
                                                     scale_interval=scale_interval,
                                                     key=self.key,
                                                     from_note=from_note,
                                                     to_note=to_note,
                                                     root_note=root_note,
                                                     note=note_int
                                                     )

        pattern_notes = None
        pattern_amplitude = None
        pattern_gate = None
        pattern_duration = None
        if isinstance(pattern_int, list):
            pattern_notes = pattern_int
        elif isinstance(pattern_int, dict):
            pattern_notes = pattern_int[iso.EVENT_NOTE]
            pattern_amplitude = pattern_int.get(iso.EVENT_AMPLITUDE)
            pattern_gate = pattern_int.get(iso.EVENT_GATE)
            pattern_duration = pattern_int.get(iso.EVENT_DURATION)
        elif not pattern_int:
            pattern_notes = None
        else:
            raise Exception("No notes returned!!!")
        pattern_notes = [x + root_note if isinstance(x, np.int32) or isinstance(x, np.int64) or isinstance(x, int)
                         else None if not x
        else tuple(map(lambda u: u + root_note, x)) for x in pattern_notes]
        pattern_notes = pattern_notes[:-1]
        len_pattern = len(pattern_notes)

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
        pattern_notes = [x if isinstance(x, np.int32) or isinstance(x, np.int64) or isinstance(x, int)
                         else tuple(map(lambda u: u, x)) if x else None for x in pattern_notes]

        return iso.PDict({
            iso.EVENT_NOTE: iso.PDegree(iso.PSequence(pattern_notes, repeats=1), self.key),
            iso.EVENT_DURATION: iso.PSequence(pattern_duration, repeats=1),
            iso.EVENT_AMPLITUDE: iso.PSequence(pattern_amplitude, repeats=len(pattern_duration)),
            iso.EVENT_GATE: iso.PSequence(pattern_gate, repeats=len(pattern_duration))
        })

    # </editor-fold>


def get_notes_at_beat(notes, durations, quantize=None, time_signature=None):
    if time_signature is None:
        time_signature = {'numerator': 4, 'denominator': 4}
    if quantize is None:  # default value for quantize - half of selected denominator
        quantize = 0.5 / time_signature['denominator']

    # quantize = 1 / 8
    # time_signature = {'numerator': 5, 'denominator': 8}
    mod_factor = time_signature['numerator'] * 4 / time_signature['denominator']

    quant_result = [0] + [quantize * math.floor(float(r) / quantize) for r in accumulate(durations, lambda x, y: x + y)]
    snoop.pp(quant_result)
    all_ranges = [(quant_result[i], quant_result[i + 1]) for i in range(len(quant_result) - 1)]
    selected_ranges = []
    selected_notes = []
    for idx, (r_from, r_to) in enumerate(all_ranges):
        snoop.pp(r_from, r_to)
        for x in np.arange((r_from // mod_factor) * mod_factor, ((r_to // mod_factor) + 1) * mod_factor, mod_factor):
            # if x % mod_factor == 0 and r_from <= x < r_to:
            if r_from <= x < r_to:
                selected_ranges.append((r_from, r_to, idx))
                selected_notes.append(notes[idx])
                snoop.pp(x)
                break
    snoop.pp(quant_result, notes)
    snoop.pp(selected_notes, selected_ranges)
    return selected_notes
