from game_object import Game
import os
import cProfile
import re

import matplotlib.pyplot as plt
from itertools import cycle

def graph():
    import json
    plt.figure(1)
    plt.clf()
    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    t = open('data', 'r')
    data = json.loads(t.read())
    for i in data:
        plt.plot(i[0], i[1], '.')

    plt.show()
    

if __name__ == '__main__':
    graph()
