import numpy as np
import itertools
import random
# import yaml
import json
import isobar as iso
import pprint

import sys
import re
from functools import wraps
from typing import Callable

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
            # with open('reviewed_pattern_cfg.yaml', 'r') as file:
            self.patterns = json.load(file)
        # print(self.patterns_config)
        # print(self.patterns_config['play_over'])
        print('after list')

        # pprint.pprint(self.patterns)

class NotePatterns:

    def __init__(self):
        self.__read_config_file__()
        self.pattern_size_for_interval = self.__init_pattern_size_for_interval__()
        # self.get_pattern = self.get_path_pattern
        self.pattern_methods_list = self.__list_get_pattern_methods__()
        self.pattern_methods_short_list  = [re.sub('get_(.*)_pattern', '\g<1>', method) for method in self.__list_get_pattern_methods__()]
        self.get_pattern = getattr(self, self.pattern_methods_list[0])
        self.dur_patterns = DurationPatterns()
        # re.sub('abc(.*)xyz', '\g<1>', 'abcdefprstuwxyz')
        # Callable[[], None]
        # self.get_pattern = self.get_one_note_pattern

        # new_func = getattr(my_tracker, func.__name__)
        # new_func()


    def __list_get_pattern_methods__(self):
        get_patt_search = re.compile('^get_.*_pattern$')
        return [x for x in dir(self) if get_patt_search.search(x)]

    @staticmethod
    def __init_pattern_size_for_interval__():
        max_range = 128
        # print(max_range)
        # dropwhile(lambda x: x<5, [1,4,6,4,1]) --> 6 4 1
        tuple_range = itertools.product(range(1, max_range), range(1, max_range))
        filt_range = itertools.filterfalse(lambda xy: xy[0] * xy[1] >= max_range, tuple_range)
        # print(list(filt_range))
        pattern_size_for_interval = [{x} for x in range(max_range)]
        for x, y in filt_range:
            pattern_size_for_interval[x * y].add(x)
        # print(pattern_size_for_interval)
        # pattern_size_for_interval[2]
        return pattern_size_for_interval


    def __read_config_file__(self):
        # print('reading config')
        # config_file = 'reviewed_pattern_cfg.yaml'
        config_file = 'reviewed_pattern_cfg.json'
        if IN_COLAB:
            config_file = '/content/SoundDesign/tracker/' + config_file

        with open(config_file, 'r') as file:
            # with open('reviewed_pattern_cfg.yaml', 'r') as file:
            # self.patterns_config = yaml.safe_load(file)
            self.patterns_config = json.load(file)
        # print(self.patterns_config)
        # print(self.patterns_config['play_over'])
        self.patterns = list(map(lambda x: np.array(x['pattern']), self.patterns_config['play_over']['patterns']))
        # print('after list')

        # pprint.pprint(self.patterns_config)

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
        # if interval==0:
        #   return None
        sign = np.sign(interval)
        interval = abs(interval)
        # print('patterns:',list(self.patterns))
        # print(interval)
        if interval == 0:
          suitable_patterns = [pattern for pattern in
                             self.patterns if pattern[-1] in self.pattern_size_for_interval[interval]]
          # print('sp for 0:',suitable_patterns)
        else:
          suitable_patterns = [sign * self.multiply_pattern(pattern, int(interval / pattern[-1])) for pattern in
                             self.patterns if pattern[-1] in self.pattern_size_for_interval[interval]]
        # print('sp for n:',suitable_patterns)
        return suitable_patterns

# <editor-fold desc="get pattern functions">
    def mod_duration(func):  #added self, eventual issue
        @wraps(func)
        def split_no(interval, max_len = 16):
            pattern_len=interval
            
            interval -=1

            parts_no16 = interval // max_len
            parts_no16+=1
            parts_no4 = interval // int(max_len/4)
            parts_no4+=1

            rnd_parts= random.randint(parts_no16, parts_no4 )

            splt_array=[]
            while pattern_len>0:
                part=-(-pattern_len//rnd_parts)
                splt_array.append(part)
                # print(f"x:{part=}")
                pattern_len-=part
                rnd_parts-=1
            # print(splt_array)

            # return (parts_no16, parts_no4)
            return (splt_array)
        
        
        def inner(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            print(f"xx {len(result[iso.EVENT_NOTE])=}, {result[iso.EVENT_NOTE]=}")
            if not np.any(result.get(iso.EVENT_DURATION)):
                # result[iso.EVENT_DURATION] = np.array([1, 7, 3])
                pattern_len = len(result[iso.EVENT_NOTE])-1
                
                splt_array = split_no(pattern_len)
                durations =[]
                for split_size in splt_array:
                    dur_part = random.choice([dp["pattern"] for dp in self.dur_patterns.patterns
                                    if dp["len"]==split_size])
                    dur_part2 = np.array(dur_part)/(split_size/pattern_len)
                    durations.extend(dur_part)
                # else:  #TODO fix len>16
                #     rpt = ((pattern_len-1)//16)+1
                #     patt_perm = itertools.product(self.dur_patterns.patterns,
                #                     repeat = ((pattern_len-1)//16)+1)
                #     patt_perm = list(patt_perm)
                    
                #     patt_perm_sel=[pt for pt in patt_perm if sum([p['len'] for p in pt]) == pattern_len]
                #     xxx = [ [y['pattern'] for y in x] for x in patt_perm_sel]
                #     yyy=xxx
                #     pass
                print(f"=========>{durations=}")
                result[iso.EVENT_DURATION] = 1/np.array(durations)

            return result
        return inner

    # self.dur_patterns


    @mod_duration
    def get_simple_pattern(self, interval=0):  # interval sould be not needed
        return {
            iso.EVENT_NOTE: np.append(random.choice([1,-1])*random.choice(self.patterns), 0)
        }

    # @mod_duration
    # def get_chord_maj_pattern(self, interval=0):  # interval sould be not needed
    #     return {
    #         iso.EVENT_NOTE: np.append(random.choice([1,-1])*random.choice([1,2,3])*random.choice(self.patterns), 0)
    #     }


    # @mod_duration
    # def get_simple3_pattern(self, interval=0):  # interval sould be not needed
    #     return {
    #         iso.EVENT_NOTE: np.append(random.choice([1,-1])*random.choice([1,2,3])*random.choice(self.patterns), 0)
    #     }

    @mod_duration
    def get_random_path_pattern(self, interval):
        # return random.choice(self.all_suitable_patterns(interval))
        # return {iso.EVENT_NOTE:random.choice(self.all_suitable_patterns(interval))}
        return {
            # iso.EVENT_PROGRAM_CHANGE : 22,
            # iso.EVENT_NOTE:random.choice([pattern for pattern in self.all_suitable_patterns(interval) if len(pattern)<=16])
            iso.EVENT_NOTE:random.choice([pattern for pattern in self.all_suitable_patterns(interval) ])
            # iso.EVENT_AMPLITUDE: np.array([120, 100])
            # iso.EVENT_DURATION: np.array([3, 1]),
            #  iso.EVENT_GATE: np.array([1, 0.25, 0.25, 3.25])

        }



    @mod_duration
    def get_chord_maj_pattern(self, interval=0):  # interval sould be not needed
        return {
            iso.EVENT_NOTE:  np.array([(0, 2, 4), 0],dtype=object)
        }

    @mod_duration
    def get_one_note_pattern(self, interval):
        # return np.array([0, interval])
        return {iso.EVENT_NOTE: np.array([0, interval])
            # ,iso.EVENT_AMPLITUDE: [12]
                }

    @mod_duration
    def get_rest_path_pattern(self, interval):
        # return {iso.EVENT_NOTE:np.array([0,0]) if interval == 0 else np.arange(0, interval+np.sign(interval), np.sign(interval))}
        if interval == 0:
            notes = np.array([0,0])
        else:
            real_notes = np.arange(0, interval , np.sign(interval))
            rests = np.repeat(None, abs(interval ))
            notes_with_rests = zip(real_notes, rests)
            notes = np.array([ nt for tp in notes_with_rests for nt in tp] + [None])

        return {
            iso.EVENT_NOTE:notes
            # iso.EVENT_AMPLITUDE: np.array([120, 100]),
            # iso.EVENT_DURATION : np.array([2, 1])
            # ,iso.EVENT_GATE:np.array([1, 0.25, 0.25, 3.25])
        }

    @mod_duration
    def get_path_pattern(self, interval):
        # return {iso.EVENT_NOTE:np.array([0,0]) if interval == 0 else np.arange(0, interval+np.sign(interval), np.sign(interval))}
        if interval == 0:
            notes = np.array([0,0])
        else:
            notes = np.arange(0, interval + np.sign(interval), np.sign(interval))
        return {
            iso.EVENT_NOTE:notes
            # iso.EVENT_AMPLITUDE: np.array([120, 100]),
            # iso.EVENT_DURATION : np.array([2, 1])
            # ,iso.EVENT_GATE:np.array([1, 0.25, 0.25, 3.25])
        }
    # </editor-fold>

    def set_pattern_function(self, function_name ):
        self.get_pattern = getattr(self, 'get_'+function_name+'_pattern' )




def main():
    import pprint

    global note_ptrn
    note_ptrn = NotePatterns()
    # dur_prtn = DurationPatterns()
    note_ptrn.get_path_pattern(5)
    # print(ptrn.get_random_pattern(5))
    # print(ptrn.get_one_note_pattern(5))
    # print(ptrn.all_suitable_patterns(5))

    # get_patt_search = re.compile('^get.*pattern$')
    # pprint.pprint([x for x in dir(Patterns) if get_patt_search.search(x)])
    # ptrn.list_get_pattern_methods()
    # print(note_ptrn.pattern_methods_list)
    # print(note_ptrn.get_pattern(5))
    pprint.pprint(dur_prtn.patterns)



if __name__ == '__main__':
    main()


