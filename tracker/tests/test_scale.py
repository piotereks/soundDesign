import pytest
import os
import sys
import json

import isobar as iso
from tracker.app.isobar_fixes import *

def test_scale_get():
    scale = iso.Scale(semitones=[0, 2 , 4, 6, 8, 10], name="test_scale", octave_size=12,
                                semitones_down =[0, 1, 3, 5, 7, 9, 11])
    assert [scale.get(x, scale_down=False) for x in range(8)] == [0, 2, 4, 6, 8, 10, 12, 14]
    assert [scale.get(x, scale_down=True) for x in range(8)] == [0, 1, 3, 5, 7, 9, 11, 12]


