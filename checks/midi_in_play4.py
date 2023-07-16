import sys
# sys.path.append("./")
import os
import mido
from isobar import *

from tracker.app.isobar_fixes import *

import tracker.app.mido_fixes


x = 1
# file = os.path.join('example_midi', 'Variable_tempo_one_note_mod.mid')
# file = os.path.join('example_midi', 'Variable_tempo_one_note_mod_double_instr.mid')
# file = os.path.join('checks', 'example_midi', 'pirates.mid')
# file = os.path.join('example_midi', 'pirates.mid')
file = os.path.join('example_midi', 'Variable_tempo_one_note_mod_double_instr.mid')
file_input_device = MidiFileInputDevice(file)
patterns = file_input_device.read()
# print("Read pattern containing %d note events" % len(pattern["note"]))
# file_input_device.callback = handle_midi_input


timeline = Timeline()
for pattern in patterns:
# for pattern in [patterns]:
    action = pattern.pop(EVENT_ACTION, None)
    if action:
        timeline.schedule({EVENT_ACTION: action})
    timeline.schedule(pattern)
timeline.background()
# timeline.run()

x = 1
