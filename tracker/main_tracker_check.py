# import tracker as tck
import tracker
import inspect

global my_tracker


def log_call():
    print(inspect.stack()[1][3])


def ts():
    my_tracker.ts()


def main():
    global my_tracker
    log_call()
    my_tracker = tracker.Tracker()
    print(my_tracker)
    my_tracker.init_timeline()
    # tracker.beat = tracker.beat_none
    my_tracker.beat = my_tracker.beat1
    my_tracker.metronome_start()
    tmln = my_tracker.tracker_timeline()
    # pprint.pprint(tmln.__dict__)


if __name__ == '__main__':
    main()
    print('Processing Done.')