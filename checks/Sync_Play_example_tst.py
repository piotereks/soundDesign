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
# global beat


name = "Microsoft GS Wavetable Synth 0"
name = "Bome Virtual MIDI Port 2"
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





# def xxx1():
#     global beat
#     beat_dict = bt1
#     tmln.event_stream['duration'] = iso.PConstant(sum(beat_dict['duration'].copy()))
#     beat = mod_timeline(beat_dict)
#
#
# def xxx2():
#     global beat
#     beat_dict = bt2
#     tmln.event_stream['duration'] = iso.PConstant(sum(beat_dict['duration'].copy()))
#     beat = mod_timeline(beat_dict)


# def beat2():
#     global beat_count
#     global prev_time
#     beat_count += 1
#
#     diff_time = timeline.current_time - prev_time
#     prev_time = timeline.current_time
#     print(f"diff:{diff_time}, timeXX: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
#     beat_count %= 4
#
#     notes = iso.PSequence([1, 3, 2, 4, 3, 5], repeats=1)
#
#     xxx = timeline.schedule(
#         {"note": notes.copy() + 66
#          }
#         , replace=True  # this is not working with version 0.1.1, only with github
#         , name="blah"  # this is not working with version 0.1.1, only with github
#     )

def xbt1():

    ddd = deepcopy(bt1)
    xxx = timeline.schedule(
        ddd,
        replace=True  # this is not working with version 0.1.1, only with github
        , name="blah"  # this is not working with version 0.1.1, only with github
    )
    print("xbt1 End" )
def xbt2():

    ddd = deepcopy(bt2)
    xxx = timeline.schedule(
        ddd,
        replace=True  # this is not working with version 0.1.1, only with github
        , name="blah"  # this is not working with version 0.1.1, only with github
    )
    print("xbt2 End" )

def m_xbt1():
    global beat
    global beat_count
    global prev_time
    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    print(f"xbt1 diff:{diff_time}, timeXX: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
    beat = xbt1
    ddd = dict(bt1)
    siz = sum(ddd['duration'])
    print(siz)
    tmln.event_stream['duration'] = 4
    print("m_xbt1 End" )

def m_xbt2():
    global beat
    global beat_count
    global prev_time
    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    print(f"xbt2 diff:{diff_time}, timeXX: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
    beat = xbt2
    ddd = dict(bt2)
    siz = sum(ddd['duration'])
    print(siz)
    tmln.event_stream['duration'] = 6
    print("m_xbt2 End" )


def to_beatn():
    global beat
    beat = beatNone
    tmln.event_stream['duration']=2
    print("to_beatn End" )

def to_beat2():
    global beat
    beat = beat2
    tmln.event_stream['duration'] = 6
    print("to_beat2 End" )


def mod_timeline(beatDict):
    global beat_count
    global prev_time
    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    print(f"mod_timeline diff:{diff_time}, timeXX: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
    cp_PDict=deepcopy(beatDict)
    xxx = timeline.schedule(
        cp_PDict,
        replace=True  # this is not working with version 0.1.1, only with github
        , name="blah"  # this is not working with version 0.1.1, only with github
    )
    print("mod_timeline - END")


def mt(beatDict):
    global beat
    global cp_PDict
    cp_PDict = deepcopy(beatDict)

    beat = lambda:  mod_timeline(cp_PDict)
    # print(f"{sum(beatDict['duration'])=} , {tmln.event_stream['duration']=}")
    tmln.event_stream['duration'] = sum(cp_PDict['duration'])
    # print(f"{sum(beatDict['duration'])=} , {tmln.event_stream['duration']=}")
    print("mt - END")

beat = beatNone

notes1 = iso.PSequence([1, 3, 2, 4], repeats=1) + 66
notes2 = iso.PSequence([1, 3, 2, 4, 3, 5], repeats=1) + 72
# durx = iso.PSequence([1, 1 / 2, 1, 1 / 3], repeats=1)
dur4 = iso.PSequence([1], repeats=4)
dur6 = iso.PSequence([1], repeats=6)
dur4_2 = iso.PSequence([1 / 2], repeats=4)
dur6mix = iso.PSequence([1, 1 / 2], repeats=3)
bt1 = iso.PDict({"note": notes1,
                 "duration": dur4
                 })

bt1_2 = iso.PDict({"note": notes1,
                   "duration": dur4_2
                   })

bt2 = iso.PDict({"note": notes2,
                 "duration": dur6
                 })

bt2m = iso.PDict({"note": notes2,
                  "duration": dur6mix
                  })

# Run main function beat with duration 4. This one is looping forever.
beat = beatNone
timeline.background()
tmln = timeline.schedule({
    "action": lambda: beat(),
    "duration": 4
})


# To Do - tracker - couple of changes as list that can be used to play changes.
# Interactive example
# mt(bt2)
# mt(bt1)
# mt(bt2m)
# mt(bt1_2)