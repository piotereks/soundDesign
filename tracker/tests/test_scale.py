import pytest
import os
import sys
import json

import isobar as iso
from tracker.app.isobar_fixes import *

def test_scale_get():
    # create scale by name and with "semitones_down"
    assert [scale.get(x, scale_down=False) for x in range(35, 43)] == [60, 62, 63, 65, 67, 69, 71, 72]
    assert [scale.get(x, scale_down=True) for x in range(35, 43)] == [60, 62, 63, 65, 67, 68, 70, 72]

