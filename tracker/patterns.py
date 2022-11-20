import numpy as np
import itertools
import random
import yaml
import pprint

import sys
import re
from typing import Callable

global IN_COLAB
IN_COLAB = 'google.colab' in sys.modules

class Patterns:

    def __init__(self):
        self.__read_config_file__()
        self.pattern_size_for_interval = self.__init_pattern_size_for_interval__()
        # self.get_pattern = self.get_path_pattern
        self.pattern_methods_list = self.__list_get_pattern_methods__()
        self.pattern_methods_short_list  = [re.sub('get_(.*)_pattern', '\g<1>', method) for method in self.__list_get_pattern_methods__()]
        self.get_pattern = getattr(self, self.pattern_methods_list[0])
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
        config_file = 'reviewed_pattern_cfg.yaml'
        if IN_COLAB:
            config_file = '/content/SoundDesign/tracker/' + config_file

        with open(config_file, 'r') as file:
            # with open('reviewed_pattern_cfg.yaml', 'r') as file:
            self.patterns_config = yaml.safe_load(file)
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
    def get_random_pattern(self, interval):
        return random.choice(self.all_suitable_patterns(interval))


    def get_one_note_pattern(self, interval):
        return np.array([0, interval])


    def get_path_pattern(self, interval):
        return np.array([0,0]) if interval == 0 else np.arange(0, interval+np.sign(interval), np.sign(interval))
    # </editor-fold>

    def set_pattern_function(self, function_name ):
        self.get_pattern = getattr(self, 'get_'+function_name+'_pattern' )




def main():
    global ptrn
    ptrn = Patterns()
    # print(ptrn.get_random_pattern(5))
    # print(ptrn.get_one_note_pattern(5))
    # print(ptrn.all_suitable_patterns(5))
    import pprint
    # get_patt_search = re.compile('^get.*pattern$')
    # pprint.pprint([x for x in dir(Patterns) if get_patt_search.search(x)])
    # ptrn.list_get_pattern_methods()
    print(ptrn.pattern_methods_list)
    print(ptrn.get_pattern(5))




if __name__ == '__main__':
    main()


