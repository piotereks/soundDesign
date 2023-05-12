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

def test_key_index_of():
    scale = iso.Scale.major
    for scalex in iso.Scale.all():
        key = iso.Key(tonic=0, scale=scale)
        print('\n'+scale.name)
            # test_pattern_midi_nr = list(range(0,13))
        for t in range(128):
            key.tonic = t%key.scale.octave_size
            test_pattern_midi_nr = [x+t for x in key.scale.semitones]
            # print(test_pattern_midi_nr)
            result_pattern = [key.nearest_note(x) for x in test_pattern_midi_nr]
            # print(result_pattern)
            # index_pattern = [(x-t%key.scale.octave_size,key.scale.indexOf(x-t%key.scale.octave_size)) for x in result_pattern]
            index_pattern = [key.scale.indexOf(x-key.tonic) for x in result_pattern]

            # assert test_pattern_midi_nr == result_pattern
            rng_start = t//key.scale.octave_size*len(key.scale.semitones)
            pdegree_pattern = list(iso.PDegree(iso.PSequence(index_pattern, repeats=1), key))
            print(result_pattern, index_pattern, pdegree_pattern)
            assert index_pattern == list(range(rng_start, rng_start+len(key.scale.semitones))), "IndexOf error"
            assert result_pattern == pdegree_pattern, f"PDegree error {(key.tonic,key.scale.name)=}"
            # if t>=12:
            #     break
        # break

