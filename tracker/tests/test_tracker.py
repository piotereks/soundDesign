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


@pytest.mark.parametrize("numerator, out_patterns", [
    (1, {'note': [32],
         'amplitude': [55],
         'duration': [1]}),
    (2, {'note': [32, 37],
         'amplitude': [55, 50],
         'duration': [1, 1]}),
    (3, {'note': [32, 37, 37],
         'amplitude': [55, 45, 50],
         'duration': [1, 1, 1]}),
    (4, {'note': [32, 37, 37, 37],
         'amplitude': [55, 45, 50, 45],
         'duration': [1, 1, 1, 1]}),
    (5, {'note': [32, 37, 37, 37],
         'amplitude': [55, 45, 50, 45],
         'duration': [1.5, 1.5, 1, 1]}),
    (6, {'note': [32, 37, 37, 37, 37, 37],
         'amplitude': [55, 45, 45, 50, 45, 45],
         'duration': [1, 1, 1, 1, 1, 1]}),
    (7, {'note': [32, 37, 37, 37, 37, 37],
         'amplitude': [55, 45, 45, 45, 50, 45],
         'duration': [1.5, 1.5, 1, 1, 1, 1]}),
    (8, {'note': [32, 37, 37, 37, 37, 37, 37, 37],
         'amplitude': [55, 45, 45, 45, 50, 45, 45, 45],
         'duration': [1, 1, 1, 1, 1, 1, 1, 1, ]}),
    (9, {'note': [32, 37, 37, 37, 37, 37, 37, 37, 37],
         'amplitude': [55, 45, 45, 50, 45, 45, 50, 45, 45],
         'duration': [1, 1, 1, 1, 1, 1, 1, 1, 1]}),
    (10, {'note': [32, 37, 37, 37, 37, 37, 37, 37],
          'amplitude': [55, 45, 45, 45, 50, 45, 45, 45, ],
          'duration': [1.5, 1.5, 1.5, 1.5, 1, 1, 1, 1]}),
    (11, {'note': [32, 37, 37, 37, 37, 37, 37, 37],
          'amplitude': [55, 45, 45, 45, 50, 45, 45, 45],
          'duration': [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1, 1]}),
    (12, {'note': [32, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37],
          'amplitude': [55, 45, 45, 50, 45, 45, 50, 45, 45, 50, 45, 45],
          'duration': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    # ,
    # (3, True),
    # (4, True)
])
def test_metro_play(numerator, out_patterns):
    # sys.stdout = open(os.devnull, 'w')
    tracker.time_signature['numerator'] = numerator
    tracker.time_signature['denominator'] = 4
    tracker.metro_play()
    assert list(tracker.metro_play_patterns['note']) == out_patterns['note']
    assert list(tracker.metro_play_patterns['amplitude']) == out_patterns['amplitude']
    assert list(tracker.metro_play_patterns['duration']) == out_patterns['duration']

#
# metro_seq = [32] + [37] * (self.time_signature['numerator'] - 1 - factor)
# metro_amp = [55] + [45] * (self.time_signature['numerator'] - 1 - factor)
# # metro_dur = [4/self.time_signature['denominator']] * self.time_signature['numerator']
# metro_dur = [6 / self.time_signature['denominator']] * (2 * factor) + [4 / self.time_signature['denominator']] \
#             * (self.time_signature['numerator'] - 3 * factor)
