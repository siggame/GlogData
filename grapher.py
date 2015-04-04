from game_object import Game
import os
import cProfile
import re

import matplotlib.pyplot as plt
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
          (.4, .4, 1)]


def graph():
    import json
    plt.figure(1)
    plt.clf()
    t = open('data', 'r')
    data = json.loads(t.read())
    for i in data:
        try:
            c = colors[i[0]]
        except:
            c = (0, 0, 0)
        plt.plot(i[1][0], i[1][1], '.', c=c)

    plt.show()
    

if __name__ == '__main__':
    graph()
