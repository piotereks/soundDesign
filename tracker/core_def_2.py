import datetime
import time
import math
import isobar as iso
import pprint
from copy import deepcopy
import inspect

global beat_count
global prev_time
global timeline
global beat
# global midi_out
# global timeline
# global tline1
# global tline2


def whoami_print():
    print(inspect.stack()[1][3])

def lam_beat():
    return lambda : beat()

def __init__():
    global timeline
    global beat
    global beat1
    global beat2
    global beat_count
    global prev_time
    global lam_beat
    whoami_print()
    timeline = init_timeline()
    # beat = beat_none
    beat = beat2
    beat_count = 0
    prev_time = timeline.current_time



def init_timeline():
    whoami_print()

    name = "Microsoft GS Wavetable Synth 0"

    # name = "Bome Virtual MIDI Port 2"
    # name = "Bome Virtual MIDI Port 4"
    # name = "Virtual Midi"
    # name= "loopMIDI 6"

    midi_out = iso.MidiOutputDevice(device_name=name, send_clock=True)
    in_timeline = iso.Timeline(120, output_device=midi_out)
    in_timeline.background()
    return in_timeline


def beat1():
    whoami_print()
    global beat_count
    global prev_time

    print('bt1', beat, beat1, beat2, beat_none)
    print(beat == beat1)
    print(lambda : beat(), beat )


    beat_count += 1

    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    print(
        f"beat1 diff:{diff_time}, timeYY: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
    beat_count %= 4

    notes = iso.PSequence([1, 3, 2, 4], repeats=1)

    xxx = timeline.schedule(
        {"note": notes.copy() + 72
         }
        ,
        replace=True  # this is not working with version 0.1.1, only with github
        , name="blah"  # this is not working with version 0.1.1, only with github

    )


def beat2():
    whoami_print()
    global beat_count
    global prev_time

    print('bt2', beat, beat1, beat2, beat_none)
    print(beat == beat1)
    print(lambda : beat(), beat )

    beat_count += 1


    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    print(
        f"beat2 diff:{diff_time}, timeXX: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
    beat_count %= 4

    notes = iso.PSequence([1, 3, 2, 4, 3, 5], repeats=1)

    xxx = timeline.schedule(
        {"note": notes.copy() + 66
         }
        , replace=True  # this is not working with version 0.1.1, only with github
        , name="blah"  # this is not working with version 0.1.1, only with github
    )


def beat_none():
    whoami_print()
    global beat_count
    global prev_time
    beat_count += 1

    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    print(
        f"beatNone diff:{diff_time}, timeXX: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
    beat_count %= 4

    notes = iso.PSequence([1, 3, 2, 4], repeats=1)

    xxx = timeline.schedule()


def ts():
    whoami_print()
    timeline.stop()


def metronome_start(in_timeline):
    whoami_print()
    # gap = 34
    metronome_audio = in_timeline.schedule({
        # "note": iso.PSequence([1, 5, 5, 5]) +gap,
        # "note": iso.PSequence([82, 69, 69, 69]) ,
        "note": iso.PSequence([32, 37, 37, 37]),
        # "note" : iso.PSeries(1,1),
        "duration": 1,
        "channel": 9,
        "amplitude": iso.PSequence([55, 45, 45, 45]),
        # "quantize": 0
    }
        , quantize=1
        , remove_when_done=False)


def sync_play_start(in_timeline):
    whoami_print()
    # global beat
    timeline.schedule({
        # "action": lam_beat(),
        "action": lambda : beat(),
        "duration": 4,
        # "quantize": 1
    }
        , quantize=1
        , remove_when_done=False)

    # return in_timeline.schedule({
    #     # "action": lam_beat(),
    #     "action": beat(),
    #     "duration": 4,
    #     # "quantize": 1
    # }
    #     , quantize=1
    #     , remove_when_done=False)


class Beats:
    notes_trip = iso.PSequence([1, 3, 2, 4, 3], repeats=1) + 75
    dur5_trip = iso.PSequence([1, 1, 1, 1 / 2, 2 / 5], repeats=1)

    notes1 = iso.PSequence([1, 3, 2, 4], repeats=1) + 66
    notes2 = iso.PSequence([1, 3, 2, 4, 3, 5], repeats=1) + 72
    # durx = iso.PSequence([1, 1 / 2, 1, 1 / 3], repeats=1)
    dur4 = iso.PSequence([1], repeats=4)
    dur6 = iso.PSequence([1], repeats=6)
    dur4_2 = iso.PSequence([1 / 2], repeats=4)
    dur6mix = iso.PSequence([1, 1 / 2], repeats=3)

    bt_trip = iso.PDict({"note": notes_trip.copy(),
                         "duration": dur5_trip.copy()
                         })
    bt1 = iso.PDict({"note": notes1.copy(),
                     "duration": dur4.copy()
                     })

    bt1_2 = iso.PDict({"note": notes1.copy(),
                       "duration": dur4_2.copy()
                       })

    bt2 = iso.PDict({"note": notes2.copy(),
                     "duration": dur6.copy()
                     })

    bt2m = iso.PDict({"note": notes2.copy(),
                      "duration": dur6mix.copy()
                      })

# 31 - sticks, 31 blup, 32,37= edge of tom, 35 - kick, 36 - hard kick, 39 - clap, 42, 44- closed hihat, 51- open hihat
# 54 - tamborine, 56 - cowbell, 60 , 61 - can, 62 - box, 67, 68 - bell, 69 = szczotka, 70 - tick, 73 - box
# 75 blup, 76 , 77- can, 80 - tiny bell, 82 - shaker, 85 - tick


def pplay(initialize: bool = False):
    global beat
    # global cp_PDictbeat
    global idxx
    global pattern_array
    global beat_count
    global prev_time
    global inside_timeline
    beat_count += 1

    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    print(
        f"beatNone diff:{diff_time}, timeXX: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
    beat_count %= 4

    if not initialize:
        pattern_array[idxx].reset()
        inside_timeline = timeline.schedule(
            pattern_array[idxx]
            , replace=True  # this is not working with version 0.1.1, only with github
            , name="blah"  # this is not working with version 0.1.1, only with github
            , quantize=1
            # ,remove_when_done=False
        )
        idxx += 1
        idxx %= len(pattern_array)
    else:
        idxx = 0
        beat = pplay
    pattern_array[idxx].reset()
    print(f"{idxx=} {sum(pattern_array[idxx]['duration'])=}")
    pattern_array[idxx].reset()
    tmln.event_stream['duration'] = math.ceil(sum(pattern_array[idxx]['duration']))
    pattern_array[idxx].reset()
    print(f"{idxx=} {sum(pattern_array[idxx]['duration'])=}")
    print("pplay - END")


__init__()
