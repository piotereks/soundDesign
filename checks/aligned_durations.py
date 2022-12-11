import numpy as np
from fractions import Fraction as F
import pytest

def align_rng2(step=1):
    return set(np.arange(0,1,1/step)+1/step)


def align_rng(step=1):
    # return np.arange(0,pow(step,2),step)+step
    return set((np.arange(0,1,1/step)+1/step))

print(pow(2,2), pow(5,2))
print(align_rng(2))
print(align_rng(3))
print(align_rng(4))
print(align_rng(6))
print(align_rng(8))
print(align_rng(10))
print(align_rng(12))

assert float(F(1,3)) == 1/3
x = {1,2,3}
y = {2,3,4}
z = {2,3}
print(x&y, x&y == z)

# aaa = [sum(xx) for xx in x]
# print(aaa)
x =np.array([1,2,3])
y = x + np.roll(x, 1)
print(x.cumsum())

# tst = np.array([2.0, 4.0, 4.0])
tst = np.array([2.0, 3.0, 6.0])
# 1/2 1/3 1/6
a2 = np.array([2,2])
a4 = np.array([4,4,4,4])

# a = set(map(lambda x : round(x,5), (1/tst).cumsum()))
a = set((1/tst).cumsum().round(5))
print(a,(1/a2).cumsum(), (1/a4).cumsum())
# print(np.array(tst).cumsum())

# print(align_rng(2))
al2 = align_rng(2)
print(a & al2 == al2)

print(a)
print(a & al2)
print(al2)
print(a & al2 == al2)

