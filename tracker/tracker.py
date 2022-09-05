import time
import isobar as iso
from isobar_fixes import *

# one time init    (this is the best to used globals)
# One time is sufficient, so basically this may be repeated

import inspect
from beats import *
from patterns import *
import pprint
from copy import deepcopy
from queue import Queue
import mido
import math


# global midi_out
global timeline
global tline1
global tline2
global inside_timeline

global IN_COLAB
IN_COLAB = 'google.colab' in sys.modules
NO_MIDI_OUT = mido.get_output_names() == [];


# global beat

global my_tracker


def log_call():
    print(inspect.stack()[1][3])



class Tracker:
    MIDI_OUT_DUMMY = 0
    MIDI_OUT_FILE = 1
    MIDI_OUT_DEVICE = 2

    name = "Microsoft GS Wavetable Synth 0"
    scale = iso.Scale.major
    degree = 0
    key = iso.Key("C", "major")

    # name = "Bome Virtual MIDI Port 2"
    # name = "Bome Virtual MIDI Port 4"
    # name = "Virtual Midi"

    # name= "loopMIDI 6"
    def __init__(self, interval_array=None, note_array=None, midi_note_array=None, midi_out_mode='dummy'):
        read_config_file_scales()
        my_beats = Beats()
        self.root_midi = [('C')]
        self.midi_out = None
        self.track = None
        log_call()
        self.beat_count = 0
        self.diff_time = 0
        self.prev_time = 0
        self.timeline = None
        self.patterns = Patterns()
        self.root_note = 0
        self.last_note = None
        self.note_queue = Queue()
        # self.root_note = None
        self.pattern_idx = 0
        # self.pattern_array = None
        self.pattern_array = [my_beats.bt1, my_beats.bt3, my_beats.bt1,
                              my_beats.bt_trip, my_beats.bt2, my_beats.bt1_2, my_beats.bt2]
        # if note_array:
        self.interval_array = []
        print('note array:', note_array)
        print('interval array:', interval_array)
        self.midi_note_array = midi_note_array
        print("self.midi_note_array:", self.midi_note_array)
        if note_array:
            for index, note in enumerate(note_array + [note_array[0]]) or []:
                # print('index,note:', index, note)
                if index > 0:
                    # print('note - note_array[index-1]:', note - note_array[index-1])
                    self.interval_array.append(note - note_array[index - 1])
                else:
                    self.interval_array.append(note)
        else:
            self.interval_array = interval_array

        print('note array2:', note_array)
        print('interval array2:', interval_array)

        self.init_pattern_array()
        # self.pattern_array = [my_beats.bt1, my_beats.bt_trip]
        # self.pattern_array = [pattern.copy() for pattern in self.pattern_array]
        # 67,69,68,70
        # 63,66,59
        # 67,69,68,70
        # 76,78,77,79,78
        # 73,75,74,76,75,79
        # 67,69,68,70
        # 73,75,74,76,75,79
        self.expected_array = [
            67, 69, 68, 70,
            63, 66, 59,
            67, 69, 68, 70,
            76, 78, 77, 79, 78,
            73, 75, 74, 76, 75, 79,
            67, 69, 68, 70,
            73, 75, 74, 76, 75, 79]

        # self.init_timeline(True)
        self.init_timeline(midi_out_mode)
        self.beat = self.beat_none
        # my_tracker.metronome_start()
        self.tmln = self.tracker_timeline()

    def init_pattern_array(self):
        # print('scales:',iso.Scale.__dict__)
        # print('scales2:',iso.Scale['chromatic'])

        self.pattern_array = []
        patterns = Patterns()
        print('======')
        root_note = self.interval_array[0]
        print("self.interval_array", self.interval_array)
        for interval in self.interval_array[1:]:
            # print('gsp:', interval, patterns.get_random_pattern(interval))
            # print('pre gsp:', interval, root_note)
            rnd_pattern = patterns.get_random_pattern(interval) + root_note
            print('------')
            print('gsp:', interval, root_note, rnd_pattern)
            # print('gsp2:', interval, iso.PSequence(rnd_pattern))
            len_rnd_pattern = len(rnd_pattern) - 1
            notes_seq = iso.PSequence(rnd_pattern[:-1], repeats=1)
            print('gsp2:', interval, len_rnd_pattern, list(notes_seq.copy()))
            beat = iso.PDict({
                "note": notes_seq,
                # "duration": 1/len_rnd_pattern
                "duration": iso.PSequence([(4 / len_rnd_pattern) - 0.000000000000002], repeats=len_rnd_pattern)
            })
            # print("beat:", beat.note, beat.duration)
            print("beatx:", list(beat["note"]), list(beat["duration"]))
            # print("beatx:", list(beat["note"]))
            self.pattern_array.append(beat)
            root_note = rnd_pattern[-1]
            print(f"root note:{root_note}")
        print("init spa2:", self.pattern_array)
        print(list(self.pattern_array))

    def init_timeline(self, midi_out_mode='dummy'):
        log_call()
        print(f" Device:{midi_out_mode}")
        print(f"{NO_MIDI_OUT=}")
        if midi_out_mode == self.MIDI_OUT_FILE:
            filename = "xoutput.mid"
            self.midi_out = iso.MidiFileOutputDevice(filename)
            print("file mode")
        elif midi_out_mode == self.MIDI_OUT_DEVICE and not NO_MIDI_OUT:
            self.midi_out = iso.MidiOutputDevice(device_name=self.name, send_clock=True)
            print("device mode")
        else:
            self.MIDI_OUT_DUMMY
            self.midi_out = iso.DummyOutputDevice()
            print("dummy mode")

        # midi_out = iso.DummyOutputDevice()
        self.timeline = iso.Timeline(120, output_device=self.midi_out)
        self.timeline.background()  # use background ts()instead of run to enable live performing (async notes passing)

    def log_and_schedule(func):
        def inner(self, *args, **kwargs):
            log_call()
            print(func.__name__)
            self.beat_count += 1
            self.diff_time = self.timeline.current_time - self.prev_time
            self.prev_time = self.timeline.current_time
            print(f"{func.__name__} diff:{self.diff_time}, timeXX: {self.timeline.current_time},"
                  f" {round(self.timeline.current_time)} beat: {self.beat_count}\n")
            self.beat_count %= 4
            # print('bef func')
            # print('args: ',*args)
            # print('kwargs: ', ** kwargs)
            notes = func(self, *args, **kwargs)
            # print("result type: ",type(result), result)
            # if type(result) == 'tuple':
            #     notes, skip = result
            # else:
            #     notes, skip = result, False
            # print('skip checked: ', skip)
            # if not skip:
            notes[iso.EVENT_NOTE] = iso.PMap(notes[iso.EVENT_NOTE], lambda midi_note: None if not midi_note else None if midi_note < 0 else None if midi_note > 127 else midi_note)
            print('check notes: ', list(notes[iso.EVENT_NOTE].copy()))
            # print('aft func')
            xxx = self.timeline.schedule(
                notes
                # ,replace=True,  # this is not working with version 0.1.1, only with github
                # name="blah"  # this is not working with version 0.1.1, only with github

            )
            print('post sched')

        return inner

    @log_and_schedule
    def beat_test(self):

        notes = iso.PDict({
            iso.EVENT_NOTE: iso.PSequence(range(-10, 10), repeats=1),
            iso.EVENT_DURATION: 1/5,
            iso.EVENT_OCTAVE: 5
            # iso.EVENT_DEGREE: xxxx
        })
        return notes

    @log_and_schedule
    def beat1(self):
        return iso.PDict({
            iso.EVENT_NOTE:iso.PSequence([1, 3, 2, 4], repeats=1) +72 })

    @log_and_schedule
    def beat2(self):
        return  iso.PDict({
            iso.EVENT_NOTE:iso.PSequence([1, 3, 2, 4, 3, 5], repeats=1) + 66})

    @log_and_schedule
    def beat_none(self):
        return iso.PDict({
            iso.EVENT_NOTE:iso.PSequence([None], repeats=4)})





    def tracker_timeline(self):
        log_call()
        return self.timeline.schedule({
            "action": lambda: self.beat()
            ,"duration": 4
            # "quantize": 1
        }
            , quantize=1
            , remove_when_done=False
        )

    def ts(self):
        log_call()
        self.timeline.stop()

    def tstart(self):
        log_call()
        self.timeline.background()

    def metronome_start(self):
        log_call()
        # gap = 34
        self.metronome_audio = self.timeline.schedule({
            # "note": iso.PSequence([1, 5, 5, 5]) +gap,
            # "note": iso.PSequence([82, 69, 69, 69]) ,
            "note": iso.PSequence([32, 37, 37, 37]),
            # "note" : iso.PSeries(1,1),
            "duration": 1,
            "channel": 9,
            "amplitude": iso.PSequence([55, 45, 45, 45]),
            # "quantize": 1
        }
            , quantize=1
            , remove_when_done=False)

    def metronome_stop(self):
        log_call()
        # gap = 34
        self.metronome_audio.stop()

    @log_and_schedule
    def pplay(self):

        # if self.pattern_idx == 0:
        #     self.scale = iso.Scale.random()
        #     print('scale:', self.scale.name, list(self.scale.semitones))
        #     # note_prev = self.scale.get(self.root_note) + 60 # 60 is midi number of C in 5th Octave

        # if not initialize:
        # key = iso.Key("C", "major")
        print("self.midi_note_array2:", self.midi_note_array)
        print("self.midi_note_array2 cvt:", [self.scale.get(self.scale.indexOf(midi_note)) for midi_note in self.midi_note_array])

        if self.midi_note_array:
            # this is to denominate midi notes to indexes of elements of scale
            mod_midi_note_array = [self.midi_note_array[-1]] + self.midi_note_array+[self.midi_note_array[0]]
            print("mod_midi_note_array:", mod_midi_note_array)

            # note = mod_midi_note_array[self.pattern_idx+1] - 60  # 60 is midi number of C in 5th Octave
            self.root_note = self.scale.indexOf(mod_midi_note_array[self.pattern_idx])
            note = mod_midi_note_array[self.pattern_idx+1]  # 60 is midi number of C in 5th Octave

            print('n1:',note,self.root_note)
            # remember that this function is calculating notes which are not from scale
            # as note with midi code 1 less
            note = self.scale.indexOf(note)
            # note_prev = self.scale.indexOf(note_prev)
            print('n1:',note,self.root_note)
            interval = note - self.root_note
            print('interval:', interval, self.interval_array[self.pattern_idx])
        else:
            interval = self.interval_array[self.pattern_idx]

        rnd_pattern = self.patterns.get_random_pattern(interval) + self.root_note
        print('grp:', interval, rnd_pattern)
        len_rnd_pattern = len(rnd_pattern) - 1
        # print('gsp2:', interval, len_rnd_pattern, iso.PSequence(rnd_pattern[:-1]))
        # base not converted notes pattern
        beat = iso.PDict({
            "note": iso.PSequence(rnd_pattern, repeats=1),
            # "duration": 1/len_rnd_pattern
            "duration": iso.PSequence([(4 / len_rnd_pattern) - 0.000000000000002], repeats=len_rnd_pattern)
        })
        print("before conversion:", list(beat["note"]), list(beat["duration"]))
        self.pattern_array[self.pattern_idx] = beat
        self.root_note = rnd_pattern[-1]
        # self.root_note = self.scale.get(rnd_pattern[-1])  # <-- this conversion is wrong
        print('new root note:', self.root_note)

        self.pattern_array[self.pattern_idx].reset()

        # Degree conversion here with scale
        converted_note = iso.PDegree(self.pattern_array[self.pattern_idx]['note'], self.scale)
        # converted_note = iso.PDegree(self.pattern_array[self.pattern_idx]['note'], self.key) # is this vaiid usage?
        notes = iso.PDict({
            iso.EVENT_NOTE: converted_note,
            iso.EVENT_DURATION: self.pattern_array[self.pattern_idx]['duration'],
            # iso.EVENT_OCTAVE: 5
            # iso.EVENT_DEGREE: xxxx
        })
        print(f'converted with scale {self.scale.name}:', list(converted_note))
        self.pattern_array[self.pattern_idx].reset()

        self.pattern_idx += 1
        self.pattern_idx %= len(self.pattern_array)
        self.pattern_array[self.pattern_idx].reset()
        self.tmln.event_stream['duration'] = math.ceil(sum(self.pattern_array[self.pattern_idx]['duration']))
        self.pattern_array[self.pattern_idx].reset()

        print("pplay - END")
        return notes

    @log_and_schedule
    def pplay_newX(self):

        if self.pattern_idx == 0:
            self.scale = iso.Scale.random()
            print('scale:', self.scale.name, list(self.scale.semitones))
        print("self.midi_note_array2:", self.midi_note_array)
        print("self.midi_note_array2 cvt:",
              [self.scale.get(self.scale.indexOf(midi_note)) for midi_note in self.midi_note_array])

        if self.midi_note_array:
            # this is to denominate midi notes to indexes of elements of scale
            mod_midi_note_array = [self.midi_note_array[-1]] + self.midi_note_array + [self.midi_note_array[0]]
            print("mod_midi_note_array:", mod_midi_note_array)
            # print("function check: ",self.play_from_to(mod_midi_note_array[self.pattern_idx],mod_midi_note_array[self.pattern_idx+1], in_pattern = True))
            # return self.play_from_to(mod_midi_note_array[self.pattern_idx],mod_midi_note_array[self.pattern_idx+1], in_pattern = True), True
            # note = mod_midi_note_array[self.pattern_idx+1] - 60  # 60 is midi number of C in 5th Octave
            self.root_note = self.scale.indexOf(mod_midi_note_array[self.pattern_idx])
            note = mod_midi_note_array[self.pattern_idx + 1]  # 60 is midi number of C in 5th Octave

            print('n1:', note, self.root_note)
            # remember that this function is calculating notes which are not from scale
            # as note with midi code 1 less
            note = self.scale.indexOf(note)
            # note_prev = self.scale.indexOf(note_prev)
            print('n1:', note, self.root_note)
            interval = note - self.root_note
            print('interval:', interval, self.interval_array[self.pattern_idx])
        else:
            interval = self.interval_array[self.pattern_idx]

        rnd_pattern = self.patterns.get_random_pattern(interval) + self.root_note
        print('grp:', interval, rnd_pattern)
        len_rnd_pattern = len(rnd_pattern) - 1
        # print('gsp2:', interval, len_rnd_pattern, iso.PSequence(rnd_pattern[:-1]))
        # base not converted notes pattern
        beat = iso.PDict({
            "note": iso.PSequence(rnd_pattern, repeats=1),
            # "duration": 1/len_rnd_pattern
            "duration": iso.PSequence([(4 / len_rnd_pattern) - 0.000000000000002], repeats=len_rnd_pattern)
        })
        print("before conversion:", list(beat["note"]), list(beat["duration"]))
        self.pattern_array[self.pattern_idx] = beat
        self.root_note = rnd_pattern[-1]
        # self.root_note = self.scale.get(rnd_pattern[-1])  # <-- this conversion is wrong
        print('new root note:', self.root_note)

        self.pattern_array[self.pattern_idx].reset()

        # Degree conversion here with scale
        converted_note = iso.PDegree(self.pattern_array[self.pattern_idx]['note'], self.scale)
        # converted_note = iso.PDegree(self.pattern_array[self.pattern_idx]['note'], self.key) # is this vaiid usage?
        notes = iso.PDict({
            iso.EVENT_NOTE: converted_note,
            iso.EVENT_DURATION: self.pattern_array[self.pattern_idx]['duration'],
            # iso.EVENT_OCTAVE: 5
            # iso.EVENT_DEGREE: xxxx
        })
        print(f'converted with scale {self.scale.name}:', list(converted_note))
        self.pattern_array[self.pattern_idx].reset()

        self.pattern_idx += 1
        self.pattern_idx %= len(self.pattern_array)
        self.pattern_array[self.pattern_idx].reset()
        self.tmln.event_stream['duration'] = math.ceil(sum(self.pattern_array[self.pattern_idx]['duration']))
        self.pattern_array[self.pattern_idx].reset()

        print("pplay - END")
        return notes

    @log_and_schedule
    def beat2(self):
        return  iso.PDict({
            iso.EVENT_NOTE:iso.PSequence([1, 3, 2, 4, 3, 5], repeats=1) + 66})

    @log_and_schedule
    def beat_none(self):
        return iso.PDict({
            iso.EVENT_NOTE: iso.PSequence([None], repeats=4)})



    @log_and_schedule
    def play_from_to_old(self, from_note, to_note, in_pattern=False ):
        print(f"in_pattern: {in_pattern}")
        # if  from_note == None:
        #     return None
        if in_pattern:
            # self.scale = iso.Scale.chromatic
            self.pattern_idx += 1
            self.pattern_idx %= len(self.pattern_array)
            new_note=self.midi_note_array[self.pattern_idx]
            print(f"in_pattern (next pattern for later): idx: {self.pattern_idx} to_note:{to_note} new_note:{new_note}")
            self.beat = lambda: self.play_from_to(to_note, new_note, in_pattern=True)
        else:
            if to_note is not None:
                print('is not None', to_note)
                self.beat = lambda: self.play_from_to(to_note, None)
            else:
                print('else ', to_note)
                self.beat = self.beat_none
        if (to_note is None) or (from_note is None):
          from_note = None if not from_note else self.scale.indexOf(from_note)
          return iso.PDict({
            iso.EVENT_NOTE: iso.PDegree(iso.PSequence([from_note], repeats=1), self.scale),
            iso.EVENT_DURATION: iso.PSequence([4], repeats=1),
            # iso.EVENT_OCTAVE: 5
            # iso.EVENT_DEGREE: xxxx
        })
        print('after_check')
        # root_note = self.scale.indexOf(from_note-60)
        # note = self.scale.indexOf(to_note-60)
        root_note = self.scale.indexOf(from_note)
        note = self.scale.indexOf(to_note)
        interval = note - root_note
        #print(f"{from_note=} {to_note=} {from_note-60=} {to_note-60=}  {root_note=} {note=} {interval=}")

        rnd_pattern = self.patterns.get_random_pattern(interval) + root_note
        len_pattern = len(rnd_pattern)-1

        print('Pseq:', list(iso.PSequence(rnd_pattern, repeats=1)))
        print('Pseq + Degree:', list(iso.PDegree(iso.PSequence(rnd_pattern, repeats=1), self.scale)))
        print('scale name:', self.scale.name)
        print('bef pdict')


        return iso.PDict({
            iso.EVENT_NOTE: iso.PDegree(iso.PSequence(rnd_pattern, repeats=1), self.scale),
            iso.EVENT_DURATION: iso.PSequence([(4 / len_pattern) - 0.000000000000002], repeats=len_pattern),
            # iso.EVENT_OCTAVE: 5
            # iso.EVENT_DEGREE: xxxx
        })


    @log_and_schedule
    def play_from_to(self, from_note, to_note, in_pattern=False ):
        print('---------------------')
        print(f"in_pattern: {in_pattern} from_note:{from_note}, to_note: {to_note}")
        print(f"{self.scale.name=}")
        # if  from_note == None:
        #     return None
        if in_pattern:
            # self.scale = iso.Scale.chromatic
            print("if in_pattern")
            from_note = self.last_note
            to_note = None if self.note_queue.empty() else self.note_queue.get_nowait()
            # to_note = self.note_queue.get_nowait()  # handle empty queue
            self.last_note = to_note
            new_note=to_note
            print(f"in_pattern (next pattern for later):  from_note:{from_note} new_note:{new_note}")
            self.beat = lambda: self.play_from_to(from_note, new_note, in_pattern=True)
        else:
            print("else in_pattern")
            if to_note is not None:
                print('is not None', to_note)
                self.beat = lambda: self.play_from_to(to_note, None)
            else:
                print('else ', to_note)
                self.beat = self.beat_none
        if (to_note is None) or (from_note is None):
          from_note = None if not from_note else self.scale.indexOf(from_note)
          return iso.PDict({
            iso.EVENT_NOTE: iso.PDegree(iso.PSequence([from_note], repeats=1), self.scale),
            iso.EVENT_DURATION: iso.PSequence([4], repeats=1),
            # iso.EVENT_OCTAVE: 5
            # iso.EVENT_DEGREE: xxxx
        })
        print('after_check')
        # root_note = self.scale.indexOf(from_note-60)
        # note = self.scale.indexOf(to_note-60)
        root_note = self.scale.indexOf(from_note)
        note = self.scale.indexOf(to_note)
        interval = note - root_note
        #print(f"{from_note=} {to_note=} {from_note-60=} {to_note-60=}  {root_note=} {note=} {interval=}")

        rnd_pattern = self.patterns.get_random_pattern(interval) + root_note
        len_pattern = len(rnd_pattern)-1

        print('Pseq:', list(iso.PSequence(rnd_pattern, repeats=1)))
        print('Pseq + Degree:', list(iso.PDegree(iso.PSequence(rnd_pattern, repeats=1), self.scale)))
        print('bef Pdict2')
        print('=====================')

        return iso.PDict({
            iso.EVENT_NOTE: iso.PDegree(iso.PSequence(rnd_pattern, repeats=1), self.scale),
            iso.EVENT_DURATION: iso.PSequence([(4 / len_pattern) - 0.000000000000002], repeats=len_pattern),
            # iso.EVENT_OCTAVE: 5
            # iso.EVENT_DEGREE: xxxx
        })

    def pplay_new(self):
        log_call()
        from_note = self.midi_note_array[self.pattern_idx]
        to_note = self.midi_note_array[self.pattern_idx+1]
        #print(f"{self.midi_note_array=} {self.pattern_idx=}")
        #print(f"{from_note=} {to_note=}")
        self.beat = lambda: self.play_from_to(from_note, to_note, in_pattern=True)
        #print(f"{self.midi_note_array=} {self.pattern_idx=}")
        self.pattern_idx += 1
        self.pattern_idx %= len(self.pattern_array)
        # print(f"{self.midi_note_array=} {self.pattern_idx=}")
        print("pplay_new Done")


    def pplay_queueX(self):
        log_call()
        print(1)
        from_note = self.last_note
        to_note = None if self.note_queue.empty() else self.note_queue.get_nowait()
        # if not self.note_queue.empty():
        #     to_note = self.note_queue.get_nowait()
        # else:
        #     to_note = None

        print(1)
        self.last_note = to_note
        print(f"from_note:{from_note} to_note:{to_note}")
        print(1)
        self.beat = lambda: self.play_from_to(from_note, to_note, in_pattern=True)
        print("pplay_queue Done")

    def pplay_queue(self):
        log_call()
        self.play_from_to(None, None, in_pattern=True)
        print("pplay_queue Done")

