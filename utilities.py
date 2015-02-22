
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
        temp = expr_data(_list)
        if temp:
            return temp[0]
        else:
            return []

def extracted_data(string):
    t = string.split(' ')
    t.pop(0)
    return t
