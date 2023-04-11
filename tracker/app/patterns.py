import os
import numpy as np
import itertools
import random
import json
import isobar as iso

# import sys
import re
from functools import wraps



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



class NotePatterns:

    def __init__(self):
        self.__read_config_file__()
        self.pattern_size_for_interval = self.__init_pattern_size_for_interval__()

        self.pattern_methods_list = self.__list_get_pattern_methods__()
        self.pattern_methods_short_list  = [re.sub('get_(.*)_pattern', '\g<1>', method) for method in self.__list_get_pattern_methods__()]
        self.get_pattern = getattr(self, self.pattern_methods_list[0])
        self.dur_patterns = DurationPatterns()


    def __list_get_pattern_methods__(self):
        get_patt_search = re.compile('^get_.*_pattern$')
        return [x for x in dir(self) if get_patt_search.search(x)]

    @staticmethod
    def __init_pattern_size_for_interval__():
        max_range = 128

        tuple_range = itertools.product(range(1, max_range), range(1, max_range))
        filt_range = itertools.filterfalse(lambda xy: xy[0] * xy[1] >= max_range, tuple_range)
        pattern_size_for_interval = [{x} for x in range(max_range)]
        for x, y in filt_range:
            pattern_size_for_interval[x * y].add(x)
        return pattern_size_for_interval


    def __read_config_file__(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(this_dir, '../config/reviewed_pattern_cfg.json')

        # config_file = 'reviewed_pattern_cfg.json'


        with open(config_file, 'r') as file:

            self.patterns_config = json.load(file)

        self.patterns = list(map(lambda x: np.array(x['pattern']), self.patterns_config['play_over']['patterns']))


    @staticmethod
    def multiply_pattern(pattern, mult):
        pattern = np.array(pattern)
        if mult == 1:
            return pattern

        else:
            res_pattern = pattern
            add_pattern = np.array(pattern[1:])

        for a in range(mult - 1):
            add_pattern = add_pattern + pattern[-1]  # This is to add "step" of pattern, so I expect

            res_pattern = np.append(res_pattern, add_pattern)
        return res_pattern  # [:-1]

    def all_suitable_patterns(self, interval):
        sign = np.sign(interval)
        interval = abs(interval)
        if interval == 0:
            suitable_patterns = [pattern for pattern in
                             self.patterns if pattern[-1] in self.pattern_size_for_interval[interval]]
        else:
            suitable_patterns = [sign * self.multiply_pattern(pattern, int(interval / pattern[-1])) for pattern in
                             self.patterns if pattern[-1] in self.pattern_size_for_interval[interval]]
        # print('sp for n:',suitable_patterns)
        return suitable_patterns

# <editor-fold desc="get pattern functions">
    def mod_duration(func):  # added self, eventual issue
        @wraps(func)
        def split_no(interval, max_len = 16):
            if interval <= 16:
                return [interval]
            pattern_len = interval
            
            interval -= 1

            parts_no16 = interval // max_len
            parts_no16 += 1
            rnd_parts = random.choice([parts_no16, parts_no16 * 2, parts_no16 * 4])

            splt_array = []
            while pattern_len > 0:
                part = -(-pattern_len//rnd_parts)
                splt_array.append(part)
                pattern_len -= part
                rnd_parts -= 1


            return splt_array
        
        
        def inner(self, *args, **kwargs):
            parms = {"interval":0,
                     "dur_variety":999,
                     "quantize": {'5': 'normal', '3': 'normal', '2': 'normal'},
                     "align":1}
            for idx, arg in enumerate(args):
                parms[list(parms.keys())[idx]] = arg
            if kwargs is not None:
                parms.update(kwargs)

            result = func(self, **parms)

            print(f"{args=},{kwargs=}")
            print(f"-----////////////{parms['dur_variety']=}")


            print(f"xx {len(result[iso.EVENT_NOTE])=}, {result[iso.EVENT_NOTE]=}")
            if not np.any(result.get(iso.EVENT_DURATION)):
                pattern_len = len(result[iso.EVENT_NOTE])-1
                
                splt_array = split_no(pattern_len)
                durations = []
                for split_size in splt_array:
                    print("beff")
                    if split_size==1:
                        durations.extend(np.array([1]))
                        continue
                    if parms['quantize']['2']==parms['quantize']['3'] and parms['quantize']['3'] == parms['quantize']['5']:
                        condition = True
                    else:
                        condition = False
                    any_flag2 = parms['quantize']['2'] == 'down'
                    any_flag3 = parms['quantize']['3'] == 'down'
                    any_flag5 = parms['quantize']['5'] == 'down'
                    dur_part = [dp["pattern"] for dp in self.dur_patterns.patterns
                                    if dp["len"]==split_size
                                              and dp['pstdev']<=parms['dur_variety']
                                              and (dp.get('align'+str(parms['align'])) or parms['align'] == '1')
                                and (((dp.get('any2') or False) == any_flag2
                                      and (dp.get('any3') or False) == any_flag3
                                      and (dp.get('any5') or False) == any_flag5
                                      )
                                    or condition)
                                              # and (dp['align'+parms['align']] or parms['align'] == 1)
                                              ]
                    print(f"1. {dur_part=}, {split_size=}")
                    if dur_part == []:
                        sdp = self.dur_patterns.patterns
                        dur_part = [dp for dp in sdp if dp["len"] == split_size]
                        min_sdp = min(map(lambda x: x['pstdev'],dur_part))
                        dur_part = [dp['pattern'] for dp in dur_part if dp["pstdev"] == min_sdp]


                        print(f"2. {dur_part=}")

                    dur_part = random.choice(dur_part)
                    print(f"3. {dur_part=}")

                    dur_part2 = np.array(dur_part)
                    durations.extend(dur_part2)

                print(f"=========>{durations=}")
                result[iso.EVENT_DURATION] = 1/np.array(durations)

            return result
        return inner



    @mod_duration
    def get_simple_pattern(self, *args, **kwargs):  # interval sould be not needed
        return {
            iso.EVENT_NOTE: np.append(random.choice([1,-1])*random.choice(self.patterns), 0)
        }

    @mod_duration
    # def get_random_path_pattern(self, *args, **kwargs):
    def get_random_path_pattern(self, **kwargs):
        interval = 0
        # if args[0]:
        #     interval = args[0]
        # elif kwargs.get('interval'):
        #     interval = kwargs.get('interval')
        if kwargs.get('interval'):
            interval = kwargs.get('interval')
        # return random.choice(self.all_suitable_patterns(interval))
        # return {iso.EVENT_NOTE:random.choice(self.all_suitable_patterns(interval))}
        org_interval=interval
        # this secion is when we want to optimize/shorten patterns
        interval_sign = 1 if interval>=0 else -1
        octave = abs(interval) // 12
        octave *= interval_sign 
        interval = abs(interval) % 12
        interval *= interval_sign
        notes_pattern = np.array(random.choice([pattern for pattern in self.all_suitable_patterns(org_interval)]))
        return {
            iso.EVENT_NOTE:notes_pattern,
        }

    @mod_duration
    def get_chord_maj_pattern(self, *args, **kwargs): # interval sould be not needed
        return {
            iso.EVENT_NOTE:  np.array([(0, 2, 4), 0],dtype=object)
        }

    @mod_duration
    # def get_one_note_pattern(self, *args, **kwargs):
    def get_one_note_pattern(self, **kwargs):
        interval = 0
        # if args[0]:
        #     interval = args[0]
        # elif kwargs.get('interval'):
        #     interval = kwargs.get('interval')
        if kwargs.get('interval'):
            interval = kwargs.get('interval')
        return {iso.EVENT_NOTE: np.array([0, interval])
                }

    @mod_duration
    # def get_rest_path_pattern(self, *args, **kwargs):
    def get_rest_path_pattern(self, **kwargs):
        interval = 0
        # if args[0]:
        #     interval = args[0]
        # elif kwargs.get('interval'):
        #     interval = kwargs.get('interval')
        if kwargs.get('interval'):
            interval = kwargs.get('interval')
        # if interval == 0:
        if not interval:
            notes = np.array([0,0])
        else:
            real_notes = np.arange(0, interval , np.sign(interval))
            rests = np.repeat(None, abs(interval ))
            notes_with_rests = zip(real_notes, rests)
            notes = np.array([ nt for tp in notes_with_rests for nt in tp] + [None])

        return {
            iso.EVENT_NOTE:notes
        }

    @mod_duration
    def get_path_pattern(self, **kwargs):
        interval = 0
        if kwargs.get('interval'):
            interval = kwargs.get('interval')

        # if interval == 0:
        if not interval:
            notes = np.array([0,0])
        else:
            notes = np.arange(0, interval + np.sign(interval), np.sign(interval))
        return {
            iso.EVENT_NOTE:notes
        }
    # </editor-fold>

    def set_pattern_function(self, function_name ):
        self.get_pattern = getattr(self, 'get_'+function_name+'_pattern' )




def main():
    global note_ptrn
    note_ptrn = NotePatterns()
    find_scale([0, 2, 3, 5, 7, 8, 11])


def find_scale(semitones:list):
    for scale in note_ptrn.patterns_config['scales']:

        if set(scale['semitones']) ==set(semitones):
            print(scale)

if __name__ == '__main__':
    main()

