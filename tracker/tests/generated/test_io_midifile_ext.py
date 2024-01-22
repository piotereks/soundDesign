""" Unit tests for Key """

import os
import pytest

from tracker.app.isobar_fixes import *
from tracker.app.midi_dev import *
# from tracker.app.midi_dev import FileOut, MidiFileManyTracksOutputDevice
from tracker.utils.dump_midi import print_mid
# from tests import dummy_timeline
snoop.install(enabled=False)


@pytest.fixture()
def dummy_timeline():
    filename = 'output.mid'
    timeline = iso.Timeline(output_device=iso.io.DummyOutputDevice(), clock_source=iso.DummyClock())
    # midi_out_device = MidiFileManyTracksOutputDevice(filename=filename)
    # timeline = iso.Timeline(output_device=midi_out_device, clock_source=iso.DummyClock())
    timeline.stop_when_done = True
    return timeline

    # timeline = iso.Timeline(output_device=iso.io.DummyOutputDevice(), clock_source=iso.DummyClock())

    # midi_out_device = MidiFileManyTracksOutputDevice(filename=filename)

    # timeline = iso.Timeline(output_device=iso.io.DummyOutputDevice(), clock_source=iso.DummyClock())
    # timeline = iso.Timeline(output_device=midi_out_device, clock_source=iso.DummyClock())

def test_io_midifile_write_rests(dummy_timeline):
    events = {
        iso.EVENT_NOTE: iso.PSequence([60, None, None, 62], 1),
        iso.EVENT_DURATION: iso.PSequence([0.5, 1.5, 1, 1], 1),
        iso.EVENT_GATE: iso.PSequence([2, 0.5, 1, 1], 1),
        iso.EVENT_AMPLITUDE: iso.PSequence([64, 32, 16, 8], 1)
    }

    midifile = MidiFileManyTracksOutputDevice(filename="output.mid")
    dummy_timeline.output_device = midifile
    dummy_timeline.schedule(events)
    dummy_timeline.run()
    midifile.write()

    d = MidiFileInputDevice("output.mid").read()
    # file_input_device = iso.MidiFileInputDevice(d)

    snoop.install(enabled=True, out='xxx.log', overwrite=True)

    for key in events.keys():
        assert isinstance(d[0][key], iso.PSequence)
        if key == iso.EVENT_NOTE:
            
            for i, note in enumerate(list(events[key])):
                if note is not None:
                    return
            snoop.pp([e or 0 for e in events[key][:i]])
            # print([e or 0 for e in events[key][:i]])
            assert list(d[0][key]) == [e or 0 for e in events[key][:i]]
        else:
            assert list(d[0][key]) == list(events[key])

    os.unlink("output.mid")

# @pytest.mark.skip
# def test_io_midifile_pdict_save(dummy_timeline):
#     events = {
#         iso.EVENT_NOTE: iso.PSequence([60, 62, 64, 67], 1),
#         iso.EVENT_DURATION: iso.PSequence([0.5, 1.5, 1, 1], 1),
#         iso.EVENT_GATE: iso.PSequence([2, 0.5, 1, 1], 1),
#         iso.EVENT_AMPLITUDE: iso.PSequence([64, 32, 16, 8], 1)
#     }
#     pdict = iso.PDict(events)
#     pdict.save("output.mid")
#     d = MidiFileInputDevice("output.mid").read()
#     for key in events.keys():
#         assert isinstance(d[key], iso.PSequence)
#         assert list(d[key]) == list(events[key])
#     os.unlink("output.mid")

def test_test2():
    pass    
 