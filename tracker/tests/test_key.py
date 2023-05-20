import pytest
import os
import sys
import json

import isobar as iso
from tracker.app.isobar_fixes import *
read_config_file_scales()


def test_key_nearest_note():
    scale = iso.Scale.major

    for scale in iso.Scale.all():
        key = iso.Key(tonic=0, scale=scale)

        for t in range(128):
            print('\n' + scale.name)

            key.tonic = t
            test_pattern_midi_nr = [x+key.tonic for x in key.scale.semitones]
            result_pattern = [key.nearest_note(x) for x in test_pattern_midi_nr]
            print(result_pattern)
            assert test_pattern_midi_nr == result_pattern, "Assert Scale Up"

            if hasattr(scale, 'semitones_down') and scale.semitones_down:
                print("semitones down")
                test_pattern_midi_nr = [x + key.tonic for x in key.scale.semitones_down]
                result_pattern = [key.nearest_note(x, scale_down=True) for x in test_pattern_midi_nr]
                print(result_pattern)
                assert test_pattern_midi_nr == result_pattern, "Assert Scale Down"



