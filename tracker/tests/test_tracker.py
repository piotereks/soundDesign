import pytest
import os
import sys
import json
import contextlib
import random

from tracker.app.isobar_fixes import *
read_config_file_scales()

from tracker.app.tracker import Tracker

this_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(this_dir, '../config/main_config.json')

with open(config_file, 'r') as file:
    loaded_config = json.load(file)
    app_config = loaded_config['app']
    tracker_config = loaded_config['tracker']
    midi_mapping = loaded_config.get('midi_mapping')

# midi_out_flag = Tracker.MIDI_OUT_DUMMY
midi_out_flag = Tracker.MIDI_OUT_MIX_FILE_DEVICE
tracker = Tracker(tracker_config=tracker_config, midi_mapping=midi_mapping, midi_out_mode=midi_out_flag)

ACCENT_BIG_FACTOR = 1.5
ACCENT_MED_FACTOR = 1.25
ACCENT_DEFAULT = 45
ACCENT_BIG = int(ACCENT_DEFAULT * ACCENT_BIG_FACTOR)
ACCENT_MED = int(ACCENT_DEFAULT * ACCENT_MED_FACTOR)


@pytest.fixture()
def init_tracker(numerator):
    tracker.time_signature['numerator'] = numerator
    tracker.time_signature['denominator'] = 4
    tracker.set_default_duration()
    tracker.set_metro_seq()


@pytest.mark.parametrize("numerator, out_patterns", [
    (1, {'note': [32],
         'amplitude': [ACCENT_BIG],
         'duration': [1]}),
    (2, {'note': [32, 37],
         'amplitude': [ACCENT_BIG, ACCENT_MED],
         'duration': [1, 1]}),
    (3, {'note': [32, 37, 37],
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_MED],
         'duration': [1, 1, 1]}),
    (4, {'note': [32, 37, 37, 37],
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT],
         'duration': [1, 1, 1, 1]}),
    (5, {'note': [32, 37, 37, 37],
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT],
         'duration': [1.5, 1.5, 1, 1]}),
    (6, {'note': [32, 37, 37, 37, 37, 37],
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT],
         'duration': [1, 1, 1, 1, 1, 1]}),
    (7, {'note': [32, 37, 37, 37, 37, 37],
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT],
         'duration': [1.5, 1.5, 1, 1, 1, 1]}),
    (8, {'note': [32, 37, 37, 37, 37, 37, 37, 37],
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT,
                       ACCENT_DEFAULT, ACCENT_DEFAULT],
         'duration': [1, 1, 1, 1, 1, 1, 1, 1, ]}),
    (9, {'note': [32, 37, 37, 37, 37, 37, 37, 37, 37],
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT,
                       ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT],
         'duration': [1, 1, 1, 1, 1, 1, 1, 1, 1]}),
    (10, {'note': [32, 37, 37, 37, 37, 37, 37, 37],
          'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT,
                        ACCENT_DEFAULT, ACCENT_DEFAULT, ],
          'duration': [1.5, 1.5, 1.5, 1.5, 1, 1, 1, 1]}),
    (11, {'note': [32, 37, 37, 37, 37, 37, 37, 37],
          'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT,
                        ACCENT_DEFAULT, ACCENT_DEFAULT],
          'duration': [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1, 1]}),
    (12, {'note': [32, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37],
          'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT,
                        ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT],
          'duration': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})
])
def test_metro_play(init_tracker, numerator, out_patterns):
    # sys.stdout = open(os.devnull, 'w')
    tracker.metro_play()
    assert list(tracker.metro_play_patterns['note']) == out_patterns['note']
    assert list(tracker.metro_play_patterns['amplitude']) == out_patterns['amplitude']
    assert list(tracker.metro_play_patterns['duration']) == out_patterns['duration']


# @pytest.mark.parametrize("numerator, accents_dict",
#                          zip(range(1, 13), [{0: ACCENT_BIG_FACTOR}
#                              , {0: ACCENT_BIG_FACTOR, 1.0: ACCENT_MED_FACTOR}
#                              , {0: ACCENT_BIG_FACTOR, 2.0: ACCENT_MED_FACTOR}
#                              , {0: ACCENT_BIG_FACTOR, 2.0: ACCENT_MED_FACTOR}
#                              , {0: ACCENT_BIG_FACTOR, 2.0: ACCENT_MED_FACTOR}
#                              , {0: ACCENT_BIG_FACTOR, 3.0: ACCENT_MED_FACTOR}
#                              , {0: ACCENT_BIG_FACTOR, 4.0: ACCENT_MED_FACTOR}
#                              , {0: ACCENT_BIG_FACTOR, 4.0: ACCENT_MED_FACTOR}
#                              , {0: ACCENT_BIG_FACTOR, 3.0: ACCENT_MED_FACTOR, 6.0: ACCENT_MED_FACTOR}
#                              , {0: ACCENT_BIG_FACTOR, 4.0: ACCENT_MED_FACTOR}
#                              , {0: ACCENT_BIG_FACTOR, 4.0: ACCENT_MED_FACTOR}
#                              , {0: ACCENT_BIG_FACTOR, 3.0: ACCENT_MED_FACTOR, 6.0: ACCENT_MED_FACTOR, 9.0: ACCENT_MED_FACTOR}]))
# def test_set_accents_dict(init_tracker, numerator, accents_dict):  # this test is rather pointless
#     tracker.accents_dict = {}
#     print("\nnumerator: ", numerator, accents_dict)
#     tracker.set_default_duration()
#     print(f"{tracker.default_duration=}, {tracker.accents_dict=}, {tracker.metro_amp=} ,{tracker.time_signature=}")
#     assert tracker.accents_dict == accents_dict
#     # print("accents dict after: ", tracker.accents_dict)
#
#     pass

def test_play_from_to_result(step=3, subset_div=5):
    """
    step=3 to improve time of test in full test suite should be step=1
    """
    # self.play_from_to(from_note, to_note, in_pattern=True)
    # random.choices(list, k=n)
    scale = iso.Scale.major
    scales = iso.Scale.all()
    if subset_div > 1:
        scales = random.choices(scales,k=len(scales)//subset_div)


    for scale in scales:

        print(f"{scale.name=}")
        for t in range(0, 12, step):
            # print(t)
            key = iso.Key(t % scale.octave_size, scale)
            test_semitones = [x + 60 + key.tonic for x in key.scale.semitones]
            # test_semitones = [x+60+key.tonic for x in key.scale.semitones]
            # print(f"{key.scale.__dict__=},{key.scale.__dict__.get('semitones')=}")

            tracker.key = key
            tracker.note_patterns.set_pattern_function('path')
            from_note = 60+key.tonic
            to_note = from_note+key.scale.octave_size
            tracker.quants_state = {'5': 'normal', '3': 'normal', '2': 'normal'}
            with contextlib.redirect_stdout(None):
                tracker.put_to_queue(from_note)
                tracker.put_to_queue(to_note)

                patt=tracker.play_from_to(from_note, to_note, in_pattern=False)

                print(list(patt[iso.EVENT_NOTE]))
                print()


            assert list(patt[iso.EVENT_NOTE]) == test_semitones, f"Play_from_to pattern mismatch {(t,from_note,to_note)=}"


def test_play_from_to_result_rev():
    # self.play_from_to(from_note, to_note, in_pattern=True)
    scale = iso.Scale.major
    scale = iso.Scale(semitones=[0, 2, 4, 6, 8, 10], name="test_scale", octave_size=12,
                                semitones_down =[0, 1, 3, 5, 7, 9, 11])

    # pattern_notes = list(range(7, -1, -1))
    # pattern_notes = list(range(0, -7, -1))
    # key = iso.Key(0, scale)
    # dgr = iso.PDegree(iso.PSequence(pattern_notes, repeats=1), key)
    # res_lst = list(dgr)
    # dgr2 = iso.PDegree(iso.PSequence([36, 35, 34, 33, 32, 31], repeats=1), key)
    # res_lst2 = list(dgr2)

    for scale in iso.Scale.all():
        if not hasattr(scale, 'semitones_down') or not scale.semitones_down:
            continue
        print(f"{scale.name=}")

        for t in range(12):
            # print(t)
            key = iso.Key(t%scale.octave_size, scale)
            # test_semitones = [x+60+key.tonic for x in key.scale.semitones]
            test_semitones = key.scale.semitones_down if hasattr(key.scale, 'semitones_down') else key.scale.semitones
            test_semitones = [x+60+key.tonic for x in test_semitones]
            test_semitones.reverse()
            rev_semitones = [test_semitones[-1]+key.scale.octave_size]+test_semitones[:-1]
            test_semitones = rev_semitones
            tracker.key = key
            tracker.note_patterns.set_pattern_function('path')
            from_note = 60+key.tonic
            to_note = from_note+key.scale.octave_size
            from_note = 60+key.scale.octave_size+key.tonic
            to_note = from_note-key.scale.octave_size
            tracker.quants_state = {'5': 'normal', '3': 'normal', '2': 'normal'}
            with contextlib.redirect_stdout(None):
                pass
                tracker.put_to_queue(from_note)
                tracker.put_to_queue(to_note)

                patt = tracker.play_from_to(from_note, to_note, in_pattern=False)

                print(list(patt[iso.EVENT_NOTE]))
                print()

            assert list(patt[iso.EVENT_NOTE]) == test_semitones, f"Play_from_to pattern mismatch {(t,from_note,to_note)=}"
