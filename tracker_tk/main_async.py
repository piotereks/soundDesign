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

# These are work in progress debug functions
def find_scale_dups():
    import itertools
    # cmp_scales = [(set(prd[0][1].semitones), set(prd[1][1].semitones)) for prd in itertools.product(enumerate(iso.Scale.all()), enumerate(iso.Scale.all()))
    #               if prd[0][0] > prd[1][0]]
    cmp_scales = [(prd[0][1].name, set(prd[0][1].semitones), prd[1][1].name, set(prd[1][1].semitones)) for prd in itertools.product(enumerate(iso.Scale.all()), enumerate(iso.Scale.all()))
                  if prd[0][0] > prd[1][0] and set(prd[0][1].semitones) == set(prd[1][1].semitones)]
    for cscale in cmp_scales:
        print(cscale)

    # for i, scale in enumerate(iso.Scale.all()):
    #     print(i,scale)
    # p.itertools.product(iso.scales.all())
    # [(x.name, x.semitones) for x in iso.Scale.all()]

def dump_scales():
    all_scales=[(scale.semitones, scale.name ) for scale in iso.Scale.all()]
    all_scales_sorted =sorted(all_scales, key=lambda i: i[0])
    print(*all_scales_sorted, sep='\n')

# nice scales https://jguitar.com/scale/E/Ionian
# nice scales https://jguitar.com/scale/E/Ionian

def main():
    global my_tracker
    log_call()
    # iso.util.midi_note_to_note_name=midi_note_to_note_name  # Overwritte original function
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
    my_tracker = Tracker(midi_note_array=midi_notes_chain, note_array=notes_chain, midi_out_mode=flag_file)
    # patterns = Patterns()
    # my_tracker.metronome_start()

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
