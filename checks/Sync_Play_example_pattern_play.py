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
# name = "Bome Virtual MIDI Port 2"
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

}, remove_when_done=False)


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

pattern_array = [bt1, bt1, bt2, bt1_2, bt2]
pattern_array = [pattern.copy() for pattern in pattern_array]
idxx = 0


def pplay(initialize : bool = False):
    global beat
    # global cp_PDictbeat
    global idxx
    global pattern_array
    if not initialize:
        pattern_array[idxx].reset()
        xxx = timeline.schedule(
            pattern_array[idxx],
            replace=True  # this is not working with version 0.1.1, only with github
            , name="blah"  # this is not working with version 0.1.1, only with github
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
    tmln.event_stream['duration'] = sum(pattern_array[idxx]['duration'])
    pattern_array[idxx].reset()
    print(f"{idxx=} {sum(pattern_array[idxx]['duration'])=}")
    print("pplay - END")


def pat_play(beatDict):
    global beat
    global cp_PDict
    global idxx
    global pattern_array
    print('pat_play')
    pprint.pprint([x.__dict__ for x in pattern_array])
    cp_PDict = deepcopy(beatDict)
    # idxx+=1
    beat = lambda:  xmod_timeline(cp_PDict)
    # print(f"{sum(beatDict['duration'])=} , {tmln.event_stream['duration']=}")
    tmln.event_stream['duration'] = sum(cp_PDict['duration'])
    # print(f"{sum(beatDict['duration'])=} , {tmln.event_stream['duration']=}")
    print("mt - END")

def xmod_timeline(beatDict):
    global beat_count
    global prev_time
    global cp_PDict
    global idxx
    global pattern_array

    print('xmod_timeline')

    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    print(f"mod_timeline diff:{diff_time}, timeXX: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
    cp_PDict=deepcopy(beatDict)
    print(f"{beatDict.__dict__=}, {cp_PDict.__dict__=}")
    # print(pattern_array)
    xxx = timeline.schedule(
        cp_PDict,
        replace=True  # this is not working with version 0.1.1, only with github
        , name="blah"  # this is not working with version 0.1.1, only with github
        ,remove_when_done=False
    )
    print('resubmit')
    idxx += 1
    print(idxx)
    pat_play(pattern_array[idxx])
    # beat = lambda: xmod_timeline(cp_PDict)
    # beat = lambda: xmod_timeline(pattern_array[idxx])

    # print(f"{sum(beatDict['duration'])=} , {tmln.event_stream['duration']=}")
    tmln.event_stream['duration'] = sum(cp_PDict['duration'])
    # print(f"{sum(beatDict['duration'])=} , {tmln.event_stream['duration']=}")

    print("mod_timeline - END")

def ts():
    timeline.stop()


def p1(beatDict):
    global beat
    global cp_PDict1
    global idxx
    global pattern_array
    print(f"{timeline.current_time=} p1")
    # pprint.pprint([x.__dict__ for x in pattern_array])
    cp_PDict1 = deepcopy(beatDict)
    # idxx+=1
    beat = lambda:  xmod_timeline_p1(cp_PDict1)
    # print(f"{sum(beatDict['duration'])=} , {tmln.event_stream['duration']=}")
    # tmln.event_stream['duration'] = sum(cp_PDict1['duration'])
    # print(f"{sum(beatDict['duration'])=} , {tmln.event_stream['duration']=}")
    print(f"====={timeline.current_time=} p1 - END")


def p2(beatDict):
    global beat
    global cp_PDict2
    global idxx
    global pattern_array
    print(f"{timeline.current_time=} p2")
    # pprint.pprint([x.__dict__ for x in pattern_array])
    cp_PDict2 = deepcopy(beatDict)
    # idxx+=1
    beat = lambda:  xmod_timeline_p2(cp_PDict2)
    # print(f"{sum(beatDict['duration'])=} , {tmln.event_stream['duration']=}")
    # tmln.event_stream['duration'] = sum(cp_PDict2['duration'])
    # print(f"{sum(beatDict['duration'])=} , {tmln.event_stream['duration']=}")
    print(f"====={timeline.current_time=} p2 - END")


def xmod_timeline_p1(beatDict):
    global beat_count
    global prev_time
    global cp_PDict1
    global idxx
    global pattern_array

    print(f"{timeline.current_time=}  xmod_timeline_p1")

    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    # print(f"xmod_timeline_p1 diff:{diff_time}, timeXX: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
    cp_PDict1=deepcopy(beatDict)
    # print(f"{beatDict.__dict__=}, {cp_PDict1.__dict__=}")
    # print(pattern_array)
    # nx1.reset()
    xxx = timeline.schedule(
        # cp_PDict1,
        # {"action": lambda: print(f"{timeline.current_time=} check of xmod_timeline_p1 trigger"),
        #  "duration": 4,
        #  "note":notes1.copy()
        #  },
        {
         "duration": 1,
         "note": nx1
         },

        replace=True  # this is not working with version 0.1.1, only with github
        , name="blah"  # this is not working with version 0.1.1, only with github
        # ,remove_when_done=False
    )
    print(f"{timeline.current_time=} resubmit")
    p2(bt2)

    print(f"{timeline.current_time=} xmod_timeline_p1 - END")

def xmod_timeline_p2(beatDict):
    global beat_count
    global prev_time
    global cp_PDict2
    global idxx
    global pattern_array

    print(f"{timeline.current_time=} xmod_timeline_p2")

    diff_time = timeline.current_time - prev_time
    prev_time = timeline.current_time
    # print(f"xmod_timeline_p1 diff:{diff_time}, timeXX: {timeline.current_time}, {round(timeline.current_time)} beat: {beat_count}\n")
    cp_PDict2=deepcopy(beatDict)
    # print(f"{beatDict.__dict__=}, {cp_PDict2.__dict__=}")
    # print(pattern_array)
    # nx2.reset()
    xxx = timeline.schedule(
        # cp_PDict2,
        # {"action": lambda: print(f"{timeline.current_time=} check of xmod_timeline_p2 trigger"),
        #           "duration": 4,
        #  "note": notes2.copy()
        #  },
        {
            "duration": 1,
            "note": nx2
        },

        replace=True  # this is not working with version 0.1.1, only with github
        , name="blah"  # this is not working with version 0.1.1, only with github
        # ,remove_when_done=False
    )
    print(f"{timeline.current_time=} resubmit")
    p1(bt1)

    print(f"{timeline.current_time=} xmod_timeline_p2 - END")


nx1 = iso.PSequence([64, 73, 66, 88], repeats=1)
nx2 = iso.PSequence([66,67,68,69], repeats=1)
