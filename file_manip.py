from bz2 import BZ2File
from collections import defaultdict
from utilities import sexpr_key, expr_key, expr_data, list_key, list_data
import time

def decompress_file(filename):
    filename_ext = filename.split('.')
    f = BZ2File(filename, 'r')
    try:
        log = f.read()
    except IOError:
        print("Error invalid data stream")
        return 

    f.close()
    new_file = open(filename_ext[0] + '.gamelog', 'w')
    new_file.write(log)
    new_file.close()

def get_log(filename):
    filename_ext = filename.split('.')
    log = ''
    if filename_ext[1] == 'glog':
        print("Assuming bz2 compression")
        f = BZ2File(filename, 'r')
        try:
            log = f.read()
        except IOError:
            print("Error invalid data stream")
            print("File is not bz2")
            print("Trying file as uncompressed format")
            filename_ext[1] = 'gamelog'
        f.close()
    
    if filename_ext[1] == 'gamelog':
        print("Assuming uncompressed gamelog")
        f = open(filename, 'r')
        log = f.read()
    return log

def get_data(filename):
    log = get_log(filename)
    if type(log) == bytes:
        data = datatize_expr(str(log), 0)
    else:
        data = datatize_expr(log, 0)
    return data

def convert_data(data):
    data_dict = {}
    data_dict['super'] = {}
    data_dict['turns'] = defaultdict(list)
    turn_numb = -1
    for i in data:
        if list_key(i) == 'gameName':
            data_dict['super']['gameName'] = list_data(i)
        elif list_key(i) == 'status':
            turn_numb += 1
            data_dict['turns'][turn_numb] = list_data(i)
        elif list_key(i) == 'animations':
            data_dict['turns'][turn_numb].append(i)
        elif list_key(i) == 'game-winner':
            data_dict['super']['winner'] = i
    return data_dict

def datatize_expr(expr, depth):
    s_exp = ""
    p_count = 0
    building_exp = False
    has_sub_exp = False
    data = []
    for index, i in enumerate(expr):
        if i == '(':
            p_count += 1
            if building_exp:
                has_sub_exp = True
        elif i == ')':
            p_count -= 1
        
        if p_count == 1 and not building_exp:
            s_exp = i
            building_exp = True
            has_sub_exp = False
        elif p_count >= 1 and building_exp:
            s_exp += i
        elif p_count == 0 and building_exp:
            building_exp = False
            s_exp += i
            if has_sub_exp:
                p_data = [expr_key(clean_expr(s_exp))]
                p_data.append([s_data for s_data in datatize_expr(strip_parent_expr(s_exp), depth + 1)])
                data.append(p_data)
            else:
                data.append(clean_expr(s_exp))
    return data

def clean_expr(expr):
    return strip_quotes(strip_paren(expr))

def strip_paren(expr):
    return expr[1:len(expr)-1]
    # return expr.strip('(').strip(')')

def strip_quotes(expr):
    return expr.replace('"', '')

def strip_parent_expr(string):
    string = string[string.find('(')+1:]
    string = string[string.find('('):]
    string = string[:string.rfind(')')+1]
    string = string[:string.rfind(')')]
    return string

def strip_parent_expr_old(string):
    new_string = ""
    p_count = 0
    building_exp = False
    for i in string:
        if i == '(':
            p_count += 1
        elif i == ')':
            p_count -= 1
        
        if p_count == 2 and not building_exp:
            new_string = i
            building_exp = True
        elif p_count >= 2 and building_exp:
            new_string += i
        elif p_count == 1 and building_exp:
            new_string += i
            if p_count == 0:
                building_exp = False
    return new_string

def testing():
    # filename = '10022-c0ca0.gamelog'
    # filename = '10007-eb6d8.gamelog'
    filename = 'glogs/10007-eb6d8.glog'
    # decompress_file(filename + '.gamelog')
    data = convert_data(get_data(filename))
    from game_object import Game

    c = Game(data['super']['gameName'])
    c.processTurns(data['turns'])
    print('total turns', c.total_turns)
    print(c.width)
    print(c.height)
    print(c.spore_count_by_turn)
    print(c.created_units)
    print(c.player1_created_units)
    print(c.player2_created_units)
    print(c.units_per_turn)
    

def datatize_test():
    string = '''("gameName" "Plants")("status" ("game" 2048 1024 0 300 0 10007 75 10 5 10 500 50) ("Player" (0 "Shell AI" 10 50.000000) (1 "Why do Golbats wear plants?" 10 0)) ("Mappable") ("Plant" (10 151 512 0 0 0 1200 0 0 150 0 0 0 0 0 0) (11 1896 512 1 0 0 1200 0 0 150 0 0 0 0 0 0) (12 289 336 2 7 0 0 0 0 100 0 0 200 0 200 200) (13 1759 336 2 7 0 0 0 0 100 0 0 200 0 200 200) (14 577 554 2 7 0 0 0 0 100 0 0 200 0 200 200) (15 1471 554 2 7 0 0 0 0 100 0 0 200 0 200 200) (16 554 908 2 7 0 0 0 0 100 0 0 200 0 200 200) (17 1494 908 2 7 0 0 0 0 100 0 0 200 0 200 200) (18 302 313 2 7 0 0 0 0 100 0 0 200 0 200 200) (19 1746 313 2 7 0 0 0 0 100 0 0 200 0 200 200) (20 621 266 2 7 0 0 0 0 100 0 0 200 0 200 200) (21 1427 266 2 7 0 0 0 0 100 0 0 200 0 200 200) (22 815 150 2 7 0 0 0 0 100 0 0 200 0 200 200) (23 1233 150 2 7 0 0 0 0 100 0 0 200 0 200 200) (24 460 869 2 7 0 0 0 0 100 0 0 200 0 200 200) (25 1588 869 2 7 0 0 0 0 100 0 0 200 0 200 200)) ("Mutation" (2 "Mother" 0 0 0 1200 150 0 0 0 0) (3 "Spawner" 1 5 0 40 75 0 0 0 0) (4 "Choker" 2 10 1 10 40 1 1 6 18) (5 "Soaker" 3 25 1 40 20 1 0 0 25) (6 "Tumbleweed" 4 10 1 15 30 1 5 9 27) (7 "Aralia" 5 60 1 90 60 1 20 38 80) (8 "Titan" 6 24 0 66 70 1 3 3 3) (9 "Pool" 7 0 0 0 100 0 0 200 200)))("animations" ("add" 0) ("add" 1) ("add" 2) ("add" 3) ("add" 4) ("add" 5) ("add" 6) ("add" 7) ("add" 8) ("add" 9) ("add" 10) ("add" 11) ("add" 12) ("add" 13) ("add" 14) ("add" 15) ("add" 16) ("add" 17) ("add" 18) ("add" 19) ("add" 20) ("add" 21) ("add" 22) ("add" 23) ("add" 24) ("add" 25))'''
    dat = datatize_expr(string, 0)
    c_d = convert_data(dat)
    print(c_d)

def droid_test():
    filename = '35-d5198.glog'
    data = convert_data(get_data(filename))
    from game_object import Game
    c = Game(data['super']['gameName'])
    c.processTurns(data['turns'])
    print(c.created_units)

if __name__ == "__main__":
    droid_test()
