import os
import general_utils

def generate_enoki_file(functions, func_num, num_params):
    with open('./tests/utils/static_code/enoki.txt', 'r') as file:
        enoki = file.read()
    enoki_file = open("./tests/utils/enoki.cpp", "w+")

    num_vars = len(functions[func_num][1])

    derivative = functions[func_num][0]
    enoki_init_vars = generate_enoki_init_vars(functions[func_num][1])
    enoki_fill = generate_enoki_fill(functions[func_num][1])
    enoki_us_vars = generate_enoki_us_vars(functions[func_num][1])
    set_requires_grads = generate_set_requires_grads(functions[func_num][1])
    grads = generate_grads(functions[func_num][1])
    print_to_outfile = generate_print_to_outfile(functions[func_num][1])

    param_filename = "./tests/utils/params.txt"

    cpp_code = enoki % (num_params, num_vars, enoki_init_vars, 
                param_filename, enoki_fill, enoki_us_vars, 
                set_requires_grads, derivative, grads, print_to_outfile)
    enoki_file.write(cpp_code)
    enoki_file.close()

def generate_enoki_init_vars(variables):
    return_string = ""
    for var in variables:
        return_string += "\tFloatX init_{} = zero<FloatX>(num_params);\n".format(var)
    return return_string

def generate_enoki_fill(variables):
    return_string = ""
    for i, var in enumerate(variables):
        return_string += "\t\tinit_{}[i] = args[i * num_vars + {}];\n".format(var, i)
    return return_string

def generate_enoki_us_vars(variables):
    return_string = ""
    for var in variables:
        return_string += "\tFloatD {}(init_{});\n".format(var, var)
    return return_string

def generate_set_requires_grads(variables):
    return_string = ""
    for var in variables:
        return_string += "\tset_requires_gradient({});\n".format(var)
    return return_string

def generate_grads(variables):
    return_string = ""
    for var in variables:
        return_string += "\tFloatX grad_{} = gradient({});\n".format(var, var)
    return return_string

def generate_print_to_outfile(variables):
    return_string = ""
    for var in variables:
        return_string += "\t\toutfile << grad_{}[i] << \" \";\n".format(var)
    return return_string

def compile_enoki():
    cmd = "g++ -std=c++17 -I ./tests/utils/ext/enoki/include/ -I ./tests/utils/ext/ ./tests/utils/enoki.cpp -o ./tests/utils/enoki -ffast-math -O3"
    os.system(cmd)

def run_enoki():
    cmd = "./tests/utils/enoki ./tests/utils/enoki_output.txt"
    os.system(cmd)
    return general_utils.parse_output("./tests/utils/enoki_output.txt")