import isobar as iso


class Beats:
    # scale = iso.Scale.minor
    scale = iso.Scale.chromatic


    # notes_trip = iso.PSequence([1, 3, 2, 4, 3], repeats=1) +75
    # notes1 = iso.PSequence([1, 3, 2, 4], repeats=1)
    # notes1  = iso.PDegree(notes1, scale) + 66
    # notes2 = iso.PSequence([1, 3, 2, 4, 3, 5], repeats=1) + 72
    # notes3 = iso.PSequence([2, 5, -2], repeats=1) + 61

    dur5_trip = iso.PSequence([1, 1, 1, 1 / 2, 2 / 5], repeats=1)
    dur4 = iso.PSequence([1], repeats=4)
    dur3 = iso.PSequence([1], repeats=3)
    dur6 = iso.PSequence([1], repeats=6)
    dur4_2 = iso.PSequence([1 / 2], repeats=4)
    dur6mix = iso.PSequence([1, 1 / 2], repeats=3)


    notes_trip = iso.PSequence([1, 3, 2, 4, 3], repeats=1) +14
    notes1 = iso.PSequence([1, 3, 2, 4], repeats=1) + 5
    notes2 = iso.PSequence([1, 3, 2, 4, 3, 5], repeats=1) + 11
    notes3 = iso.PSequence([2, 5, -2], repeats=1)

    notes_trip = iso.PSequence([1, 3, 2, 4, 3], repeats=1) +9
    notes1 = iso.PSequence([1, 3, 2, 4], repeats=1) + 3
    notes2 = iso.PSequence([1, 3, 2, 4, 3, 5], repeats=1) + 7
    notes3 = iso.PSequence([2, 5, -2], repeats=1)


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
    bt3 = iso.PDict({"note": notes3.copy(),
                     "duration": dur3.copy()
                     })

    bt2m = iso.PDict({"note": notes2.copy(),
                      "duration": dur6mix.copy()
                      })

# [x['duration'].reset() for x in my_tracker.pattern_array]
# [math.ceil(sum(x['duration'])) for x in my_tracker.pattern_array]
# sum([len(x['duration']) for x in my_tracker.pattern_array])
# [x.note for x in my_tracker.midi_out.miditrack if x.type=='note_on']