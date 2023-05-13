import pytest
import os
import sys
import json

import isobar as iso
from tracker.app.isobar_fixes import *

def test_key_nearest_note():
    scale = iso.Scale.major
    for scale in iso.Scale.all():
        key = iso.Key(tonic=0, scale=scale)
        print('\n'+scale.name)
            # test_pattern_midi_nr = list(range(0,13))
        for t in range(128):
            key.tonic = t
            test_pattern_midi_nr = [x+key.tonic for x in key.scale.semitones]
            print(test_pattern_midi_nr)
            result_pattern = [key.nearest_note(x) for x in test_pattern_midi_nr]
            print(result_pattern)
            assert test_pattern_midi_nr == result_pattern



