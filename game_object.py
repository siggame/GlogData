from utilities import list_data, list_key, extracted_data
from collections import defaultdict

def get_game_type(game_name):
    return Game(game_name)

def get_game_data_type(game_name):
    if game_name == 'chess':
        return ChessData()
    elif game_name == 'Plants':
        return PlantsData()

class Game(object):
    def __init__(self, game_name):
        self.name = game_name
        self.created_units = 0
        self.total_turns = 0
        self.depth = 0
        self.player1_created_units = 0
        self.player2_created_units = 0

        self.units_per_turn = defaultdict(list)

    def unit_created(self):
        self.created_units += 1

    def processTurns(self, data):
        self.glogdata = get_game_data_type(self.name)
        if self.glogdata is None:
            return
        self.glogdata.set_game(self)
        sorted_keys = data.keys()
        sorted_keys.sort()
        for i in sorted_keys:
            self._process(data[i])
            
    def _process(self, data, key=None):
        for i in data:
            if type(i) == type(list()):
                self._process(list_data(i), list_key(i))
            else:
                if key is not None:
                    k = key
                    j = []
                    # special case for player since the quotes were removed
                    if k == 'Player':
                        k += '_order'
                        k = k.lower()
                        temp = i.split(' ')
                        lenth = len(self.glogdata.get_funcs(k))
                        c_l = 0
                        while c_l < lenth - 2:
                            j.append(temp[len(temp)-(c_l+1)])
                            c_l += 1
                        player_name = temp[1:len(temp)-2]
                        j.append(player_name)
                        j.append(temp[0])
                        k = 'player'
                        j = j[::-1]
                    elif k == 'animations':
                        k = list_key(i)
                        j = extracted_data(i)
                    else:
                        j = i.split(' ')
                else:
                    k = list_key(i)
                    j = extracted_data(i)

                k += '_func'
                k = k.lower()

                if self.glogdata.params().count(k):
                    # print "Processing", k, j                
                    self.glogdata.get_funcs(k)(j)
                    
                    # specific_funs = self.glogdata.get_funcs(k)
                    # for t, s in zip(specific_funs, j):
                    #    print t, s
                    #    t(s)

class GameData(object):
    def __init__(self):
        self.player_order = ['empty', 'empty', 'empty']
        self.animation = [self.empty_func, self.empty_func]

    def set_game(self, gameObj):
        self.gameObj = gameObj

    def params(self):
        return self.__dict__.keys()

    def get_funcs(self, spec):
        if self.params().count(spec):
            return self.__dict__[spec]
        else:
            return None

    def empty_func(self, data):
        pass

    def add_func(self, data):
        pass

    def width_func(self, data):
        self.gameObj.width = int(data)

    def height_func(self, data):
        self.gameObj.height = int(data)

    def turn_func(self, data):
        data = int(data)
        self.set_current_turn(data)
        if self.gameObj.total_turns < data:
            self.gameObj.total_turns = data

    def set_current_turn(self, data):
        self.current_turn = int(data)

    def get_item(self, string, d_type, data):
        return data[d_type.index(string)]

class ChessData(GameData):
    def __init__(self):
        super(ChessData, self).__init__()
        self.game_order = [self.empty_func, self.turn_func, self.empty_func, self.empty_func]
    
    def game_func(self, data):
        print data
        pass
        
class MarsData(GameData):
    def __init__(self):
        super(MarsData, self).__init__()
        self.game_func = self._game_func

    def _game_func(self, data):
        pass

class PlantsData(GameData):
    def __init__(self):
        super(PlantsData, self).__init__()

        self.game_func = self._game_func
        self.player_func = self._player_func
        self.plant_func = self._plant_func

        self.game_order = ['width', 'height', 'turn', 'empty', 'empty']
        self.player_order.extend(['spore_count'])
        self.plant_order = ['id', 'empty', 'empty', 'owner', 'empty', 'empty']

        self.plant_ids_found = []
        self.player1_ids = []
        self.player2_ids = []

        # self.uproot = [self.empty_func, self.empty_func, self.empty_func, self.empty_func, self.empty_func]
        # self.animations = [self.empty_func]

    def _game_func(self, data):
        turns = self.get_item('turn', self.game_order, data)
        self.current_turn = int(turns)
        if self.gameObj.total_turns < int(turns):
            self.gameObj.total_turns = int(turns)

        self.gameObj.width = int(self.get_item('width', self.game_order, data))
        self.gameObj.height = int(self.get_item('height', self.game_order, data))

    def _player_func(self, data):
        s_d = self.get_item('spore_count', self.player_order, data)
        if self.current_turn == 0:
            self.gameObj.spore_count_by_turn = [float(s_d)]
        else:
            self.gameObj.spore_count_by_turn.append(float(s_d))

    def _plant_func(self, data):
        plant_id = int(self.get_item('id', self.plant_order, data))
        plant_owner = int(self.get_item('owner', self.plant_order, data))
        if not self.plant_ids_found.count(int(plant_id)):
            self.plant_ids_found.append(int(plant_id))
            if plant_owner == 0:
                self.gameObj.player1_created_units += 1
            elif plant_owner == 1:
                self.gameObj.player2_created_units += 1

        if self.gameObj.created_units < len(self.plant_ids_found):
            self.gameObj.created_units = len(self.plant_ids_found)

        self.gameObj.units_per_turn[self.current_turn].append((plant_id, plant_owner))


    def spore_count(self, data):
        if self.current_turn == 0:
            self.gameObj.spore_count_by_turn = [float(data)]
        else:
            self.gameObj.spore_count_by_turn.append(float(data))
