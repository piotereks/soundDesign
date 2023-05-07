import numpy as np
from fractions import *

def func(x, a):
    return -a*np.cos(np.deg2rad(x)/2) + np.sin(np.deg2rad(x))

def find_a(a):
    x_vals = np.arange(0, 361, 0.01)
    y_vals = np.abs(func(x_vals, a))
    # print(y_)
    max_val = np.max(y_vals)

    # return(Fraction(max_val/a).limit_denominator(100))
    return(a,1/a, max_val/a)
    # a = max_val * 2/3
    # return a

# a = find_a()
# print(a)
# a_vals = np.arange(0.5, 1.5, 0.01)
# xxx = [find_a(a) for a in np.arange(0.5, 1.5, 0.01) if abs(1.5-find_a(a)[1])<=0.001]
xxx = [find_a(a) for a in np.arange(0.01, 1.5, 0.001) if abs(1.5-abs(find_a(a)[2]))<=0.002]
print(xxx)