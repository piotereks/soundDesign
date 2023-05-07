

import matplotlib.pyplot as plt
import numpy as np
import math


def draw_function(function):
    # 100 linearly spaced numbers
    # x = np.linspace(-5,5,100)
    x = np.linspace(0,360,100)


    # the function, which is y = x^2 here
    # y = x**2
    y = function(x)

    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # plot the function
    plt.plot(x,y, 'r')

    # show the plot
    plt.show()






if __name__ == '__main__':
    pass
    r=32
    # vect = np.vectorize(np.int)
    # y = 5*np.sin(x)
    # draw_function(lambda x: x**2)
    # draw_function(lambda x: 5*math.sin(2*math.pi*x/32))
    def fun(x):
        # y1 = 5*np.cos(np.radians(x)/2)
        # y1 = np.sin(np.radians(90+x/2))
        # y2 = 0.5*np.sin(np.radians(x))
        y1 = -1.38/10*np.cos(np.radians(x/2))
        y1 = -0.46*np.cos(np.radians(x/2))
        # y1 = 1.376556396484375*np.cos(np.radians(x/2))
        y2 = np.sin(np.radians(x))
        # -sin(x / 2) / 2 + cos(x)
        # y1 = np.cos(np.radians(x))
        # y2 = -1/2*np.sin(np.radians(x/2))
        # math.sin(math.pi * x / r) + 1.38*math.cos(math.pi * x / r/ 2)
        # y2=0
        return y1+y2


    # notes = [-5 * len(key.scale.semitones)
    #          + key.scale.indexOf(5 * key.scale.octave_size + round(scale_interval *
    #             (math.sin(math.pi * x / r) + 1.38*math.cos(math.pi * x / r/ 2))))
    #          for x in range(r + 1)]

    # scale_interval / 2 / 1.38 * (+ math.sin(2 * math.pi * x / r) - (1.38 * math.cos(2 * math.pi * x / r / 2) - 1.38))

    # for x in range(0, 36000):
    #     if abs(fun(x/100))<0.0001:
    #         print(x/100,fun(x/100))

    # szukamy maksimum i minimum w przedziale [0, 2*pi]
    max_y = float('-inf')
    min_y = float('inf')
    for i in range(0, 36001):
        x = i / 100
        val = fun(x)
        if val > max_y:
            max_y = val
            max_x = x
        if val < min_y:
            min_y = val
            min_x = x

    print(f"Maksimum wynosi y({max_x}) = {max_y}")
    print(f"Minimum wynosi y({min_x}) = {min_y}")

    print(fun(max_x), fun(0), fun(max_x)/fun(0))
    print(fun(min_x), fun(360), fun(min_x)/fun(360))
    # print(fun(0))
    # print(fun(360))


    draw_function(lambda x : fun(x))
    # notes = [int(5*math.sin(2*math.pi*x/r)) for x in range(r+1)]
    # 72.75     7.760498952347206e-06
    # 287.25    7.760498952125161e-06
    # 1.760172593020045
    # -1.760172593020045

    print('Processing Done')