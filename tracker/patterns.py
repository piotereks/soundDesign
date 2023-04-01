import numpy as np
import itertools
import random
import json
import isobar as iso

import sys
import re
from functools import wraps


global IN_COLAB
IN_COLAB = 'google.colab' in sys.modules

class DurationPatterns:
    def __init__(self):
        self.__read_config_file__()

    def __read_config_file__(self):
        # print('reading config')
        config_file = 'duration_patterns.json'
        if IN_COLAB:
            config_file = '/content/SoundDesign/tracker/' + config_file

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

        config_file = 'reviewed_pattern_cfg.json'
        if IN_COLAB:
            config_file = '/content/SoundDesign/tracker/' + config_file

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
    def mod_duration(func):  #added self, eventual issue
        @wraps(func)
        def split_no(interval, max_len = 16):
            if interval<=16:
                return [interval]
            pattern_len=interval
            
            interval -=1

            parts_no16 = interval // max_len
            parts_no16 += 1
            rnd_parts = random.choice([parts_no16, parts_no16 * 2, parts_no16 * 4])

            splt_array=[]
            while pattern_len>0:
                part = -(-pattern_len//rnd_parts)
                splt_array.append(part)
                pattern_len -= part
                rnd_parts -= 1


            return splt_array
        
        
        def inner(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            variety = 999
            if args[1] is not None:
                variety = args[1]
            elif kwargs.get('variety'):
                variety = kwargs.get('variety')
            print(f"{args=},{kwargs=}")
            print(f"-----////////////{variety=}")

            print(f"xx {len(result[iso.EVENT_NOTE])=}, {result[iso.EVENT_NOTE]=}")
            if not np.any(result.get(iso.EVENT_DURATION)):
                pattern_len = len(result[iso.EVENT_NOTE])-1
                
                splt_array = split_no(pattern_len)
                durations = []
                for split_size in splt_array:
                    dur_part = random.choice([dp["pattern"] for dp in self.dur_patterns.patterns
                                    if dp["len"]==split_size and dp['pstdev']<=variety] )
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
    def get_random_path_pattern(self, *args, **kwargs):
        interval = 0
        if args[0]:
            interval = args[0]
        elif kwargs.get('interval'):
            interval = kwargs.get('interval')
        # return random.choice(self.all_suitable_patterns(interval))
        # return {iso.EVENT_NOTE:random.choice(self.all_suitable_patterns(interval))}
        org_interval=interval
        # this secion is when we want to optimize/shorten patterns
        interval_sign = 1 if interval>=0 else -1
        octave = abs(interval) // 12
        octave *= interval_sign 
        interval = abs(interval) % 12
        interval *=interval_sign
        #
        
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
    def get_one_note_pattern(self, *args, **kwargs):
        interval = 0
        if args[0]:
            interval = args[0]
        elif kwargs.get('interval'):
            interval = kwargs.get('interval')
        return {iso.EVENT_NOTE: np.array([0, interval])
                }

    @mod_duration
    def get_rest_path_pattern(self, *args, **kwargs):
        interval = 0
        if args[0]:
            interval = args[0]
        elif kwargs.get('interval'):
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
    # def get_path_pattern(self, interval):
    def get_path_pattern(self, *args, **kwargs):
        interval = 0
        if args[0]:
            interval = args[0]
        elif kwargs.get('interval'):
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
    import pprint

    global note_ptrn
    note_ptrn = NotePatterns()
    find_scale([0, 2, 3, 5, 7, 8, 11])


def find_scale(semitones:list):
    for scale in note_ptrn.patterns_config['scales']:

        if set(scale['semitones']) ==set(semitones):
            print(scale)

if __name__ == '__main__':
    main()


# patterns_config