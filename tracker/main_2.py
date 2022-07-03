from core_def import *

# import core_def

# timeline = core_def.timeline
print(timeline)

print(f"xtime: {round(timeline.current_time)}")
global beat_count
global beat

beat = xbeat

beat_count = 0
prev_time = 0


# Run main function beat with duration 4. This one is looping forever.
# beat = beat_none
# timeline.background()  --already handled in init_timeline


metronome_start(timeline)
tsched = sync_play_start(timeline)
print('after def')

#
#
# metronome_print = timeline.schedule({
#     "action": lambda: mprint(),
#     "duration": 1,
#     # "quantize": 0
# }
#     , quantize=1
#     , remove_when_done=False)
#
# # To Do - tracker - couple of changes as list that can be used to play changes.
# # Interactive example
# # mt(bt2)
# # mt(bt1)
# # mt(bt2m)
# # mt(bt1_2)
#
# # events = {
# #     iso.EVENT_NOTE: iso.PSequence([60, 62, 64, 67], 1),
# #     iso.EVENT_DURATION: iso.PSequence([0.5, 1.5, 1, 1], 1),
# #     iso.EVENT_GATE: iso.PSequence([2, 0.5, 1, 1], 1),
# #     iso.EVENT_AMPLITUDE: iso.PSequence([64, 32, 16, 8], 1)
# # }
# # pdict = iso.PDict(events)mt(
#
# # This works as for concatenation
# pDictx = iso.PDict({
#     'note': iso.PSequence(list(bt1['note']) + list(bt2['note']), repeats=1),
#     'duration': iso.PSequence(list(bt1['duration']) + list(bt2['duration']), repeats=1)
# })
#
# pattern_array = [bt1, bt1, bt_trip, bt2, bt1_2, bt2]
# pattern_array = [pattern.copy() for pattern in pattern_array]
# idxx = 0