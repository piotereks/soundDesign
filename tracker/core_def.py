import time
import isobar as iso
import inspect
# one time init  (this is the best to used globals)
# One time is sufficient, so basically this may be repeated


import isobar as iso
import pprint
from copy import deepcopy

global midi_out
global timeline
global tline1
global tline2
global inside_timeline
import math
# global beat

gap = None
def whoami_print():
    print('proc:' + inspect.stack()[1][3])

name = "Microsoft GS Wavetable Synth 0"
# name = "Bome Virtual MIDI Port 2"
# name = "Bome Virtual MIDI Port 4"
# name = "Virtual Midi"

# name= "loopMIDI 6"

print('mo in gl:', 'midi_out' in globals())
if 'midi_out' not in locals():
    print('no midiout')
    midi_out = iso.MidiOutputDevice(device_name=name, send_clock=True)

else:
    print('yes: midi out')

if 'timeline' not in locals():
    print('creating timeline')
    timeline = iso.Timeline(120, output_device=midi_out)
    timeline.background()  # use background instead of run to enable live performing (async notes passing)
else:
    print('reusing timeline')

# filename = "output.mid"
# output = iso.MidiFileOutputDevice(filename)
# # iso.MAX_CLOCK_RATE
# timeline = iso.Timeline(120, output_device=output)
# # timeline = iso.Timeline(iso.MAX_CLOCK_RATE, output_device=output)
# timeline.stop_when_done = True
print(f"xxtime: {round(timeline.current_time)}")
global beat_count
beat_count = 0
prev_time = 0


def beat1():
    whoami_print()

    global beat_count
    global prev_time
    beat_count += 1

    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    print(f"beat1 diff:{diff_time}, timeYY: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
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
    beat_count += 1

    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    print(f"beat2 diff:{diff_time}, timeXX: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
    beat_count %= 4

    notes = iso.PSequence([1, 3, 2, 4, 3, 5], repeats=1)

    xxx = timeline.schedule(
        {"note": notes.copy() + 66
         }
        , replace=True  # this is not working with version 0.1.1, only with github
        , name="blah"  # this is not working with version 0.1.1, only with github
    )


def beatNone():
    whoami_print()
    global beat_count
    global prev_time
    beat_count += 1

    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    print(f"beatNone diff:{diff_time}, timeXX: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
    beat_count %= 4

    notes = iso.PSequence([1, 3, 2, 4], repeats=1)

    xxx = timeline.schedule()






def ts():
    whoami_print()
    timeline.stop()



def rmetro(inc = 1):
    global gap
    whoami_print()
    gap += inc
    metronome_audio.event_stream['note'] = iso.PSequence([0, 0, 0, 0]) + gap
def mprint():
    global gap
    whoami_print()
    print(f"metro: {timeline.current_time} {gap=}")
    # gap += 1

# metronome_print = timeline.schedule({
#     "action": lambda: mprint(),
#     "duration": 1,
#     # "quantize": 0
# }
#     , quantize=1
#     , remove_when_done=False)






def pplay(initialize : bool = False):
    global beat
    # global cp_PDictbeat
    global idxx
    global pattern_array
    global beat_count
    global prev_time
    global inside_timeline
    whoami_print()
    beat_count += 1

    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    print(f"beatNone diff:{diff_time}, timeXX: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
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

beat = beat2
def init_tl():
    global beat
    whoami_print()
    lam = lambda: beat()
    return  timeline.schedule({
        "action": lam,
        "duration": 4,
        # "quantize": 1
    }
        , quantize=1
        , remove_when_done=False)

x=1
print('----------')
print(beat)
timeline.schedule({
        "action": lambda x : beat(),
        "args": {
                "x": 1
            },
        "duration": 4,
        # "quantize": 1
    }
        , quantize=1
        , remove_when_done=False)
