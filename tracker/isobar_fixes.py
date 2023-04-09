import isobar as iso
from up_down_scale import *
from up_down_pdegree import *
from up_down_key import *
import math
import sys
# import yaml
import json
global IN_COLAB
IN_COLAB = 'google.colab' in sys.modules
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
    # print('reading config')
   
    config_file = 'reviewed_pattern_cfg.json'
    if IN_COLAB:
        config_file = '/content/SoundDesign/tracker/' + config_file

    with open(config_file, 'r') as file:
        # with open('reviewed_pattern_cfg.yaml', 'r') as file:
        # loaded_yaml = yaml.safe_load(file)
        loaded_json = json.load(file)
    # uuuu = [iso.Scale(scale['semitones'], scale['name']) for scale in loaded_yaml['scales']]
    for scale in loaded_json['scales']:
        for name in scale['name']:
            new_scale = iso.Scale(scale['semitones'], name, semitones_down=scale.get('semitones_down'))

def pattern__next__(self):
    print("pattern__next__")
    raise StopIteration

LENGTH_MAX = 65536
def pattern_all(self, maximum=LENGTH_MAX):
    """
    Returns all output values, up to a maximum length of `maximum`.
    """
    print("pattern_all")
    values = []
    try:
        # do we even need a LENGTH_MAX?
        # if we omit it, .all() will become an alias for list(pattern)
        #  - maybe not such a bad thing.
        for n in range(maximum):
            value = next(self)
            values.append(value)
    except StopIteration:
        pass
    print(f"1.{values=}")

    self.reset()
    print(f"2.{values=}")
    return values

def pattern_nextn(self, count):
    """
    Returns the next `count` output values.
    If fewer than `count` values are generated, return all output values.
    """
    print("pattern_nextn")
    rv = []
    try:
        for n in range(count):
            rv.append(next(self))
    except StopIteration:
        pass

    return rv

iso.util.midi_note_to_note_name = midi_note_to_note_name  #Overwrite original function
iso.Scale.__init__ = UpDownScale.__init__
iso.Scale.__getitem__ = UpDownScale.__getitem__
iso.Scale.get = UpDownScale.get



iso.Key.__init__ = UpDownKey.__init__
iso.Key.get = UpDownKey.get

iso.PDegree.__init__ = UpDownPDegree.__init__
iso.PDegree.__next__ = UpDownPDegree.__next__
# iso.PDegree.all = pattern_all
# iso.PDegree.nextn = pattern_nextn
# iso.PDegree.__next__ = pattern__next__
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

read_config_file_scales()
# xxx = list()
# Degree new degree=41, self.scale_down=True, scale.get(degree, scale_down=self.scale_down)=71

scale = iso.Scale.byname('minor melodic up/down')
key = iso.Key(0, scale)
ppp = scale.get(41, scale_down=True)
print(f"{ppp=}")
# uuu = iso.PDegree(iso.PSequence([72, 71, 69, 67, 65, 63, 62], repeats=1), key)
# uuu = iso.PDegree(iso.PSequence([42, 41, 40, 39, 38, 37, 36, 35], repeats=1), key)
uuu = iso.PDegree(iso.PSequence([41, 40, 39, 38, 37, 36, 35], repeats=1), key)
ooo = list(uuu)
print(f"{ooo=}")
x = 1