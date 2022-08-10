from tracker import *
from patterns import *

def ts():
    global my_tracker
    my_tracker.ts()


def sbt1():
    my_tracker.beat = my_tracker.beat1


def sbt2():
    my_tracker.beat = my_tracker.beat2


def sbtn():
    my_tracker.beat = my_tracker.beat_none


def sbtp():
    my_tracker.beat = my_tracker.pplay


def save_midi():
    my_tracker.midi_out.write()


def cmp():
    # print('expected:\n', my_tracker.expected_array)
    print('expected:\n', [y for x in my_tracker.pattern_array for y in list(x['note'])])
    print('played:\n', [x.note for x in my_tracker.midi_out.miditrack if x.type == 'note_on'])

# speeding up and slowing down tempo when autoplay
def main():
    global my_tracker
    log_call()
    intervals_chain = [1, 3,    -2, 1, 1, 7, -6, -4, -1] # fix in random_pattern zero interval
                       # [3, 0, -2, 1, 1, 7, -6, -4, -1, 1]
    notes_chain = [1, 4, 4, 2, 3, 4, 11, 5, 1, 0]
    print(sum(intervals_chain))
    flag_file = True
    flag_file = False

    # my_tracker = Tracker(interval_array=intervals_chain, flag_file=flag_file)
    my_tracker = Tracker(note_array=notes_chain, flag_file=flag_file)
    # patterns = Patterns()
    # my_tracker.metronome_start()


#     global my_tracker
#     log_call()
#     my_tracker = Tracker()
#     print(my_tracker)
#     # my_tracker.init_timeline()
#     # tracker.beat = tracker.beat_none
#     # my_tracker.beat = my_tracker.beat1
#     # my_tracker.metronome_start()
#     # tmln = tracker.tracker_timeline()
#     # pprint.pprint(tmln.__dict__)


if __name__ == '__main__':
    main()
    print('Processing Done.')

