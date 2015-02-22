from utilities import list_data, list_key, extracted_data

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

    def unit_created(self):
        self.created_units += 1

    def processTurns(self, data):
        self.glogdata = get_game_data_type(self.name)
        self.glogdata.set_game(self)
        sorted_keys = data.keys()
        sorted_keys.sort()
        for i in sorted_keys:
            print i
            self._process(data[i])

            
    def _process(self, data, key=None):
        self.depth += 1
        for i in data:
            print i
            if type(i) == type(list()):
                self._process(list_data(i), list_key(i))
            else:
                if key is not None:
                    k = key
                    j = []
                    # special case for player since the quotes were removed
                    if k == 'Player':
                        temp = i.split(' ')
                        lenth = len(self.glogdata.get_funcs(k))
                        print temp, lenth
                        c_l = 0
                        while c_l < lenth - 2:
                            j.append(temp[len(temp)-(c_l+1)])
                            c_l += 1
                        player_name = temp[1:len(temp)-2]
                        j.append(player_name)
                        j.append(temp[0])
                        j = j[::-1]
                    else:
                        j = i
                else:
                    k = list_key(i)
                    j = extracted_data(i)

                if self.glogdata.params().count(k):
                    print "Processing", k, repr(j)
                    specific_funs = self.glogdata.get_funcs(k)
                    for t, s in zip(specific_funs, j):
                        print t, s
                        t(s)

class GameData(object):
    def __init__(self):
        self.Player = [self.empty_func, self.empty_func, self.empty_func]

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

class ChessData(GameData):
    def __init__(self):
        super(ChessData, self).__init__()
        self.game = [self.empty_func, self.turn_func, self.empty_func, self.empty_func]
        
class PlantsData(GameData):
    def __init__(self):
        super(PlantsData, self).__init__()
        self.game = [self.width_func, self.height_func,
                     self.turn_func, self.empty_func, 
                     self.empty_func, self.empty_func, 
                     self.empty_func, self.empty_func, 
                     self.empty_func, self.empty_func,
                     self.empty_func, self.empty_func]
        self.Player.append(self.spore_count)

    def spore_count(self, data):
        print("Spore count")
        if self.current_turn == 0:
            self.gameObj.spore_count_by_turn = [float(data)]
        else:
            self.gameObj.spore_count_by_turn.append(float(data))
