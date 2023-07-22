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
# file = os.path.join('example_midi', 'Variable_tempo_one_note_mod_double_instr.mid')
file = os.path.join('example_midi', 'Var_tempo_1_trk_sax.mid')
file_input_device = MidiFileInputDevice(file)
patterns = file_input_device.read()
# print("Read pattern containing %d note events" % len(pattern["note"]))
# file_input_device.callback = handle_midi_input


timeline = Timeline()
for pattern in patterns:
# for pattern in [patterns]:
    action = pattern.pop(EVENT_ACTION, None)
    # action_fun  = [lambda x=x: f(timeline, x) for f, x in action]
    # action_funx = iso.PSequence(action_fun)
    action_fun = iso.PSequence([lambda msg=msg: f(timeline, msg) for f, msg in action])
    # xxx = action_fun[11](None)
    if action:
        # timeline.schedule({EVENT_ACTION: action_fun})
        timeline.schedule({EVENT_ACTION: action_fun})
    timeline.schedule(pattern)
timeline.background()
# timeline.run()

x = 1
