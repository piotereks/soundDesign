import json
import os

from .cust_iso_midi_file_in import *
from .cust_timeline import *
from .cust_track import *
from .up_down_key import *
from .up_down_pdegree import *

print("======================isobar fixes=============")


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
    str_note = "%s%d" % (iso.note_names[degree][0], octave)
    frac = math.modf(note)[0]
    if frac > 0:
        str_note = (str_note + " + %2f" % frac)

    return str_note


def read_config_file_scales():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(this_dir, '../config/note_patterns.json')

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
iso.Key._extracted_from_nearest_note = UpDownKey._extracted_from_nearest_note

iso.Key.__contains__ = UpDownKey.__contains__
iso.Key.semitones_down = UpDownKey.semitones_down

iso.PDegree.__init__ = UpDownPDegree.__init__
iso.PDegree.__next__ = UpDownPDegree.__next__

iso.MidiFileInputDevice.__init__ = CustMidiFileInputDevice.__init__
iso.MidiFileInputDevice.read = CustMidiFileInputDevice.read
iso.MidiFileInputDevice.print_obj = CustMidiFileInputDevice.print_obj  # this creates function, not patches
iso.MidiFileInputDevice.set_tempo_callback = CustMidiFileInputDevice.set_tempo_callback  # this creates function, not patches

iso.timeline.event.Event.__init__ = CustEvent.__init__

iso.timeline.Timeline.__init__ = CustTimeline.__init__
iso.timeline.Timeline.schedule = CustTimeline.schedule
iso.timeline.Timeline.tick = CustTimeline.tick
iso.timeline.Timeline.run = CustTimeline.run

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
