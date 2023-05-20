from .tracker import Tracker
from .trackergui import *
from .log_call import *

import os
import json


# <editor-fold desc="Interactive simplification functions">
# def tracker_dec(func):
#     def inner():
#         # global self.yy_tracker
#         # print(func.__name__)
#         new_func = getattr(self.tracker_ref, func.__name__)
#         # print('new func: ',new_func)
#         new_func()
#
#     return inner


# @tracker_dec
# def tstop():
#     pass

#
# @tracker_dec
# def ts():
#     pass


# @tracker_dec
# def tstart():
#     pass

#
# def mstart():
#     my_tracker.metronome_start()
#
#
# def mstop():
#     my_tracker.metronome_stop()
#
#
# def sbt1():
#     my_tracker.beat = my_tracker.beat1
#
#
# def sbt2():
#     my_tracker.beat = my_tracker.beat2
#
#
# def sbtn():
#     my_tracker.beat = my_tracker.beat_none
#
#
# def sbtt():
#     my_tracker.beat = my_tracker.beat_test




#
# def sbft(note_from=60, note_to=64):
#     my_tracker.beat = lambda: my_tracker.play_from_to(note_from, note_to)


# </editor-fold>

# <editor-fold desc="wrk functions">






#TODO To move to utils

# def cmp():
#     # print('expected:\n', my_tracker.expected_array)
#     print('expected:\n', [y for x in my_tracker.pattern_array for y in list(x['note'])])
#     print('played:\n', [x.note for x in my_tracker.midi_out.miditrack if x.type == 'note_on'])


#TODO To move to utils

# def find_scale_dups():
#     import itertools
#
#     cmp_scales = [(prd[0][1].name, set(prd[0][1].semitones), prd[1][1].name, set(prd[1][1].semitones)) for prd in
#                   itertools.product(enumerate(iso.Scale.all()), enumerate(iso.Scale.all()))
#                   if prd[0][0] > prd[1][0] and set(prd[0][1].semitones) == set(prd[1][1].semitones)]
#     for cscale in cmp_scales:
#         print(cscale)


#TODO To move to utils

# def dump_scales():
#     all_scales = [(scale.semitones, scale.name) for scale in iso.Scale.all()]
#     all_scales_sorted = sorted(all_scales, key=lambda i: i[0])
#     print(*all_scales_sorted, sep='\n')


# </editor-fold>


def main():
    # global self.yy_tracker
    # global keyboard
    log_call()
    this_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(this_dir, '../config/main_config.json')



    # wanted_file = os.path.join(this_dir, fname)

    with open(config_file, 'r') as file:
        loaded_config = json.load(file)
        app_config = loaded_config['app']
        tracker_config = loaded_config['tracker']
        midi_mapping = loaded_config.get('midi_mapping')

    # midi_out_flag = Tracker.MIDI_OUT_DEVICE
    midi_out_flag = Tracker.MIDI_OUT_MIX_FILE_DEVICE
    # midi_out_flag = Tracker.MIDI_OUT_FILE

    tracker = Tracker(tracker_config=tracker_config, midi_mapping=midi_mapping, midi_out_mode=midi_out_flag)
    # my_tracker.midi_out.program_change(program=22)

    TrackerGuiApp(parm_rows=12, parm_cols=5, app_config=app_config, tracker_ref=tracker).run()


if __name__ == '__main__':
    main()
    print('Processing Done.')

