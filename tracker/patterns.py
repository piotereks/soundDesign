import numpy as np
import itertools
import random 
import yaml
import pprint


class Patterns:
  def __init__(self):
    self.__read_config_file__()
    self.pattern_size_for_interval=self.__init_pattern_size_for_interval__()
    self.patterns=map(np.array, [
          [0,1,2,3,1],
          [0,2,1,3,2],
          [0,-1,1],
          [0,1,2,3,4,5,6,7,8],
          [0,2,1,3]
          ])

    # self.patterns=[
    #       [0,1,2,3,1],
    #       [0,2,1,3,2],
    #       [0,-1,1],
    #       [0,1,2,3,4,5,6,7,8],
    #       [0,2,1,3]
    #       ]
    # self.patterns=[np.array(pattern) for pattern in self.patterns]
      
  def __init_pattern_size_for_interval__(self):
    max_range=128
    # dropwhile(lambda x: x<5, [1,4,6,4,1]) --> 6 4 1
    tuple_range=itertools.product(range(1,max_range),range(1,max_range))
    filt_range=itertools.filterfalse(lambda xy: xy[0]*xy[1]>=max_range, tuple_range)
    # print(list(filt_range))
    pattern_size_for_interval=[{x} for x in range(max_range)]
    for x,y in filt_range:
      pattern_size_for_interval[x*y].add(x)
    # print(pattern_size_for_interval)
    pattern_size_for_interval[2]
    return pattern_size_for_interval
  # pattern_size_for_interval=init_pattern_size_for_interval()
  # print(pattern_size_for_interval)  

  def multiply_pattern(self,pattern, mult): # target function should return already PSequence
    pattern=np.array(pattern)
    if mult==1:
      return pattern
      # or return pattern[1:]
    else:
      res_pattern=pattern # Check if pattern can be modified withing function and is not modyfing top
      add_pattern=np.array(pattern[1:])
      # print(pattern, res_pattern, add_pattern)
      
    for a in range(mult-1):
      add_pattern=add_pattern+pattern[-1]  # This is to add "step" of pattern, so I expect
      # [0, 2, 3, 2, 1] + 1 => [1, 3, 4, 3, 2]
      # Check if this works
      res_pattern = np.append(res_pattern,add_pattern)
    return res_pattern #[:-1]

  def get_suitable_pattern(self,interval):
    # if interval==0:
    #   return None
    sign=np.sign(interval)
    interval=abs(interval)  
    suitable_patterns=[sign*self.multiply_pattern(pattern,int(interval/pattern[-1])) for pattern in patterns if pattern[-1] in self.pattern_size_for_interval[interval]] 
    return suitable_patterns

  def get_random_pattern(self,interval):
    if interval!=0:
      return random.choice(self.get_suitable_pattern(interval)) 
    else:
      None

  def __read_config_file__(self):
    with open('/content/SoundDesign/reviewed_pattern_cfg.yaml', 'r') as file:
      self.patterns_config = yaml.safe_load(file)

      pprint.pprint(self.patterns_config)

ptrn=Patterns()





# print(np.array(pattern) for pattern in patterns)
# for x in np_patterns:
  # print(x,x+2)

suitable_patterns=[pattern for pattern in patterns if pattern[-1] in pattern_size_for_interval[2]] 
#recalculated intervals here.

print('sp',suitable_patterns)