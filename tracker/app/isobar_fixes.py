import isobar as iso
import os
from .up_down_scale import *
from .up_down_pdegree import *
from .up_down_key import *
import math
import sys
import json

print("======================isobar fixex=============")
def midi_note_to_note_name(note):
    """
    corrected tool function
    Maps a MIDI note index to a note name.
    Supports fractional pitches.
    """
    if (type(note) is not int and type(note) is not float) or (note < 0 or note > 127):
        raise iso.InvalidMIDIPitch()

    degree = int(note) % len(iso.note_names)
    octave = int(note / len(iso.note_names))
    str = "%s%d" % (iso.note_names[degree][0], octave)
    frac = math.modf(note)[0]
    if frac > 0:
        str = (str + " + %2f" % frac)

    return str


def read_config_file_scales():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(this_dir, '../config/reviewed_pattern_cfg.json')

    with open(config_file, 'r') as file:
        loaded_json = json.load(file)
    for scale in loaded_json['scales']:
        for name in scale['name']:
            new_scale = iso.Scale(scale['semitones'], name, semitones_down=scale.get('semitones_down'),
                                  octave_size=scale.get('octave_size', 12))


iso.util.midi_note_to_note_name = midi_note_to_note_name
iso.Scale.__init__ = UpDownScale.__init__
iso.Scale.__getitem__ = UpDownScale.__getitem__
iso.Scale.get = UpDownScale.get
iso.Scale.indexOf = UpDownScale.indexOf


iso.Key.__init__ = UpDownKey.__init__
iso.Key.get = UpDownKey.get
iso.Key.nearest_note = UpDownKey.nearest_note
iso.Key.__contains__ = UpDownKey.__contains__
iso.Key.semitones_down = UpDownKey.semitones_down



iso.PDegree.__init__ = UpDownPDegree.__init__
iso.PDegree.__next__ = UpDownPDegree.__next__

# wrong semitones
del iso.Scale.minor
del iso.Scale.dict['minor']
del iso.Scale.ionian
del iso.Scale.dict['ionian']

del iso.Scale.lydian
del iso.Scale.dict['lydian']

# no such scale
del iso.Scale.maj7
del iso.Scale.dict['maj7']

iso.Scale.minor = iso.Scale([0, 2, 3, 5, 7, 8, 10], "minor")

iso.Scale.minor = iso.Scale([0, 2, 3, 5, 7, 8, 10], "minor natural")
iso.Scale.minor_harm = iso.Scale([0, 2, 3, 5, 7, 8, 11], "minor harmonic")

# read_config_file_scales()
#
# scale = iso.Scale.byname('minor melodic up/down')
# key = iso.Key(0, scale)
# ppp = scale.get(41, scale_down=True)
# print(f"{ppp=}")
# # uuu = iso.PDegree(iso.PSequence([72, 71, 69, 67, 65, 63, 62], repeats=1), key)
# # uuu = iso.PDegree(iso.PSequence([42, 41, 40, 39, 38, 37, 36, 35], repeats=1), key)
# uuu = iso.PDegree(iso.PSequence([41, 40, 39, 38, 37, 36, 35], repeats=1), key)
# ooo = list(uuu)
# print(f"{ooo=}")
# x = 1