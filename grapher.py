from game_object import Game
from file_manip import convert_data, get_data
import os

def gather_all_data(path):
    glogs = [path + '/' + i for i in os.listdir(path)]
    # glogs = ['/Users/brandon/Desktop/glog/glogs/10045-ed136.glog']
    for i in glogs:
        print i
    s = [convert_data(get_data(i)) for i in glogs]
    t = [Game(i['super']['gameName']) for i in s]
    for j, i in zip(t, s):
        j.processTurns(i['turns'])

    plants_games = [i for i in t if i.name == 'Plants']

    for i in plants_games:
        print "Data!"
        print 'created units', i.created_units
        print 'total turns', i.total_turns
        print 'player 1 units', i.player1_created_units
        print 'player 2 units', i.player2_created_units
        print 'spore count', i.spore_count_by_turn
        # print i.winner

if __name__ == '__main__':
    gather_all_data(os.path.abspath('glogs'))

