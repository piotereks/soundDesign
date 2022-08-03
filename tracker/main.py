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
    # intervals_chain = [1, 3, -2, 1, 1, 10, -9, -4,-1] # fix in random_pattern zero interval
    intervals_chain = [1, 3, -2, 1, 1, 7, -6, -4,-1] # fix in random_pattern zero interval
    print(sum(intervals_chain))
    my_tracker = Tracker(interval_array=intervals_chain, flag_file=False)

    # print(my_tracker)
    # my_tracker.init_timeline()
    # tracker.beat = tracker.beat_none
    # my_tracker.beat = my_tracker.beat1
    # my_tracker.metronome_start()
    # tmln = tracker.tracker_timeline()
    # pprint.pprint(tmln.__dict__)

    patterns = Patterns()

    # for interval  in intervals_chain:
    #     print('gsp:', interval, patterns.get_random_pattern(interval))


if __name__ == '__main__':
    main()
    print('Processing Done.')

