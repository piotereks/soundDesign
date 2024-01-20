# import isobar as iso
import pytest

from tracker.app.isobar_fixes import *
from tracker.app.midi_dev import *
from tracker.app.tracker import get_notes_at_beat

# from tracker.app.midi_dev import FileOut, MidiFileManyTracksOutputDevice


# snoop.install(enabled=True, out='output.log', overwrite=True)
snoop.install(out='outputx.log', overwrite=True)
snoop.install(enabled=True)
# snoop.install(enabled=False)
this_dir = Path(__file__).resolve().parent

@pytest.fixture
def dummy_timeline(request):
    play_or_dummy = request.param["play_or_dummy"]
    filename = request.param["filename"]
    midi_out = 'Microsoft GS Wavetable Synth 0'

    if play_or_dummy == 'play':
        midi_out_device = FileOut(device_name=midi_out, filename=filename, send_clock=True, virtual=False)
        timeline = iso.Timeline(output_device=midi_out_device)
    else:
        midi_out_device = MidiFileManyTracksOutputDevice(filename=filename)
        timeline = iso.Timeline(output_device=midi_out_device, clock_source=iso.DummyClock())
    timeline.stop_when_done = True

    return timeline


@pytest.mark.parametrize("dummy_timeline", [{"play_or_dummy": "dummy", "filename": 'legato_check.mid'}], indirect=True)
def test_dur_calc(dummy_timeline):
    # dummy_timeline.schedule()
    filename = this_dir / '..' / 'tests' / 'xoutput_1t_legato1.5.mid'
    filename = this_dir / '..' / 'tests' / 'x1x1a_ne_chord.mid'
    file_input_device = iso.MidiFileInputDevice(filename)
    file_content = file_input_device.read()
    dummy_timeline.schedule(file_content, remove_when_done=True)
    pass

# @pytest.mark.parametrize("dummy_timeline", [{"play_or_dummy": "dummy", "filename": "file1"}], indirect=True)

def test_note_at_beat():
    from itertools import accumulate
    # this_dir = os.path.dirname(os.path.abspath(__file__))
    filename = this_dir / '..' / 'tests' / 'x1x1a.mid'
    filename = this_dir / '..' / 'tests' / 'x1x1b.mid'
    # filename = this_dir / '..' / 'tests' / 'x1x1ax2.mid'
    # filename = this_dir / '..' / 'tests' / 'Pirates of the Caribbean.mid'
    filename = this_dir / '..' / 'tests' / 'xoutput_with_text.mid'
    filename = this_dir / '..' / 'tests' / 'xoutput_1t_legato1.5.mid'
    filename = this_dir / '..' / 'tests' / 'x1x1a_ne_chord.mid'
    file_input_device = iso.MidiFileInputDevice(filename)
    # file_content = file_input_device.read()

    # mid_file = mido.MidiFile(filename)
    # file_input_device.midi_reader.tracks
    # file_input_device.midi_reader.merged_track
    # file_input_device.midi_reader


    #  currently assumed there is on note per position.
    # interested are chords, but also situation where notes in chord have different lenghts
    file_content = file_input_device.read()
    for tr in file_content:
        if tr.get(EVENT_AMPLITUDE):
            tr[EVENT_AMPLITUDE].sequence = [int(a*0.2) for a in tr[EVENT_AMPLITUDE].sequence]

    track = next(f for f in file_content if f.get(EVENT_NOTE))
    durs = list(track[EVENT_DURATION])
    notes = list(track[EVENT_NOTE])
    # durs = [0.5, 1.0, 6.5, 0.5, 1.0, 1.0, 9.5]
    # notes = [50, 51, 52, 53, 54, 55, None]
    result = list(accumulate(durs, lambda x, y: x + y))
    # xxx[0][0].keywords['objects']
    # [t[EVENT_ACTION].sequence[0].keywords['objects'] for t in file_content if t.get(EVENT_ACTION)]
    # rand_result = [0.7380925910636513, 1.5426592173357494, 8.1621390946605, 8.254313008771904, 9.228673171609053, 10.66374474678596, 19.770060113625792]
    notes_at_beat = get_notes_at_beat(notes=notes, durations=durs, quantize=1 / 8, time_signature={'numerator': 5, 'denominator': 8})
    snoop.pp(notes_at_beat)
    x = 1


def test_hanging_rest_test(dummy_timeline):

    def file_beat():
        _ = dummy_timeline.schedule(patterns, remove_when_done=True)
    events1 = {

        iso.EVENT_NOTE: iso.PSequence(sequence=[50, 51, 52, 53], repeats=1)
        , iso.EVENT_DURATION: iso.PSequence(sequence=[1, 1, 1, 1], repeats=1)
        , iso.EVENT_CHANNEL: 0
    }