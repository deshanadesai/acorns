import string
import random

character_selection = 'abcdefghjklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def create_func(s):
    if s > len(character_selection):
        raise Exception("s must be less than {}".format(len(character_selection))) 
    vars = create_vars(s)

    function_string = ""

    prefix_string = ""
    for i in range(s):
        prefix_string += "4*"

    product_string = ""
    for i, var in enumerate(vars):
        product_string += "({} * (1 - {}))".format(var, var)

        if (i != len(vars) - 1):
            product_string += "*"
    
    function_string = prefix_string + "(" + product_string + ")"

    function = [function_string, vars]
    print (function)
    print(vars)
    return function

def create_vars(s):
    vars = []
    i = 0
    while i < s:
        letter = random.choice(character_selection)
        if letter not in vars:
            vars.append(letter)
            i += 1
    return vars

create_func(36)
