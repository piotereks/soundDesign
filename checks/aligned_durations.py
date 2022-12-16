import numpy as np
from fractions import Fraction as F
import pytest

def align_begin(step=1):
    return set((np.arange(0,1,1/step)).round(5))


def align_rng(step=1):
    # return np.arange(0,pow(step,2),step)+step
    return set((np.arange(0,1,1/step)+1/step).round(5))

ret_pattern= np.array([4,4,8,8,4])    
# I will know if it is aligned alread
# aligned 2 and 4, but 4 is important - dynamic is 120 80 100 80  (out of 1,28) 
# shall this be expressed maybe as % from 128? or really constants (% seem better)
# there will be only couple of amplitude patterns 
# opt 1 - dynamic only for begining
# opt 2 - dynamic for whole 1/4 of period
# accents are within beat, not bar necesarilly
# then recalculation might be not needed here since accent will be always 
# on first note of beat (in my design this is for playfrom_to function and always first note)
print(f"{ret_pattern=}")
print(align_begin(4))
ret_pattern_set=set((1/np.array(ret_pattern)).cumsum().round(5))
print(f"{ret_pattern_set=}")

 


# print(pow(2,2), pow(5,2))
# print(align_rng(2))
# print(align_rng(3))
# print(align_rng(4))
# print(align_rng(6))
# print(align_rng(8))
# print(align_rng(10))
# print(align_rng(12))

# assert float(F(1,3)) == 1/3
# x = {1,2,3}
# y = {2,3,4}
# z = {2,3}
# print(x&y, x&y == z)

# # aaa = [sum(xx) for xx in x]
# # print(aaa)
# x =np.array([1,2,3])
# y = x + np.roll(x, 1)
# print(x.cumsum())

# # tst = np.array([2.0, 4.0, 4.0])
# tst = np.array([2.0, 3.0, 6.0])
# # 1/2 1/3 1/6
# a2 = np.array([2,2])
# a4 = np.array([4,4,4,4])

# # a = set(map(lambda x : round(x,5), (1/tst).cumsum()))
# a = set((1/tst).cumsum().round(5))
# print(a,(1/a2).cumsum(), (1/a4).cumsum())
# # print(np.array(tst).cumsum())

# # print(align_rng(2))
# al2 = align_rng(2)
# print(a & al2 == al2)

# print(a)
# print(a & al2)
# print(al2)
# print(a & al2 == al2)

