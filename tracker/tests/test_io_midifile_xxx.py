""" Unit tests for Key """

import os
# from tracker.app.isobar_fixes import *
# from isobar_ext import *
import isobar_ext as iso
# from isobar_ext.io.midifile import MidiFileOutputDevice, MidiFileInputDevice
import pytest
from . import dummy_timeline

def test_io_midifile_write(dummy_timeline):
    events = {
        iso.EVENT_NOTE: iso.PSequence([60, 62, 64, 67], 1),
        iso.EVENT_DURATION: iso.PSequence([0.5, 1.5, 1, 1], 1),
        iso.EVENT_GATE: iso.PSequence([2, 0.5, 1, 1], 1),
        iso.EVENT_AMPLITUDE: iso.PSequence([64, 32, 16, 8], 1)
    }

    midifile = iso.MidiFileOutputDevice("output.mid")
    dummy_timeline.output_device = midifile
    dummy_timeline.schedule(events)
    dummy_timeline.run()
    midifile.write()

    midi_file_in = iso.MidiFileInputDevice("output.mid")
    d = midi_file_in.read(multi_track_file=True)

    for key in events.keys():
        assert isinstance(d[key], iso.PSequence)
        assert list(d[key]) == list(events[key])

    os.unlink("output.mid")

def test_io_midifile_pdict_save(dummy_timeline):
    events = {
        iso.EVENT_NOTE: iso.PSequence([60, 62, 64, 67], 1),
        iso.EVENT_DURATION: iso.PSequence([0.5, 1.5, 1, 1], 1),
        iso.EVENT_GATE: iso.PSequence([2, 0.5, 1, 1], 1),
        iso.EVENT_AMPLITUDE: iso.PSequence([64, 32, 16, 8], 1)
    }
    pdict = iso.PDict(events)
    pdict.save("output.mid")
    d = iso.MidiFileInputDevice("output.mid").read(multi_track_file=True)
    for key in events.keys():
        assert isinstance(d[key], iso.PSequence)
        assert list(d[key]) == list(events[key])
    os.unlink("output.mid")