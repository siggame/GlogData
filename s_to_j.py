from bz2 import BZ2File

def decompress_file(filename):
    f = BZ2File(filename + '.glog', 'r')
    log = f.read()
    f.close()
    new_file = open(filename + '.gamelog', 'w')
    new_file.write(log)
    new_file.close()

def convert_file(filename):
    reader = open(filename + '.gamelog', 'r')
    log = reader.read()
    data = datatize_expr(log, 0)
    print 'Top layer'
    for i in data:
        print i[0]

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
                p_data = [expr_key(s_exp)]
                p_data.extend(datatize_expr(strip_parent_expr(s_exp), depth + 1))
                data.append(p_data)
            else:
                data.append([s_exp])
    return data

def expr_key(expr):
    return expr.strip('(').split(' ')[0]

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
    filename = '10022-c0ca0'
    # decompress_file(filename)
    convert_file(filename)
    # print strip_parent_expr('3 (412 h (e w3) (3 1))')
    
