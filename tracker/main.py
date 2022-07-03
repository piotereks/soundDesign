from core_def import *
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
print('here')
# beat = beatNone(1)
# beat= beat2
timeline.background()
# tmln=init_tl()
gap = 34
print('here2')
# metronome_audio = timeline.schedule({
#     # "note": iso.PSequence([1, 5, 5, 5]) +gap,
#     # "note": iso.PSequence([82, 69, 69, 69]) ,
#     "note": iso.PSequence([32, 37, 37, 37]),
#     # "note" : iso.PSeries(1,1),
#     "duration": 1,
#     "channel": 9,
#     "amplitude": iso.PSequence([55, 45, 45, 45]),
#     # "quantize": 0
# }
#     , quantize=1
#     , remove_when_done=False)
print('here3')
# 31 - sticks, 31 blup, 32,37= edge of tom, 35 - kick, 36 - hard kick, 39 - clap, 42, 44- closed hihat, 51- open hihat
# 54 - tamborine, 56 - cowbell, 60 , 61 - can, 62 - box, 67, 68 - bell, 69 = szczotka, 70 - tick, 73 - box
# 75 blup, 76 , 77- can, 80 - tiny bell, 82 - shaker, 85 - tick


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
print('here4')
pattern_array = [bt1, bt1, bt_trip, bt2, bt1_2, bt2]
pattern_array = [pattern.copy() for pattern in pattern_array]
idxx = 0

print('here5')

