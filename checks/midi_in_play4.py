import sys
# sys.path.append("./")
import os
import mido
# from isobar import *

import pytest

import isobar as iso
from tracker.app.isobar_fixes import *

import tracker.app.mido_fixes
from functools import partial



x = 1
# file = os.path.join('example_midi', 'Variable_tempo_one_note_mod.mid')
# file = os.path.join('example_midi', 'Variable_tempo_one_note_mod_double_instr.mid')
# file = os.path.join('checks', 'example_midi', 'pirates.mid')
# file = os.path.join('example_midi', 'pirates.mid')
# file = os.path.join('example_midi', 'Var_tempo_2_trks_sax_piano.mid')
file = os.path.join('example_midi', 'Var_tempo_1_trk_sax.mid')
file_input_device = iso.MidiFileInputDevice(file)
patterns = file_input_device.read()
# print("Read pattern containing %d note events" % len(pattern["note"]))
# file_input_device.callback = handle_midi_input

timeline = iso.Timeline()
# timeline = iso.Timeline(iso.MAX_CLOCK_RATE, output_device=iso.io.DummyOutputDevice(), clock_source=iso.DummyClock())
timeline.stop_when_done = True

for pattern in patterns:
# for pattern in [patterns]:
    action_fun = pattern.pop(iso.EVENT_ACTION, None)
    if action_fun:
        action_fun = [partial(f, timeline) for f in action_fun]
        # action_fun  = [lambda x=x: f(timeline, x) for f, x in action]
        action_fun = iso.PSequence(action_fun, repeats=1)
    # xxx = [lambda msg=msg: f(timeline, msg) for f, msg in action]
    # xxx = [partial(f, msg) for f, msg in action]
    # yyy = list(xxx)
    # action_fun = iso.PSequence(xxx, repeats=1)
    # action_fun = iso.PSequence([lambda msg=msg: f(timeline, msg) for f, msg in action], repeats=1)
    # xxx = action_fun[11](None)
    flag = True
    if action_fun:
        # timeline.schedule({EVENT_ACTION: action_fun})
        timeline.schedule({iso.EVENT_ACTION: action_fun},   remove_when_done=flag)
        # pass
    timeline.schedule(pattern, remove_when_done=flag)
# timeline.background()
timeline.run()

x = 1
print('Processing Done')