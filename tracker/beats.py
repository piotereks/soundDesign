import isobar as iso


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
