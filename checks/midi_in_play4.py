import sys
# sys.path.append("./")
import os
import mido
# from isobar import *

import pytest

import isobar as iso
from tracker.app.isobar_fixes import *
from tracker.app.mido_fixes import *

# import tracker.app.mido_fixes
from functools import partial
from collections.abc import Iterable


x = 1
# file = os.path.join('example_midi', 'Variable_tempo_one_note_mod.mid')
# file = os.path.join('example_midi', 'Variable_tempo_one_note_mod_double_instr.mid')
# file = os.path.join('checks', 'example_midi', 'pirates.mid')
# file = os.path.join('example_midi', 'pirates.mid')
# file = os.path.join('example_midi', 'Var_tempo_2_trks_sax_piano.mid')
file = os.path.join('example_midi', 'Var_tempo_1_trk_sax_short.mid')
file = os.path.join('example_midi', 'Var_tempo_1_trk_sax_sh2.mid')
file = os.path.join('example_midi', 'Var_tempo_1_trk_sax.mid')
file = os.path.join('example_midi', 'Var_tempo_2_trks_sax_piano.mid')
file = os.path.join('example_midi', '4_notes3.mid')
file = os.path.join('example_midi', '4_notes4.mid')
file_input_device = iso.MidiFileInputDevice(file)
patterns = file_input_device.read()
# print("Read pattern containing %d note events" % len(pattern["note"]))
# file_input_device.callback = handle_midi_input

# timeline = iso.Timeline()
# timeline = iso.Timeline(output_device=midi_out_device)

# midi_out_play_name = 'Microsoft GS Wavetable Synth 0'
# midi_out = midi_out_play_name
tmp_filename = 'test2.mid'
midi_out_play_name = 'Microsoft GS Wavetable Synth 0'
midi_out = midi_out_play_name
midi_out_device = FileOut(device_name=midi_out, filename=tmp_filename, send_clock=True, virtual=False)

# timeline = iso.Timeline(output_device=iso.io.DummyOutputDevice(), clock_source=iso.DummyClock())
timeline = iso.Timeline(output_device=midi_out_device)
timeline.stop_when_done = True


flag = True
if False:
    for pattern in patterns:
    # for pattern in [patterns]:
        action_fun = pattern.pop(iso.EVENT_ACTION, None)
        if action_fun:
            res_fun = []

            action_fun = [partial(f, timeline) for f in action_fun]
            action_fun = iso.PSequence(action_fun, repeats=1)

            timeline.schedule({iso.EVENT_ACTION: action_fun,
                                      iso.EVENT_DURATION: pattern.get(iso.EVENT_DURATION, None)}, remove_when_done=flag)
        else:
            timeline.schedule(pattern, remove_when_done=flag)
timeline.schedule(patterns)
xxx = list(patterns[0]['action'])[0]
xxx()
# timeline.background()
timeline.run()
timeline.output_device.write()
x = 1
print('Processing Done')