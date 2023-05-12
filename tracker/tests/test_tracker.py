import pytest
import os
import sys
import json
from tracker.app.isobar_fixes import *

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

def test_play_from_to_result():
    x=1
    # self.play_from_to(from_note, to_note, in_pattern=True)
    scale = iso.Scale.major
    key = iso.Key(4, scale)
    tracker.key=key
    tracker.note_patterns.set_pattern_function('path')
    tracker.put_to_queue(64)
    tracker.put_to_queue(76)
    tracker.quants_state = {'5': 'normal', '3': 'normal', '2': 'normal'}
    patt=tracker.play_from_to(64, 76, in_pattern=True)
    print(list(patt[iso.EVENT_NOTE]))
    print()
    # print(patt[iso.EVENT_NOTE])
    # return iso.PDict({
    #     iso.EVENT_NOTE: iso.PDegree(iso.PSequence(pattern_notes, repeats=1), self.key.scale),
    #     # iso.EVENT_NOTE: iso.PSequence(pattern_notes, repeats=1),
    #     # iso.EVENT_NOTE: pattern_notes,
    #     iso.EVENT_DURATION: iso.PSequence(pattern_duration, repeats=1),
    #     iso.EVENT_AMPLITUDE: iso.PSequence(pattern_amplitude, repeats=len(pattern_duration)),
    #     iso.EVENT_GATE: iso.PSequence(pattern_gate, repeats=len(pattern_duration))
    # })
    assert list(patt[iso.EVENT_NOTE]) == [64, 66, 68, 69, 71, 73, 75]
