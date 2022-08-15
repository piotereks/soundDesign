import isobar as iso
import math
import sys
import yaml
global IN_COLAB
IN_COLAB = 'google.colab' in sys.modules

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
    config_file = 'reviewed_pattern_cfg.yaml'
    if IN_COLAB:
        config_file = '/content/SoundDesign/tracker/' + config_file

    with open(config_file, 'r') as file:
        # with open('reviewed_pattern_cfg.yaml', 'r') as file:
        loaded_yaml = yaml.safe_load(file)
    # uuuu = [iso.Scale(scale['semitones'], scale['name']) for scale in loaded_yaml['scales']]
    for scale in loaded_yaml['scales']:
        for name in scale['name']:
            new_scale = iso.Scale(scale['semitones'],name)

    # TODO:
    # Modify creating scales so that there is one scale, but may have many names
    # (but is that important?) maybe only for random functions

    # print(self.patterns_config)
    # print(self.patterns_config['play_over'])
    # self.patterns = list(map(lambda x: np.array(x['pattern']), self.patterns_config['play_over']['patterns']))
    # print('after list')

    # pprint.pprint(self.patterns_config)


iso.util.midi_note_to_note_name = midi_note_to_note_name  #Overwrite original function
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
