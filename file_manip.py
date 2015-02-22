from bz2 import BZ2File
from collections import defaultdict
from utilities import sexpr_key, expr_key, expr_data, list_key, list_data

def decompress_file(filename):
    filename_ext = filename.split('.')
    f = BZ2File(filename, 'r')
    try:
        log = f.read()
    except IOError:
        print "Error invalid data stream"
        return 

    f.close()
    new_file = open(filename_ext[0] + '.gamelog', 'w')
    new_file.write(log)
    new_file.close()

def get_log(filename):
    filename_ext = filename.split('.')
    log = ''
    if filename_ext[1] == 'glog':
        print "Assuming bz2 compression"
        f = BZ2File(filename, 'r')
        try:
            log = f.read()
        except IOError:
            print "Error invalid data stream"
            print "File is not bz2"
            print "Trying file as uncompressed format"
            filename_ext[1] = 'gamelog'
        f.close()
    
    if filename_ext[1] == 'gamelog':
        print "Assuming uncompressed gamelog"
        f = open(filename, 'r')
        log = f.read()
    return log

def get_data(filename):
    log = get_log(filename)
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
                # print p_data
                data.append(p_data)
            else:
                data.append(clean_expr(s_exp))
    return data

def clean_expr(expr):
    return strip_quotes(strip_paren(expr))

def strip_paren(expr):
    return expr.strip('(').strip(')')

def strip_quotes(expr):
    return expr.replace('"', '')

def strip_parent_expr(string):
    # string = strip_junk(string)
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

if __name__ == "__main__":
    # filename = '10022-c0ca0.gamelog'
    filename = '10007-eb6d8.gamelog'
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