import os
import numpy as np
import math
import itertools
import random
import json
import isobar as iso
import re
from functools import wraps

from fractions import *


class DurationPatterns:
    def __init__(self):
        self.__read_config_file__()

    def __read_config_file__(self):
        # print('reading config')
        this_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(this_dir, '../config/duration_patterns.json')

        with open(config_file, 'r') as file:
            self.patterns = json.load(file)

        print('after list')


def mod_duration(func):  # added self, eventual issue
    @wraps(func)
    def split_no(interval, max_len=16, dot_beat=False, numerator=4):
        # (5, 7, 10, 11)  5 2. 2; 7 2. 2 2, 10 2.2. 2 2, 11 2. 2. 2. 2
        if dot_beat and numerator in (5, 10):
            tmp_split_array = [('dot', interval - interval // 2), ('norm', interval // 2)]
        elif dot_beat and numerator == 7:
            tmp_split_array = [('dot', interval - interval * 2 // 3), ('norm', interval * 2 // 3)]
        elif dot_beat and numerator == 11:
            tmp_split_array = [('dot', interval - interval // 4), ('norm', interval // 4)]
        else:
            tmp_split_array = [('norm', interval)]

        split_array = []
        for split in tmp_split_array:
            if split[1] <= 16:
                split_array.append(split)
            else:
                pattern_len = split[1]
                interval -= 1
                parts_no16 = pattern_len // max_len
                parts_no16 += 1
                rnd_parts = random.choice([parts_no16, parts_no16 * 2, parts_no16 * 4])
                while pattern_len > 0:
                    part = -(-pattern_len // rnd_parts)
                    split_array.append((split[0], part))
                    pattern_len -= part
                    rnd_parts -= 1
        return split_array

    def inner(self, *args, **kwargs):
        parameters = {"interval": 0,
                      "dur_variety": 999,
                      "quantize": {'5': 'normal', '3': 'normal', '2': 'normal'},
                      "align": 1,
                      "dot_beat": False,
                      "numerator": 4}
        for idx, arg in enumerate(args):
            parameters[list(parameters.keys())[idx]] = arg
        if kwargs is not None:
            parameters.update(kwargs)

        result = func(self, **parameters)

        print(f"{args=},{kwargs=}")
        print(f"-----////////////{parameters['dur_variety']=}")

        print(f"xx {len(result[iso.EVENT_NOTE])=}, {result[iso.EVENT_NOTE]=}")
        dur_list = result.get(iso.EVENT_DURATION)
        if dur_list is None or dur_list == []:
            pattern_len = len(result[iso.EVENT_NOTE]) - 1

            split_array = split_no(pattern_len, dot_beat=parameters['dot_beat'], numerator=parameters['numerator'])
            print(f"{pattern_len=},{split_array=}")
            durations = []
            for norm_dot, split_size in split_array:
                if split_size == 0:
                    continue
                if split_size == 1:
                    if norm_dot == 'norm':
                        # durations.extend(np.array([1]))
                        durations.extend([1])
                    else:
                        durations.extend([1.5])
                        # durations.extend(np.array([1.5]))
                    continue
                if parameters['quantize']['2'] == parameters['quantize']['3'] and parameters['quantize']['3'] == \
                        parameters['quantize'][
                            '5']:
                    condition = True
                else:
                    condition = False
                any_flag2 = parameters['quantize']['2'] == 'down'
                any_flag3 = parameters['quantize']['3'] == 'down'
                any_flag5 = parameters['quantize']['5'] == 'down'

                dur_part = [dp["pattern"] for dp in self.dur_patterns.patterns
                            if dp.get(norm_dot)
                            and dp["len"] == split_size
                            and dp['pstdev'] <= parameters['dur_variety']
                            and (dp.get('align' + str(parameters['align'])) or parameters['align'] == '1')
                            and (((dp.get('any2') or False) == any_flag2
                                  and (dp.get('any3') or False) == any_flag3
                                  and (dp.get('any5') or False) == any_flag5
                                  )
                                 or condition)
                            ]
                print(f"1. {dur_part=}, {split_size=}")
                if not dur_part:  # f dur_part == []:
                    sdp = self.dur_patterns.patterns
                    dur_part = [dp for dp in sdp if dp["len"] == split_size]
                    min_sdp = min(map(lambda x: x['pstdev'], dur_part))
                    dur_part = [dp['pattern'] for dp in dur_part if dp["pstdev"] == min_sdp]

                    print(f"2. {dur_part=}")

                if norm_dot == "norm":
                    dur_part = random.choice(dur_part)
                else:
                    dur_part = list(map(lambda x: Fraction(x / 1.5).limit_denominator(1000), random.choice(dur_part)))

                print(f"3. {dur_part=}")

                durations.extend(dur_part)

            print(f"=========>{durations=}")
            result[iso.EVENT_DURATION] = [Fraction(1 / x).limit_denominator(1000) for x in durations]

        return result

    return inner


class NotePatterns:

    def __init__(self):
        self.patterns = {}
        self.__read_config_file__()
        self.pattern_size_for_interval = self.__init_pattern_size_for_interval__()

        self.pattern_methods_list = self.__list_get_pattern_methods__()
        self.pattern_methods_short_list = [re.sub('get_(.*)_pattern', '\\g<1>', method) for method in
                                           self.__list_get_pattern_methods__()]
        self.get_pattern = getattr(self, self.pattern_methods_list[0])
        self.dur_patterns = DurationPatterns()
        self.key = iso.Key()
        self.prev_chord = set()

    def __list_get_pattern_methods__(self):
        get_patt_search = re.compile('^get_.*_pattern$')
        return [x for x in dir(self) if get_patt_search.search(x)]

    @staticmethod
    def __init_pattern_size_for_interval__():
        max_range = 128
        tuple_range = itertools.product(range(1, max_range), range(1, max_range))
        filter_range = itertools.filterfalse(lambda xy: xy[0] * xy[1] >= max_range, tuple_range)
        pattern_size_for_interval = [{x} for x in range(max_range)]
        for x, y in filter_range:
            pattern_size_for_interval[x * y].add(x)
        return pattern_size_for_interval

    def __read_config_file__(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(this_dir, '../config/note_patterns.json')

        with open(config_file, 'r') as file:
            self.patterns_config = json.load(file)

        self.patterns['play_over'] = list(map(lambda x: x['pattern'], self.patterns_config['play_over']['patterns']))
        self.patterns['ornament'] = list(map(lambda x: x['pattern'], self.patterns_config['ornament']['patterns']))
        self.patterns['diminution'] = list(
            map(lambda x: x['pattern'], self.patterns_config['diminution']['patterns']))

    @staticmethod
    def multiply_pattern(pattern: list, mult):
        # pattern = np.array(pattern)
        # add_pattern = []
        # res_pattern = []

        mult = abs(mult)
        if mult == 1:
            return pattern

        else:
            res_pattern = pattern
            add_pattern = pattern[1:]
            shift = pattern[-1]
        for a in range(mult - 1):
            add_pattern = list(map(lambda x: x + shift, add_pattern))
            res_pattern.extend(add_pattern)
        return res_pattern  # [:-1]

    def all_suitable_patterns(self, interval):
        sign = int(np.sign(interval))
        interval = abs(interval)

        if interval == 0:
            suitable_patterns = [pattern for pattern in
                                 self.patterns['play_over'] if pattern[-1] in self.pattern_size_for_interval[interval]]
        else:
            # cntr = 0
            suitable_patterns = [list(map(lambda x: x * sign * int(np.sign(pattern[-1])),
                                          self.multiply_pattern(pattern[:], int(interval / pattern[-1]))))
                                 for pattern in self.patterns['play_over']
                                 if abs(pattern[-1]) in self.pattern_size_for_interval[interval]]

        return suitable_patterns

    def all_suitable_diminutions(self, interval):
        sign = int(np.sign(interval))
        interval = abs(interval)

        if interval == 0:
            suitable_patterns = [pattern for pattern in
                                 self.patterns['diminution'] if
                                 pattern[-1] in self.pattern_size_for_interval[interval]]
        else:
            # cntr = 0
            suitable_patterns = [list(map(lambda x: x * sign * int(np.sign(pattern[-1])),
                                          pattern[:]))
                                 for pattern in self.patterns['diminution']
                                 if abs(pattern[-1]) == interval]
            if not suitable_patterns:
                suitable_patterns = [range(0, sign * interval + sign, sign)]

        return suitable_patterns

    # <editor-fold desc="get pattern functions">

    @mod_duration
    def get_simple_pattern(self, **kwargs):  # interval should be not needed
        return {
            iso.EVENT_NOTE: list(
                map(lambda x: x * random.choice([1, -1]), random.choice(self.patterns['play_over']))) + [0]
        }

    @mod_duration
    def get_random_path_pattern(self, **kwargs):
        interval = 0
        if kwargs.get('interval'):
            interval = kwargs.get('interval')
        org_interval = interval
        interval_sign = 1 if interval >= 0 else -1
        octave = abs(interval) // 12
        octave *= interval_sign
        interval = abs(interval) % 12
        interval *= interval_sign
        print(f"{org_interval=}, {octave=}, {interval=}")
        notes_pattern = random.choice([pattern for pattern in self.all_suitable_patterns(org_interval)])
        # notes_pattern = random.choice(deb)
        return {
            iso.EVENT_NOTE: notes_pattern,
        }

    @mod_duration
    def get_random_dim_pattern(self, **kwargs):
        interval = 0
        if kwargs.get('interval'):
            interval = kwargs.get('interval')
        org_interval = interval
        interval_sign = 1 if interval >= 0 else -1
        octave = abs(interval) // 12
        octave *= interval_sign
        interval = abs(interval) % 12
        interval *= interval_sign
        print(f"{org_interval=}, {octave=}, {interval=}")
        notes_pattern = random.choice([pattern for pattern in self.all_suitable_diminutions(org_interval)])
        # notes_pattern = random.choice(deb)
        return {
            iso.EVENT_NOTE: notes_pattern,
        }

    @mod_duration
    def get_chord_maj_pattern(self, **kwargs):
        return {
            iso.EVENT_NOTE: [(0, 2, 4), 0]
        }

    @mod_duration
    def get_chord_improved_pattern(self, **kwargs):
        parameters = {"interval": 0,
                      "dur_variety": 999,
                      "quantize": {'5': 'normal', '3': 'normal', '2': 'normal'},
                      "align": 1,
                      "dot_beat": False,
                      "numerator": 4,
                      "from_note": 60,
                      "key": iso.Key()}

        def invert_chord(chord_to_inv: list) -> list:
            # chord_to_inv[0] += major.octave_size
            # chord_to_inv.sort()
            # return [x - chord_to_inv[0] + from_note for x in chord_to_inv]
            chord_to_inv[-1] -= major.octave_size
            chord_to_inv.sort()
            return chord_to_inv

        if kwargs is not None:
            parameters.update(kwargs)

        from_note = parameters.get('from_note', 60)
        key = parameters.get('key', None)
        from_note = key.nearest_note(from_note)  # This is taken from used scale/key not major

        major = iso.Scale.major
        key_major = iso.Key(tonic=key.tonic, scale=major)
        maj_semitones = NotePatterns.multiply_pattern(major.semitones + [major.octave_size], 2)

        chord_n = 3
        semitone_step = 2
        chords_list = []

        # chord_3n = 3
        # chord_4n = 4

        for i in range(len(maj_semitones) // 2):
            for chord_st in (3, 4):
                chord = [maj_semitones[i + x * semitone_step] - maj_semitones[i] + from_note for x in range(chord_st)]
                chord_set = set(chord)
                if chord_set not in chords_list:
                    chords_list.append(chord_set)
                    for _ in range(chord_st-1):
                        chord_set = set(invert_chord(chord))
                        if chord_set not in chords_list:
                            chords_list.append(chord_set)
        # thirds and fifths
        thirds_fifths = [{0, 4}, {0, 3}, {0, 5}, {0, 6}, {0, 7}, {0, 8}, {0, 9}]
        chords_list.extend([{list(x)[0] + from_note, list(x)[1] + from_note} for x in thirds_fifths])

        # chords_list_down = chords_list.copy()
        # for s in chords_list_down:  # Iterate through each set
        #     for i, elem in enumerate(s):  # Iterate through each element in the set
        #         s.remove(elem)  # Remove the element from the set
        #         s.add(elem - major.octave_size)  # Add the incremented element back to the set

        chords_list_down, chords_list_up = [], []

        for s in chords_list:
            incremented_set_down = set()
            incremented_set_up = set()
            for elem in s:
                incremented_set_down.add(elem - major.octave_size)
                incremented_set_up.add(elem + major.octave_size)
            chords_list_down.append(incremented_set_down)
            chords_list_up.append(incremented_set_up)
        chords_list.extend(chords_list_down)
        chords_list.extend(chords_list_up)

        chords_list = [s for s in chords_list if from_note in s]
        # scale = key.scale

        from_note_idx = key.scale.indexOf(from_note - key.tonic)
        three_octaves = set(
            [key.get(note_idx) for note_idx in range(from_note_idx -1 -len(key.scale.semitones), from_note_idx + len(key.scale.semitones) * 2 + 1)])
        chord_found = [ch & three_octaves for ch in chords_list if ch & three_octaves == ch]

        if chord_found:
            # check how many notes are shared with prev_chord
            max_match = max([len(x & self.prev_chord) for x in chord_found])
            chord_found = [x for x in chord_found if len(x & self.prev_chord) == max_match]

            """ 
            Check proximity of notes by calculating sum of difference between each pair of notes (product of elements).
            """
            max_len = max([len(x) for x in chord_found])
            chord_found = [x for x in chord_found if len(x) == max_len]

            min_delta = min([sum(abs(p[0] - p[1]) for p in itertools.product(x, self.prev_chord))/len(x) for x in chord_found])
            chord_found = [x for x in chord_found if
                           sum(abs(p[0] - p[1]) for p in itertools.product(x, self.prev_chord))/len(x) == min_delta]

            chord = list(random.choice(chord_found))
            chord.sort()
            chord = tuple(chord)
            self.prev_chord = set(chord)
            chord_idx = tuple(key.scale.indexOf(key.nearest_note(x) - key.tonic) - from_note_idx for x in chord)
        else:
            chord_idx = 0
            self.prev_chord = set()

        return {
            iso.EVENT_NOTE: [chord_idx, 0]
        }

    @mod_duration
    def get_one_note_pattern(self, **kwargs):
        interval = 0
        if kwargs.get('interval'):
            interval = kwargs.get('interval')
        return {
            iso.EVENT_NOTE: [0, interval]
        }

    @mod_duration
    def get_rest_path_pattern(self, **kwargs):
        interval = 0
        if kwargs.get('interval'):
            interval = kwargs.get('interval')
        # if interval == 0:
        if not interval:
            notes = [0, 0]
        else:
            real_notes = range(0, interval, int(np.sign(interval)))
            rests = [None] * abs(interval)
            notes_with_rests = zip(real_notes, rests)
            notes = [nt for tp in notes_with_rests for nt in tp] + [None]

        return {
            iso.EVENT_NOTE: notes
        }

    @mod_duration
    def get_path_pattern(self, **kwargs):
        interval = 0
        if kwargs.get('interval'):
            interval = kwargs.get('interval')

        if not interval:
            notes = [0, 0]
        else:
            notes = range(0, interval + int(np.sign(interval)), int(np.sign(interval)))
        return {
            iso.EVENT_NOTE: notes
        }

    @mod_duration
    def get_sine_pattern(self, **kwargs):
        parameters = {"interval": 0,
                      "dur_variety": 999,
                      "quantize": {'5': 'normal', '3': 'normal', '2': 'normal'},
                      "align": 1,
                      "dot_beat": False,
                      "numerator": 4,
                      "key": iso.Key()}

        if kwargs is not None:
            parameters.update(kwargs)

        interval = parameters.get('interval', 0)
        scale_interval = parameters.get('scale_interval', 0)
        key = parameters.get('key', None)
        # root_note = parameters.get('root_note', None)
        # org_interval = interval
        # interval_sign = 1 if interval >= 0 else -1
        r = 32
        if interval == 0:
            notes = [(-5 * len(key.scale.semitones)
                      + key.scale.indexOf(5 * key.scale.octave_size + key.nearest_note(
                        7 * math.sin(4 * math.pi / 2 * x / r) + key.tonic) - key.tonic))
                     for x in range(r + 1)]
        else:
            if key is not None:
                notes = [(-5 * len(key.scale.semitones)
                          + key.scale.indexOf(5 * key.scale.octave_size + key.nearest_note(
                            scale_interval * x / r
                            + (abs(scale_interval * 0.66) + scale_interval * 0.33) * math.sin(
                                4 * math.pi / 2 * x / r) + key.tonic) - key.tonic))
                         for x in range(r + 1)]

            else:
                notes = [
                    round(scale_interval * math.sin(5 * math.pi / 2 * x / r))
                    for x in range(r + 1)]

        return {
            iso.EVENT_NOTE: notes,
            iso.EVENT_DURATION: [1] * len(notes)
        }

    @mod_duration
    def get_sine_var_len_pattern(self, **kwargs):
        parameters = {"interval": 0,
                      "dur_variety": 999,
                      "quantize": {'5': 'normal', '3': 'normal', '2': 'normal'},
                      "align": 1,
                      "dot_beat": False,
                      "numerator": 4,
                      "key": iso.Key()}

        if kwargs is not None:
            parameters.update(kwargs)

        interval = parameters.get('interval', 0)
        scale_interval = parameters.get('scale_interval', 0)
        key = parameters.get('key', None)
        # org_interval = interval
        # interval_sign = 1 if interval >= 0 else -1
        r = 32
        if interval == 0:
            notes = [int(5 * math.sin(2 * math.pi * x / r)) for x in range(r + 1)]
        else:
            # notes = [round(interval*math.sin(5*math.pi/2*x/r)) for x in range(r+1)]
            if key is not None:
                notes = [-5 * len(key.scale.semitones)
                         + key.scale.indexOf((5 * key.scale.octave_size + round(
                    scale_interval * math.sin(5 * math.pi / 2 * x / r))) - key.tonic % 12)
                         for x in range(r + 1)]
            else:
                notes = [
                    round(scale_interval * math.sin(5 * math.pi / 2 * x / r))
                    for x in range(r + 1)]

        result_dict = {
            iso.EVENT_NOTE: notes,
            iso.EVENT_DURATION: [1] * len(notes)
        }

        notes_wrk = []
        dur_wrk = []
        # result_dict = {}
        for idx in range(len(notes)):
            if idx == 0 or notes[idx] != notes[idx - 1]:
                notes_wrk.append(result_dict[iso.EVENT_NOTE][idx])
                dur_wrk.append(result_dict[iso.EVENT_DURATION][idx])
            else:
                dur_wrk[-1] += 1

        result_dict[iso.EVENT_NOTE] = notes_wrk
        result_dict[iso.EVENT_DURATION] = dur_wrk

        return result_dict

    # </editor-fold>

    def set_pattern_function(self, function_name):
        self.get_pattern = getattr(self, 'get_' + function_name + '_pattern')


def main():
    pass


if __name__ == '__main__':
    main()
