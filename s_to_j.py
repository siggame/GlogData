from bz2 import BZ2File
from collections import defaultdict

class Game(object):
    def __init__(self, data):
        self.set_data(data)
        self.data = {}
    
    def set_name(self, data):
        for i in data:
            if expr_key(i[0]) == 'gameName':
                self.name = expr_data(i[0])[0]
                break

    def set_data(self, data):
        self.set_name(data)
        

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
    for i in data:
        print i
        print ""
    return data

def convert_data(data):
    print ""
    print "DATA!"

    data_dict = defaultdict(list)

    turn_numb = 0
    for i in data:

        print "key", list_key(i)

        if list_key(i) == 'gameName':
            data_dict['gameName'] = list_data(i)
        elif list_key(i) == 'status':
            turn_numb += 1
            data_dict['turn_%d' % turn_numb] = list_data(i)
        elif list_key(i) == 'animations':
            print list_data(i)
            data_dict['turn_%d' % turn_numb].append(i)

    print 'gameName', data_dict['gameName']
    print 'turn_1', data_dict['turn_1']
    print ""
    print 'turn_2', data_dict['turn_2']
    print ""
    print 'turn_3', data_dict['turn_3']

func_count = 0

def datatize_expr(expr, depth):
    global func_count
    func_count += 1
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
                #if depth >= 1:
                #    data.append(clean_expr(s_exp))
                #else:
                #    data.append([clean_expr(s_exp)])
                data.append(clean_expr(s_exp))
    return data

def sexpr_key(s_expr):
    return s_expr.strip('(').split(' ')[0]

def expr_key(expr):
    return expr.split(' ')[0]

def expr_data(expr):
    return expr.split(' ')[1:]

def list_key(_list):
    if type(_list) is type(list()):
        return _list[0]
    else:
        return expr_key(_list)

def list_data(_list):
    if type(_list) is type(list()):
        return _list[1]
    else:
        print _list
        temp = expr_data(_list)
        if temp:
            return temp[0]
        else:
            return []

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
    convert_data(get_data(filename))
    # print strip_parent_expr('3 (412 h (e w3) (3 1))')
    
