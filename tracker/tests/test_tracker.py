import pytest
import os
import sys
import json

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
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_DEFAULT],
         'duration': [1, 1, 1, 1, 1, 1, 1, 1, ]}),
    (9, {'note': [32, 37, 37, 37, 37, 37, 37, 37, 37],
         'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT],
         'duration': [1, 1, 1, 1, 1, 1, 1, 1, 1]}),
    (10, {'note': [32, 37, 37, 37, 37, 37, 37, 37],
          'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_DEFAULT, ],
          'duration': [1.5, 1.5, 1.5, 1.5, 1, 1, 1, 1]}),
    (11, {'note': [32, 37, 37, 37, 37, 37, 37, 37],
          'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_DEFAULT],
          'duration': [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1, 1]}),
    (12, {'note': [32, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37],
          'amplitude': [ACCENT_BIG, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT, ACCENT_MED, ACCENT_DEFAULT, ACCENT_DEFAULT],
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
