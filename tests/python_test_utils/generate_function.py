import string
import random

character_selection = 'abcdefghjklmnopqrstuvwxzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def gen_other(s):
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

def generate_poly(degree, variables, terms, input_string):
    def gen_polynomial(select_deg, append_term, select_var):
        for deg in range(0, select_deg-1):
            append_term += select_var + ' * '
        append_term += select_var
        return append_term


    op = [' + ', ' - ', ' * ', ' / ']
#     paranthesis = ['']
    blocks = random.randint(1,1)
    

    append_term = ''
    for b in range(blocks):

        select_deg = random.randint(1,degree)
        select_var = random.choice(variables)
        # fix this
#         select_paranthesis = random.choice(paranthesis)

        
        if b==0:
            append_term += gen_polynomial(select_deg, append_term, select_var)
        else:
            append_term = append_term + ' * '+gen_polynomial(select_deg, '', select_var)

    select_op = random.choice(op)
    
    if len(input_string)==0:
        input_string.append('('+append_term+')')
    else:
        input_string.append(select_op + '('+ append_term+')')

    if len(input_string) == terms:
        final_string = ''.join(input_string)  
        return final_string
    else:          
        return function_generator(degree, variables, terms, input_string)