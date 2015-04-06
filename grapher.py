from game_object import Game
import os
import cProfile
import re
import colorsys 
import matplotlib.pyplot as plt
import random
from itertools import cycle

colors = [(1, 0, 0),
          (0, 1, 0),
          (1, 1, 0),
          (0, 1, 1),
          (1, 0, 1),
          (0, .8, 1),
          (0, 1, .2),
          (.4, 0, 0),
          (.6, .8, .2),
          (.4, .4, 1),
          (.6, 1.0, 1.0),
          (.8, 1.0, .2),
          (1, 1, .6)]


def colors_gen(count):
    for i in range(count):
        temp = [float(i)/count, 1, .5]
        random.shuffle(temp)
        yield colorsys.rgb_to_hls(temp[0], temp[1], temp[2])

def graph():
    import json
    plt.figure(1)
    plt.clf()
    t = open('data', 'r')
    data = json.loads(t.read())
    color_c = max(data, key = lambda x: x[0])[0]
    for i in data:
        try:
            c = colors[i[0]]
        except:
            c = (0, 0, 0)
        plt.plot(i[1][0], i[1][1], '.', c=c)
    plt.ylabel("average number of deaths from traps")
    plt.xlabel("average number of player 1 currency")
    plt.show()
    

if __name__ == '__main__':
    graph()
