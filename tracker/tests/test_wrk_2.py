# import isobar as iso
import pytest

from tracker.app.isobar_fixes import *
from tracker.app.midi_dev import *
# from tracker.app.midi_dev import FileOut, MidiFileManyTracksOutputDevice
from tracker.utils.dump_midi import print_mid


# snoop.install(enabled=True, out='output.log', overwrite=True)
snoop.install(out='outputx.log', overwrite=True)
snoop.install(enabled=True)
# snoop.install(enabled=False)


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



# @pytest.mark.parametrize("dummy_timeline", [{"play_or_dummy": "dummy", "filename": "file1"}], indirect=True)

def test_note_at_beat():
    from itertools import accumulate
    import numpy as np
    this_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(this_dir, '..', 'tests', 'x1x1a.mid')
    filename = os.path.join(this_dir, '..', 'tests', 'x1x1b.mid')
    filename = os.path.join(this_dir, '..', 'tests', 'x1x1ax2.mid')
    filename = os.path.join(this_dir, '..', '..', 'x1x1b.mid')
    file_input_device = iso.MidiFileInputDevice(filename)
    file_content = file_input_device.read()
    # mid_file = mido.MidiFile(filename)
    # file_input_device.midi_reader.tracks
    # file_input_device.midi_reader.merged_track
    # file_input_device.midi_reader

    track = next(f for f in file_content if f.get(EVENT_NOTE))
    #  currently assumed there is on note per position.
    # interested are chords, but also situation where notes in chord have different lenghts
    durs = list(track[EVENT_DURATION])
    notes = list(track[EVENT_NOTE])
    # durs = [0.5, 1.0, 6.5, 0.5, 1.0, 1.0, 9.5]
    # notes = [50, 51, 52, 53, 54, 55, None]
    result = list(accumulate(durs, lambda x, y: x + y))

    # rand_result = [0.7380925910636513, 1.5426592173357494, 8.1621390946605, 8.254313008771904, 9.228673171609053, 10.66374474678596, 19.770060113625792]
    get_notes_at_beat(notes=notes, durations=durs, quantize=1/8, time_signature={'numerator': 5, 'denominator': 8})

    x = 1


def get_notes_at_beat(notes, durations, quantize=None, time_signature=None):
    from itertools import accumulate
    import numpy as np
    if time_signature is None:
        time_signature = {'numerator': 4, 'denominator': 4}
    if quantize is None:  #  default value for quantize - half of selected denominator
        quantize = 0.5/time_signature['denominator']

    # quantize = 1 / 8
    # time_signature = {'numerator': 5, 'denominator': 8}
    mod_factor = time_signature['numerator'] * 4 / time_signature['denominator']

    quant_result = [0] + [quantize * math.floor(float(r) / quantize) for r in accumulate(durations, lambda x, y: x + y)]
    snoop.pp(quant_result)
    all_ranges = [(quant_result[i], quant_result[i + 1]) for i in range(len(quant_result) - 1)]
    selected_ranges = []
    selected_notes = []
    for idx, (r_from, r_to) in enumerate(all_ranges):
        snoop.pp(r_from, r_to)
        for x in np.arange((r_from // mod_factor) * mod_factor, ((r_to // mod_factor) + 1) * mod_factor, mod_factor):
            # if x % mod_factor == 0 and r_from <= x < r_to:
            if r_from <= x < r_to:
                selected_ranges.append((r_from, r_to, idx))
                selected_notes.append(notes[idx])
                snoop.pp(x)
                break
    snoop.pp(quant_result, notes)
    snoop.pp(selected_notes, selected_ranges)
    return selected_notes
