import numpy as np
import itertools
import random
import yaml
import pprint

import sys
global IN_COLAB
IN_COLAB = 'google.colab' in sys.modules

class Patterns:
    def __init__(self):
        self.__read_config_file__()
        self.pattern_size_for_interval = self.__init_pattern_size_for_interval__()


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

    def get_suitable_pattern(self, interval):
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

    def get_random_pattern(self, interval):

      return random.choice(self.get_suitable_pattern(interval))


    def __read_config_file__(self):
        # print('reading config')
        config_file = 'reviewed_pattern_cfg.yaml'
        if IN_COLAB:
          config_file = '/content/SoundDesign/tracker/'+config_file
          
        with open(config_file, 'r') as file:
        # with open('reviewed_pattern_cfg.yaml', 'r') as file:
            self.patterns_config = yaml.safe_load(file)
        # print(self.patterns_config)
        # print(self.patterns_config['play_over'])
        self.patterns = list(map(lambda x: np.array(x['pattern']), self.patterns_config['play_over']['patterns']))
        # print('after list')

        # pprint.pprint(self.patterns_config)


def main():
    ptrn = Patterns()



if __name__ == '__main__':
    main()


