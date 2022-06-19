import time
import isobar as iso

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
print(f"xtime: {round(timeline.current_time)}")
global beat_count
beat_count = 0
prev_time = 0


def beat1():
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
    timeline.stop()

beat = beatNone
notes_trip = iso.PSequence([1, 3, 2, 4, 3], repeats=1) + 75
dur5_trip = iso.PSequence([1, 1, 1, 1/2, 2/5], repeats=1)

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

# Run main function beat with duration 4. This one is looping forever.
beat = beatNone
timeline.background()
tmln = timeline.schedule({
    "action": lambda: beat(),
    "duration": 4,
    # "quantize": 1
}
    , quantize=1
    , remove_when_done=False)

gap = 34
metronome_audio = timeline.schedule({
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
# 31 - sticks, 31 blup, 32,37= edge of tom, 35 - kick, 36 - hard kick, 39 - clap, 42, 44- closed hihat, 51- open hihat
# 54 - tamborine, 56 - cowbell, 60 , 61 - can, 62 - box, 67, 68 - bell, 69 = szczotka, 70 - tick, 73 - box
# 75 blup, 76 , 77- can, 80 - tiny bell, 82 - shaker, 85 - tick

def rmetro(inc = 1):
    global gap
    gap += inc
    metronome_audio.event_stream['note'] = iso.PSequence([0, 0, 0, 0]) + gap
def mprint():
    global gap
    print(f"metro: {timeline.current_time} {gap=}")
    # gap += 1

metronome_print = timeline.schedule({
    "action": lambda: mprint(),
    "duration": 1,
    # "quantize": 0
}
    , quantize=1
    , remove_when_done=False)



# To Do - tracker - couple of changes as list that can be used to play changes.
# Interactive example
# mt(bt2)
# mt(bt1)
# mt(bt2m)
# mt(bt1_2)

# events = {
#     iso.EVENT_NOTE: iso.PSequence([60, 62, 64, 67], 1),
#     iso.EVENT_DURATION: iso.PSequence([0.5, 1.5, 1, 1], 1),
#     iso.EVENT_GATE: iso.PSequence([2, 0.5, 1, 1], 1),
#     iso.EVENT_AMPLITUDE: iso.PSequence([64, 32, 16, 8], 1)
# }
# pdict = iso.PDict(events)mt(

# This works as for concatenation
pDictx = iso.PDict({
    'note' : iso.PSequence(list(bt1['note'])+list(bt2['note']),repeats=1),
    'duration' :  iso.PSequence(list(bt1['duration'])+list(bt2['duration']),repeats=1)
    })

pattern_array = [bt1, bt1, bt_trip, bt2, bt1_2, bt2]
pattern_array = [pattern.copy() for pattern in pattern_array]
idxx = 0


def pplay(initialize : bool = False):
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

