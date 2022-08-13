import time
import isobar as iso

# one time init    (this is the best to used globals)
# One time is sufficient, so basically this may be repeated

import inspect
import isobar as iso
from beats import *
from patterns import *
import pprint
from copy import deepcopy

# global midi_out
global timeline
global tline1
global tline2
global inside_timeline

global IN_COLAB
IN_COLAB = 'google.colab' in sys.modules

import math

# global beat

global my_tracker


def log_call():
    print(inspect.stack()[1][3])


class Tracker:
    name = "Microsoft GS Wavetable Synth 0"
    scale = iso.Scale.major
    degree = 0
    key = iso.Key("C", "major")

    # name = "Bome Virtual MIDI Port 2"
    # name = "Bome Virtual MIDI Port 4"
    # name = "Virtual Midi"

    # name= "loopMIDI 6"
    def __init__(self,interval_array=None, note_array=None,  midi_note_array=None,flag_file=False):
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
        self.init_timeline(flag_file)
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

    def init_timeline(self, file_flag=False):
        log_call()
        if file_flag:
            filename = "xoutput.mid"
            self.midi_out = iso.MidiFileOutputDevice(filename)
        else:
            self.midi_out = iso.MidiOutputDevice(device_name=self.name, send_clock=True)
        # midi_out = iso.DummyOutputDevice()
        self.timeline = iso.Timeline(120, output_device=self.midi_out)
        self.timeline.background()  # use background ts()instead of run to enable live performing (async notes passing)

    def beat_test(self):
        log_call()
        # global beat_count
        # global prev_time
        self.beat_count += 1

        self.diff_time = self.timeline.current_time - self.prev_time
        self.prev_time = self.timeline.current_time
        print(
            f"beat_test diff:{self.diff_time}, timeXX: {self.timeline.current_time}, {round(self.timeline.current_time)} beat: {self.beat_count}\n")
        self.beat_count %= 4

        notes = iso.PDict({
            iso.EVENT_NOTE: iso.PSequence(range(-10, 10), repeats=1),
            iso.EVENT_DURATION: 1/5,
            iso.EVENT_OCTAVE: 5
            # iso.EVENT_DEGREE: xxxx
        })

        xxx = self.timeline.schedule(
            notes,
            replace=True,  # this is not working with version 0.1.1, only with github
            name="blah"  # this is not working with version 0.1.1, only with github

        )
    def beat1(self):
        log_call()
        # global beat_count
        # global prev_time
        self.beat_count += 1

        self.diff_time = self.timeline.current_time - self.prev_time
        self.prev_time = self.timeline.current_time
        print(
            f"beat2 diff:{self.diff_time}, timeXX: {self.timeline.current_time}, {round(self.timeline.current_time)} beat: {self.beat_count}\n")
        self.beat_count %= 4

        notes = iso.PSequence([1, 3, 2, 4], repeats=1)

        xxx = self.timeline.schedule(
            {"note": notes.copy() + 72,
             },
            replace=True,  # this is not working with version 0.1.1, only with github
            name="blah"  # this is not working with version 0.1.1, only with github

        )

    def beat2(self):
        log_call()
        # global beat_count
        # global prev_time
        self.beat_count += 1

        self.diff_time = self.timeline.current_time - self.prev_time
        self.prev_time = self.timeline.current_time
        print(
            f"beat2 diff:{self.diff_time}, timeXX: {self.timeline.current_time}, {round(self.timeline.current_time)} beat: {self.beat_count}\n")
        self.beat_count %= 4

        notes = iso.PSequence([1, 3, 2, 4, 3, 5], repeats=1)

        xxx = self.timeline.schedule(
            {"note": notes.copy() + 66
             }
            , replace=True  # this is not working with version 0.1.1, only with github
            , name="blah"  # this is not working with version 0.1.1, only with github
        )

    def beat_none(self):
        log_call()
        print(self)
        print('xxx')
        # global beat_count
        # global prev_time
        self.beat_count += 1

        self.diff_time = self.timeline.current_time - self.prev_time
        self.prev_time = self.timeline.current_time
        print(
            f"beatNone diff:{self.diff_time}, timeXX: {self.timeline.current_time}, {round(self.timeline.current_time)} beat: {self.beat_count}\n")
        self.beat_count %= 4

        notes = iso.PSequence([1, 3, 2, 4], repeats=1)

        xxx = self.timeline.schedule()

    beat = beat_none

    def tracker_timeline(self):
        log_call()
        return self.timeline.schedule({
            "action": lambda: self.beat(),
            "duration": 4,
            "quantize": 1
        }
            , quantize=1
            , remove_when_done=False)

    def ts(self):
        log_call()
        self.timeline.stop()

    def metronome_start(self):
        log_call()
        # gap = 34
        metronome_audio = self.timeline.schedule({
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

    # def pplay(self, initialize: bool = False):
    def pplay_working(self):

        log_call()
        self.beat_count += 1

        self.diff_time = self.timeline.current_time - self.prev_time
        self.prev_time = self.timeline.current_time
        print(f"---\npplay diff:{self.diff_time}, timeXX: {self.timeline.current_time}, {round(self.timeline.current_time)} \
        beat: {self.beat_count}")
        self.beat_count %= 4
        if self.pattern_idx == 0:
            self.scale = iso.Scale.random()
            print('scale:', self.scale.name)

        # if not initialize:
        # key = iso.Key("C", "major")
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

        self.pattern_array[self.pattern_idx].reset()

        # Degree conversion here with scale
        converted_note = iso.PDegree(self.pattern_array[self.pattern_idx]['note'], self.scale)
        # converted_note = iso.PDegree(self.pattern_array[self.pattern_idx]['note'], self.key) # is this vaiid usage?
        xto_play = iso.PDict({
            iso.EVENT_NOTE: converted_note,
            iso.EVENT_DURATION: self.pattern_array[self.pattern_idx]['duration'],
            iso.EVENT_OCTAVE: 5
            # iso.EVENT_DEGREE: xxxx
        })
        print(f'converted with scale {self.scale.name}:', list(converted_note))
        self.pattern_array[self.pattern_idx].reset()
        self.track = self.timeline.schedule(
            # self.pattern_array[self.pattern_idx],
            xto_play,
            replace=True,  # this is not working with version 0.1.1, only with github
            name="blah",  # this is not working with version 0.1.1, only with github
            # quantize=1
            # ,remove_when_done=False
        )
        self.pattern_idx += 1
        self.pattern_idx %= len(self.pattern_array)
        # else:
        #     self.pattern_idx = 0
        #     self.beat = self.pplay
        # self.pattern_array[self.pattern_idx].reset()
        # print(f"{self.pattern_idx=} {sum(self.pattern_array[self.pattern_idx]['duration'])=}")
        # print(
        #     f"self.pattern_idx={self.pattern_idx} sum(self.pattern_array[self.pattern_idx]['duration'])={sum(self.pattern_array[self.pattern_idx]['duration'])}")

        self.pattern_array[self.pattern_idx].reset()
        # These statements need some analysis about sync
        # xxx = math.ceil(sum(self.pattern_array[self.pattern_idx]['duration']))

        # print(math.ceil(sum(self.pattern_array[self.pattern_idx]['duration'])))
        self.pattern_array[self.pattern_idx].reset()
        self.tmln.event_stream['duration'] = math.ceil(sum(self.pattern_array[self.pattern_idx]['duration']))
        # self.tmln.event_stream['duration'] = sum(self.pattern_array[self.pattern_idx]['duration'])
        # print(f"xxx={xxx} self.tmln.event_stream['duration']={self.tmln.event_stream['duration']}")
        self.pattern_array[self.pattern_idx].reset()
        print("pplay - END")
    def pplay(self):

        log_call()
        self.beat_count += 1

        self.diff_time = self.timeline.current_time - self.prev_time
        self.prev_time = self.timeline.current_time
        print(f"---\npplay diff:{self.diff_time}, timeXX: {self.timeline.current_time}, {round(self.timeline.current_time)} \
        beat: {self.beat_count}")
        self.beat_count %= 4
        if self.pattern_idx == 0:
            self.scale = iso.Scale.random()
            print('scale:', self.scale.name, list(self.scale.semitones))
            # note_prev = self.scale.get(self.root_note) + 60 # 60 is midi number of C in 5th Octave

        # if not initialize:
        # key = iso.Key("C", "major")
        print("self.midi_note_array2:", self.midi_note_array)
        print("self.midi_note_array2 cvt:", [self.scale.get(self.scale.indexOf(midi_note)) for midi_note in self.midi_note_array])

        if self.midi_note_array:
            # this is to denominate midi notes to indexes of elements of scale
            mod_midi_note_array = [self.midi_note_array[-1]] + self.midi_note_array+[self.midi_note_array[0]]
            print("mod_midi_note_array:", mod_midi_note_array)

            note = mod_midi_note_array[self.pattern_idx+1] - 60  # 60 is midi number of C in 5th Octave
            # note_prev = mod_midi_note_array[self.pattern_idx] - 60  # 60 is midi number of C in 5th Octave
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
        xto_play = iso.PDict({
            iso.EVENT_NOTE: converted_note,
            iso.EVENT_DURATION: self.pattern_array[self.pattern_idx]['duration'],
            iso.EVENT_OCTAVE: 5
            # iso.EVENT_DEGREE: xxxx
        })
        print(f'converted with scale {self.scale.name}:', list(converted_note))
        self.pattern_array[self.pattern_idx].reset()
        self.track = self.timeline.schedule(
            # self.pattern_array[self.pattern_idx],
            xto_play,
            replace=True,  # this is not working with version 0.1.1, only with github
            name="blah",  # this is not working with version 0.1.1, only with github
            # quantize=1
            # ,remove_when_done=False
        )
        self.pattern_idx += 1
        self.pattern_idx %= len(self.pattern_array)
        # else:
        #     self.pattern_idx = 0
        #     self.beat = self.pplay
        # self.pattern_array[self.pattern_idx].reset()
        # print(f"{self.pattern_idx=} {sum(self.pattern_array[self.pattern_idx]['duration'])=}")
        # print(
        #     f"self.pattern_idx={self.pattern_idx} sum(self.pattern_array[self.pattern_idx]['duration'])={sum(self.pattern_array[self.pattern_idx]['duration'])}")

        self.pattern_array[self.pattern_idx].reset()
        # These statements need some analysis about sync
        # xxx = math.ceil(sum(self.pattern_array[self.pattern_idx]['duration']))

        # print(math.ceil(sum(self.pattern_array[self.pattern_idx]['duration'])))
        self.pattern_array[self.pattern_idx].reset()
        self.tmln.event_stream['duration'] = math.ceil(sum(self.pattern_array[self.pattern_idx]['duration']))
        # self.tmln.event_stream['duration'] = sum(self.pattern_array[self.pattern_idx]['duration'])
        # print(f"xxx={xxx} self.tmln.event_stream['duration']={self.tmln.event_stream['duration']}")
        self.pattern_array[self.pattern_idx].reset()
        print("pplay - END")

