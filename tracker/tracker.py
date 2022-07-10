import time
import isobar as iso

# one time init    (this is the best to used globals)
# One time is sufficient, so basically this may be repeated

import inspect
import isobar as iso
from beats import *
import pprint
from copy import deepcopy

# global midi_out
global timeline
global tline1
global tline2
global inside_timeline


import math
# global beat

global my_tracker

def log_call():
    print(inspect.stack()[1][3])


class Tracker:
    name = "Microsoft GS Wavetable Synth 0"
    scale = iso.Scale.major
    degree = 0
    key = iso.Key("C","major")
    # name = "Bome Virtual MIDI Port 2"
    # name = "Bome Virtual MIDI Port 4"
    # name = "Virtual Midi"

    # name= "loopMIDI 6"
    def __init__(self):
        my_beats = Beats()
        self.midi_out = None
        self.track = None
        log_call()
        self.beat_count = 0
        self.diff_time = 0
        self.prev_time = 0
        self.timeline = None
        self.pattern_idx = 0
        # self.pattern_array = None
        self.pattern_array = [my_beats.bt1, my_beats.bt3, my_beats.bt1,
                              my_beats.bt_trip, my_beats.bt2, my_beats.bt1_2, my_beats.bt2]
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
        self.init_timeline()
        self.beat = self.beat_none
        # my_tracker.metronome_start()
        self.tmln = self.tracker_timeline()

    def init_timeline(self, file_flag=False):
        log_call()
        if file_flag:
            filename = "output.mid"
            self.midi_out = iso.MidiFileOutputDevice(filename)
        else:
            self.midi_out = iso.MidiOutputDevice(device_name=self.name, send_clock=True)

        # midi_out = iso.DummyOutputDevice()
        self.timeline = iso.Timeline(120, output_device=self.midi_out)
        self.timeline.background()  # use background ts()instead of run to enable live performing (async notes passing)

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

    def pplay(self, initialize: bool = False):
        # global beat
        # global cp_PDictbeat
        # global idxx
        # global pattern_array
        # global beat_count
        # global prev_time
        # global inside_timeline
        log_call()
        self.beat_count += 1

        self.diff_time = self.timeline.current_time - self.prev_time
        self.prev_time = self.timeline.current_time
        print(f"pplay diff:{self.diff_time}, timeXX: {self.timeline.current_time}, {round(self.timeline.current_time)} \
        beat: {self.beat_count}\n")
        self.beat_count %= 4

        if not initialize:
            # key = iso.Key("C", "major")
            print('not init')
            self.pattern_array[self.pattern_idx].reset()
            print('b:',list(self.pattern_array[self.pattern_idx]['note']))
            self.pattern_array[self.pattern_idx].reset()
            # xxxx = iso.PDegree(self.pattern_array[self.pattern_idx]['note'], self.scale) + 61
            xxxx = iso.PDegree(self.pattern_array[self.pattern_idx]['note'], self.key)
            xto_play = iso.PDict({
                                 iso.EVENT_NOTE: xxxx,
                                   iso.EVENT_DURATION: self.pattern_array[self.pattern_idx]['duration'],
                                   iso.EVENT_OCTAVE: 5
                                   # iso.EVENT_DEGREE: xxxx
            })
            print('a:',list(xxxx))
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
        else:
            self.pattern_idx = 0
            self.beat = self.pplay
        self.pattern_array[self.pattern_idx].reset()
        print(f"{self.pattern_idx=} {sum(self.pattern_array[self.pattern_idx]['duration'])=}")

        self.pattern_array[self.pattern_idx].reset()
        # These statements need some analysis about sync
        xxx = math.ceil(sum(self.pattern_array[self.pattern_idx]['duration']))

        # print(math.ceil(sum(self.pattern_array[self.pattern_idx]['duration'])))
        self.pattern_array[self.pattern_idx].reset()
        self.tmln.event_stream['duration'] = math.ceil(sum(self.pattern_array[self.pattern_idx]['duration']))
        # self.tmln.event_stream['duration'] = sum(self.pattern_array[self.pattern_idx]['duration'])
        print(f"{xxx=} {self.tmln.event_stream['duration']=}")
        self.pattern_array[self.pattern_idx].reset()
        print("pplay - END")


def ts():
    global my_tracker
    my_tracker.ts()


def sbt1():
    my_tracker.beat = my_tracker.beat1


def sbt2():
    my_tracker.beat = my_tracker.beat2


def sbtn():
    my_tracker.beat = my_tracker.beat_none


def sbtp():
    my_tracker.beat = my_tracker.pplay


def save_midi():
    my_tracker.midi_out.write()


def cmp():
    # print('expected:\n', my_tracker.expected_array)
    print('expected:\n', [y for x in my_tracker.pattern_array for y in list(x['note'])])
    print('played:\n', [x.note for x in my_tracker.midi_out.miditrack if x.type == 'note_on'])


def main():
    global my_tracker
    log_call()
    my_tracker = Tracker()
    print(my_tracker)
    # my_tracker.init_timeline()
    # tracker.beat = tracker.beat_none
    # my_tracker.beat = my_tracker.beat1
    # my_tracker.metronome_start()
    # tmln = tracker.tracker_timeline()
    # pprint.pprint(tmln.__dict__)


if __name__ == '__main__':
    main()
    print('Processing Done.')