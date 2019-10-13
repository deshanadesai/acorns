import sys
import math
import matplotlib.pyplot as plt
import torch
from timeit import default_timer as timer
import os
from subprocess import PIPE, run
import numpy as np

def parse_output(filename):
    f = open(filename, "r")
    output = f.read()
    output_array = output.split()
    runtime = output_array[0]
    if len(output_array) > 1:
        values = output_array[1:]
    else:
        values = "No values generated"
    return [values, runtime]

def generate_params(num_params, function_num):
    print("Generating params for function_num", function_num) #, " which is: ", functions[function_num][0])
    num_variables = len(functions[function_num][1])
    function_params = np.zeros(shape=(num_variables, num_params))
    for i, var in enumerate(functions[function_num][1]):
        variable_params = np.random.rand(num_params) * 10
        function_params[i] = variable_params
    reshaped = np.reshape(function_params, num_params*num_variables, order='F')
    param_string = "\n".join(str(x) for x in reshaped)
    param_f = open("params.txt", "w+")
    param_f.write(param_string)
    param_f.close()
    return reshaped

def generate_function_c_file(func_num):
    f = open(INPUT_FILENAME, 'w')
    signature = ""
    function = functions[func_num]
    signature += "int function_" + str(func_num) + "("
    for j in range(len(function[1])):
        var = function[1][j]
        signature += "double " + var
        if j == len(function[1]) - 1:
            signature += ")\n"
        else:
            signature += ", "
    body = "{"
    body += "\n" + OFFSET + "int p = " + function[0] + ";"
    body += "\n" + OFFSET + "return 0;"
    body += "\n}"
    output = signature + body
    f.write(output)
    f.close()

def print_param_to_file(params):
    param_string = "\n".join(str(x) for x in params)
    param_f = open(PARAMS_FILENAME, "w+")
    param_f.write(param_string)
    param_f.close()

def generate_graph(avgs, denom):
    plt.figure(1)
    plt.subplot(211)
    for avg in avgs:
        plt.plot(denom, avg)
    plt.xticks(denom)
    plt.title('C Code vs Pytorch vs. Enoki vs. Wenzel # It: 10')
    # legend
    plt.legend( sympy_functions,
            shadow=True, loc=(0.01, 0.48), handlelength=1.5, fontsize=16)
    plt.xlabel(function)
    plt.savefig('graph_{}.png'.format(func_num))
    plt.clf()

def generate_derivatives_c_file(func_num, sympy_func):
    vars = ",".join(str(x) for x in functions[func_num][1])
    cmd = "python3 sympy_pruning_comparison.py " + INPUT_FILENAME + " p -ccode " + str(RUN_C) + " -reverse " + str(
        REVERSE)+" -second_der "+ str(SECOND_DER)+" --vars \"" + vars + "\" -func \"function_" + str(func_num) + "\" --output_filename \"" + DERIVATIVES_FILENAME + "\" " + "--sympy " + sympy_func
    print(cmd)
    os.system(cmd)

def run_ours(func, num_params):
    if sys.platform.startswith('win'):
        print("running....")
        run_command = "\"utils/program.exe\" " + \
            str(num_params) + " " + \
            str(len(func[1])) + " " + PARAMS_FILENAME + " " + OUTPUT_FILENAME
    else:
        run_command = "./" + RUNNABLE_FILENAME + " " + \
            str(num_params) + " " + \
            str(len(func[1])) + " " + PARAMS_FILENAME + " " + OUTPUT_FILENAME
    print(run_command)
    run(run_command, stdout=PIPE, stderr=PIPE,
        universal_newlines=True, shell=True)
    return parse_output(OUTPUT_FILENAME)

def compile_ours():
    if RUN_C:
        if sys.platform.startswith('win'):
            cmd = "cl " + RUNNABLE_FILENAME + ".c " + UTILS_FILENAME + " " + \
                DERIVATIVES_FILENAME + ".c  /link /out:utils/program.exe"
        else:
            cmd = "gcc-9 -O3 -ffast-math -o " + RUNNABLE_FILENAME + " " + RUNNABLE_FILENAME + \
                ".c " + DERIVATIVES_FILENAME + ".c " + " -lm"
        print(cmd)
        os.system(cmd)

if __name__ == "__main__":
    functions = [
        ["((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k", ["k"]]
    ]

    sympy_functions = ["simplify", "expand", "factor", "collect", "cancel", "none"]
    
    INPUT_FILENAME = 'functions.c'
    DERIVATIVES_FILENAME = 'derivatives'
    RUNNABLE_FILENAME = 'runnable'
    OUTPUT_FILENAME = 'output.txt'
    PARAMS_FILENAME = 'params.txt'
    OFFSET = "    "
    INIT_NUM_PARAMS = 10
    num_vars = len(functions[0][1])
    NUM_ITERATIONS = 10
    NUM_THREADS_PYTORCH = 1
    RUN_C = True
    RUN_ISPC = False
    REVERSE = False
    SECOND_DER = False

    for func_num, func in enumerate(functions):

        avgs = []
        denom = []

        for sympy_func in sympy_functions:

            avg = []
            num_params = INIT_NUM_PARAMS

            # generate and compile our code
            generate_function_c_file(func_num)
            generate_derivatives_c_file(func_num, sympy_func)
            compile_ours()

            while num_params <= 100000:

                # generate parameters
                params = generate_params(num_params, func_num)
                print_param_to_file(params)

                # initialize arrays for run
                run_times = []

                for i in range(NUM_ITERATIONS):
                    output = run_ours(functions[func_num], num_params)
                    run_times.append(float(output[1]))

                # get the average time
                avg.append(sum(run_times) / len(run_times))
                denom.append(num_params)

                if num_params < 10000:
                    num_params += 2000
                else:
                    num_params = num_params + 10000
            avgs.append(avg)
        # generate_graph(avgs)
            # generate_graph(avg_original, avg_pruned, denom, func_num, functions[func_num][0])
    for i, avg in enumerate(avgs):
        print("{}:{}".format(sympy_functions[i], avg[-1]))
    # generate_graph(avgs, denom)
  
