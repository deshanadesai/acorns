import os
import sys
import general_utils
import os
from subprocess import PIPE, run

def generate_function_c_file(func_num, functions, input_filename):
    f = open(input_filename, 'w')
    signature = ""
    function = functions[func_num]
    signature += "double function_" + str(func_num) + "("
    for j in range(len(function[1])):
        var = function[1][j]
        signature += "double " + var
        if j == len(function[1]) - 1:
            signature += ")\n"
        else:
            signature += ", "
    body = "{"
    body += "\ndouble p = " + function[0] + ";"
    body += "\n\treturn p;"
    body += "\n}"
    output = signature + body
    f.write(output)
    f.close()

def generate_derivatives_c_file(func_num):
    cmd = "./tests/utils/ext/tapenade/bin/tapenade ./tests/utils/tapenade_func.c -head function_{} -reverse -output \"./tests/utils/tapenade_ders\"".format(func_num)
    os.system(cmd)
    with open("./tapenade_ders_b.c") as file:
        c_code = file.read()
        c_code = c_code.replace("#include <adBuffer.h>", "")
        output_file = open('./tests/utils/tapenade_ders.c', "w+")
        output_file.write(c_code)
        output_file.close()
    
def generate_derivative_string(vars, num_vars, func_num):
    der_string = ""
    for i, var in enumerate(vars):
        der_string += "\t\tdouble {} = values[i * {} + {}];\n".format(var, num_vars, i)
        der_string += "\t\tdouble {}b = 0;\n".format(var)
    der_string += "\t\tdouble function_{}b = 1;\n".format(func_num)
    der_string += "\t\tfunction_{}_b(".format(func_num)
    for var in vars:
        der_string += "{}, &{}b, ".format(var, var)
    der_string += "function_{}b);\n".format(func_num)
    for i, var in enumerate(vars):
        der_string += "\t\tders[i * {} + {}] = {}b;\n".format(num_vars, i, var)
    return der_string

def generate_runnable_tapenade(vars, num_vars, func_num):
    ders_string = generate_derivative_string(vars, num_vars, func_num)
    tapenade_der = None
    with open("./tests/utils/tapenade_ders.c") as file:
        tapenade_der = file.read()
    with open("./tests/utils/static_code/runnable_tapenade.txt") as file:
        tapenade = file.read() 
        print(tapenade_der)
        print(tapenade)
        c_code = tapenade.format(tapenade_der, ders_string)
        output_file = open('./tests/utils/runnable_tapenade.c', "w+")
        output_file.write(c_code)
        output_file.close()


def run_tapenade(func, num_params, functions, params_filename, output_filename, runnable_filename):
    if sys.platform.startswith('win'):
        print("running....")
        run_command = "\"utils/program.exe\" " + \
            str(num_params) + " " + \
            str(len(func[1])) + " " + params_filename + " " + output_filename
    else:
        run_command = runnable_filename + " " + \
            str(num_params) + " " + \
            str(len(func[1])) + " " + params_filename + " " + output_filename
    print(run_command)
    run(run_command, stdout=PIPE, stderr=PIPE,
        universal_newlines=True, shell=True)
    return general_utils.parse_output(output_filename)

def compile(runnable_filename):
    if sys.platform.startswith('win'):
        cmd = "cl " + runnable_filename + ".c  /out:utils/program.exe"
    else:
        cmd = "gcc -O3 -ffast-math -o " + runnable_filename + " " + runnable_filename + ".c -lm"
    print(cmd)
    os.system(cmd)
    
