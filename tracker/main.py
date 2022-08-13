from tracker import *
from patterns import *
global IN_COLAB
IN_COLAB = 'google.colab' in sys.modules

def ts():
    global my_tracker
    my_tracker.ts()


def sbt1():
    my_tracker.beat = my_tracker.beat1


def sbt2():
    my_tracker.beat = my_tracker.beat2


def sbtn():
    my_tracker.beat = my_tracker.beat_none


def sbtt():
    my_tracker.beat = my_tracker.beat_test

def sbtp():
    my_tracker.beat = my_tracker.pplay


def save_midi():
    my_tracker.midi_out.write()


def cmp():
    # print('expected:\n', my_tracker.expected_array)
    print('expected:\n', [y for x in my_tracker.pattern_array for y in list(x['note'])])
    print('played:\n', [x.note for x in my_tracker.midi_out.miditrack if x.type == 'note_on'])

# speeding up and slowing down tempo when autoplay


def notepad_scale():
    global notepad
    notepad = [("Scale","1 3 5 6 8 10 12 13","Dur /Jońska - 1mod"),
("Scale","1 3 5 6 8 9 11 13","durowa miekka /hinduska"),
("Scale","1 3 4 6 8 10 11 13","Mol /Dorycka - 2 mod"),
("Scale","1 3 4 6 8 9 11 13      ","moll melodyczna down"),
("Scale","1 3 4 6 8 10 12 13      ","moll melodyczna up"),
("Scale","1 3 4 6 8 9 10 11 12 13    ","moll melodyczna up/down"),
("Scale","1 3 4 6 8 9 11 13","moll naturalna"),
("Scale","1 3 4 6 8 9 12 13","molowa harmoniczna"),
("Scale","1 2 5 6 8 9 11 13","5 mod mol harm"),
("Scale","1 3 5 7 8 10 11 13","lidian dominant /góralska"),
("Scale","1 2 4 6 7 9 11 13","lokrycka - 7 mod"),
("Scale","1 3 5 6 8 10 11 13","miksolidyjska - 5 mod"),
("Scale","1 2 4 6 8 9 11 13","Frygijska - 3 mod"),
("Scale","1 3 5 6 8 10 11 13","Lidyjska - 4 mod"),
("Scale","1 3 4 6 8 9 11 13","Eolska - 6 mod"),
("Scale","1 3 7 8 10 12 13       ","pentatoniczna półtonowa hemitoniczna"),
("Scale","1 3 5 8 10 13","pentatonika durowa /chinska-mongolska"),
("Scale","1 4 6 8 11 13","Pentatonika molowa"),
("Scale","1 2 6 8 9 13        ","pentatonika półtonowa diatoniczna"),
("Scale","1 4 6 7 8 11 12 13      ","bluesowa mol"),
("Scale","1 4 6 7 8 11 13","bluesowa"),
("Scale","1 2 4 5 7 9 11 13","alterowana"),
("Scale","1 3 5 7 9 11 13","całotonowa"),
("Scale","1 3 5 6 8 9 12 13","harmoniczna durowa"),
("Scale","1 2 4 5 7 8 10 11 13","pólton/cały ton."),
("Scale","1 4 7 10 13","zmniejszona"),
("Scale","1 3 4 5 8 9 10 13      ","bluesowa dur"),
("Scale","1 3 5 6 7 9 11 13      ","arabska"),
("Scale","1 3 5 8 10 13        ","chińska-mongolska /pentatonika durowa"),
("Scale","1 3 4 7 8 12 13       ","cygańska 1"),
("Scale","1 2 5 6 8 9 12 13      ","cygańska 2"),
("Scale","1 3 5 7 8 10 11 13      ","góralska /lidian dominant"),
("Scale","1 3 4 8 10 13        ","hawajska"),
("Scale","1 3 5 6 8 9 11 13      ","hinduska /durowa miekka"),
("Scale","1 2 5 6 8 9 11 13      ","hiszpańka"),
("Scale","1 2 6 8 9 13        ","japońska down"),
("Scale","1 2 6 8 11 13        ","japońska up"),
("Scale","1 2 6 8 9 11 13       ","japońska up/down"),
("Scale","1 2 4 6 8 10 11 13      ","jawajska"),
("Scale","1 2 4 6 8 9 12 13      ","neapolitańska"),
("Scale","1 2 5 6 7 9 12 13      ","perska"),
("Scale","1 4 5 7 8 10 11 13      ","węgierska"),
("Scale","1 3 4 7 8 10 13       ","wołowska"),
("Scale","1 3 5 6 8 9 10 12 13","bebop major"),
("Scale","1 3 5 6 8 10 11 12 13","bebop dominant"),
("Scale","1 3 4 5 6 8 10 11 13","bebop dorian"),
("Scale","1 3 4 6 8 9 10 12 13","bebop minor"),
("Scale","1 2 4 6 7 8 9 11 13","bebop locrian"),
("Chord","1 5 8           ","3 durowy X /Xmaj "),
("Chord","1 5 8 12         ","4 durowy Xmaj7 z septymą wielką"),
("Chord","1 5 8 12 15       ","5 durowy Xmaj9 z septymą wielką i noną"),
("Chord","1 5 8 10         ","4 durowy Xmaj6 z sekstą"),
("Chord","1 5 8 10 15       ","5 durowy Xmaj6/9 z sekstą i noną"),
("Chord","1 5 9 12         ","4 durowy Xmaj7/#5 z septymą wielkąi podwyższoną kwintą"),
("Chord","1 5 7 12         ","4 durowy Xmaj7/b5 z septymą wielkąi podwyższoną kwintą"),
("Chord","1 5 8 12 15 19     ","6 durowy Xmaj7/9/#11 z septymą wielką i noną"),
("Chord","1 5 8 11         ","4 dominanta X7 septymowa"),
("Chord","1 5 8 11 15       ","5 dominanta X9 nonowa /z noną wlk"),
("Chord","1 5 8 11 14       ","5 dominanta X7/b9 nonowa /z noną małą"),
("Chord","1 5 7 11         ","4 dominanta X7/b5 septymowa z obniżoną kwintą"),
("Chord","1 5 9           ","3 dominanta X/#5 trójdzwięk zwiększony"),
("Chord","1 5 9 11         ","4 dominanta X7/#5 septymowa z podwyższoną kwintą"),
("Chord","5 8 11           ","3 dominanta X/7-1 /lub Em/b5 trójdzwięk zmiejszony"),
("Chord","5 8 11 14         ","4 dominanta X/b9-1 /lub Eo akord zmniejszony"),
("Chord","1 5 8 11 15 18     ","6 dominanta X11 nonowa z unidecymą"),
("Chord","1 5 8 11 15 19     ","6 dominanta X9/#11 nonowa ze zwiększoną unidecymą"),
("Chord","1 5 8 11 15 18 22   ","7 dominanta X13 septymowa z tercdecymą"),
("Chord","1 5 8 11 14 18 22   ","7 dominanta X13/b9 septymowa z tercdecymą"),
("Chord","1 5 8 11 16 18 22   ","7 dominanta X13/#9 septymowa z tercdecymą"),
("Chord","1 4 8           ","3 molowy Xm "),
("Chord","1 4 8 12         ","4 molowy Xm/maj7 z septymą wielką"),
("Chord","1 4 8 11         ","4 molowy Xm7 z septymą małą"),
("Chord","1 4 8 10         ","4 molowy Xm6 z sekstą wielką"),
("Chord","1 4 8 11 15       ","5 molowy Xm9 z septymą i noną"),
("Chord","1 4 7 11         ","4 molowy Xm7/b5 molowu septymowy z obniżoną kwiną /akord półzmiejszony"),
("Chord","1 4 8 11 15 18     ","6 molowy Xm11 z sotymą i undecymą"),
("Chord","1 6 8 11         ","4 zawieszony X7sus4 /septymowy z kwartką zamiast tercji"),
("Chord","1 6 8 11 15       ","5 zawieszony X9sus4 /nonowy z kwartką zamiast tercji"),
("Chord","1 4 7 10         ","4 zmniejszony X7dim4"),
("Chord","1 4 7 11         ","4 półzmiejszony X7dim 2"),
]

# [xxx[1].split() for xxx in notepad if xxx[0]=="Scale"]
# [([int(aaa)-1 for aaa in xxx[1].split()],xxx[2]) for xxx in notepad if xxx[0]=="Scale" ]
# uuu=[iso.Scale([int(aaa)-1 for aaa in xxx[1].split()[:-1]],xxx[2]) for xxx in notepad if xxx[0]=="Scale" ]
# [scale.name for scale in iso.Scale.all()]


def read_config_file_scales():
    # print('reading config')
    config_file = 'reviewed_pattern_cfg.yaml'
    if IN_COLAB:
        config_file = '/content/SoundDesign/tracker/' + config_file

    with open(config_file, 'r') as file:
        # with open('reviewed_pattern_cfg.yaml', 'r') as file:
        loaded_yaml = yaml.safe_load(file)
    uuuu = [iso.Scale(scale['semitones'], scale['name']) for scale in loaded_yaml['scales']]

    # print(self.patterns_config)
    # print(self.patterns_config['play_over'])
    # self.patterns = list(map(lambda x: np.array(x['pattern']), self.patterns_config['play_over']['patterns']))
    # print('after list')

    # pprint.pprint(self.patterns_config)
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


def main():
    global my_tracker
    log_call()
    iso.util.midi_note_to_note_name=midi_note_to_note_name  # Overwritte original function
    intervals_chain = [1, 3,    -2, 1, 1, 7, -6, -4, -1] # fix in random_pattern zero interval
                       # [3, 0, -2, 1, 1, 7, -6, -4, -1, 1]
                #[1, 3,  0,-2, 1, 1, 7, -6, -4, -1]
    # self.midi_note_array2:     [61, 64, 64, 62, 63, 64, 71, 65, 61, 60]
    # self.midi_note_array2 cvt: [62, 64, 64, 62, 64, 64, 70, 65, 62, 60]

    notes_chain = [1, 4, 4, 2, 3, 4, 11, 5, 1, 0]
                #[63, 65, 65, 63, 63, 65, 70, 65, 63, 60]
    midi_notes_chain = list(np.array(notes_chain)+60)
    print(midi_notes_chain)

    print(sum(intervals_chain))
    flag_file = True
    flag_file = False

    # my_tracker = Tracker(interval_array=intervals_chain, flag_file=flag_file)
    my_tracker = Tracker(midi_note_array=midi_notes_chain, note_array=notes_chain, flag_file=flag_file)
    # patterns = Patterns()
    # my_tracker.metronome_start()
    read_config_file_scales()
    # notepad_scale()
    # uuu=[iso.Scale([int(aaa) - 1 for aaa in xxx[1].split()[:-1]], xxx[2]) for xxx in notepad if xxx[0] == "Scale"]



if __name__ == '__main__':
    main()
    print('Processing Done.')

# This is the way to initialize additional scales
# iso.Scale.xxx = iso.Scale([0,2,5,7],"xxx")
# [(scale.name, scale.octave_size) for scale in iso.Scale.all()]

# get(self, n):
# """ Retrieve the n'th degree of this scale. """
#indexOf(self, note):
#ts()""" Return the index of the given note within this scale. """

print("scale name", iso.Scale.default.name)

# check what is exact mapping between iso.Scale index, notes and midi notes.
# yaml.dump(xxx, default_flow_style=None)

# iso.util.midi_note_to_note_name(60)
# Out[18]: 'C4'
# iso.util.note_name_to_midi_note('C5')
# Out[19]: 60