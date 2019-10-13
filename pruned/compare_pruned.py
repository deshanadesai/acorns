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

def print_param_to_file(params):
    param_string = "\n".join(str(x) for x in params)
    param_f = open(PARAMS_FILENAME, "w+")
    param_f.write(param_string)
    param_f.close()

def generate_graph(avg_us, avg_pytorch, avg_enoki, avg_wenzel, denom, func_num, function):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(denom, avg_us,
             denom, avg_pytorch,
             denom, avg_enoki,
             denom, avg_wenzel)
    plt.xticks(denom)
    plt.title('C Code vs Pytorch vs. Enoki vs. Wenzel # It: 10')
    # legend
    plt.legend( ('Ours', 'Pytorch', 'Enoki', 'Wenzel'),
            shadow=True, loc=(0.01, 0.48), handlelength=1.5, fontsize=16)
    plt.xlabel(function)
    plt.savefig('results/graph_{}.png'.format(func_num))
    plt.clf()

def run_original(func, num_params):
    run_command = "./run_original " + \
        str(num_params) + " " + \
        str(len(func[1])) + " " + PARAMS_FILENAME + " " + OG_OUTPUT_FILENAME
    print(run_command)
    run(run_command, stdout=PIPE, stderr=PIPE,
        universal_newlines=True, shell=True)
    return parse_output(OG_OUTPUT_FILENAME)

def run_pruned(func, num_params):
    run_command = "./run_pruned " + \
        str(num_params) + " " + \
        str(len(func[1])) + " " + PARAMS_FILENAME + " " + P_OUTPUT_FILENAME
    print(run_command)
    run(run_command, stdout=PIPE, stderr=PIPE,
        universal_newlines=True, shell=True)
    return parse_output(P_OUTPUT_FILENAME)

if __name__ == "__main__":
    functions = [
        ["((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k", ["k"]]
    ]

    RUNNABLE_FILENAME = 'runnable'
    OG_OUTPUT_FILENAME = 'original_output.txt'
    P_OUTPUT_FILENAME = 'pruned_output.txt'
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

        avg_original = []
        avg_pruned = []
        denom = []
        num_params = INIT_NUM_PARAMS

        while num_params <= 100000:

            # generate parameters
            params = generate_params(num_params, func_num)
            print_param_to_file(params)

            # initialize arrays for run
            original_times = []
            pruned_times = []

            for i in range(NUM_ITERATIONS):
                original = run_original(functions[func_num], num_params)
                pruned = run_pruned(functions[func_num], num_params)
                original_times.append(float(original[1]))
                pruned_times.append(float(pruned[1]))

            # get the average time
            avg_original.append(sum(original_times) / len(original_times))
            avg_pruned.append(sum(pruned_times) / len(pruned_times))
            denom.append(num_params)

            if num_params < 10000:
                num_params += 2000
            else:
                num_params = num_params + 10000
        print("Avg Original: " + str(avg_original))
        print("Avg Pruned: " + str(avg_pruned))
        # generate_graph(avg_original, avg_pruned, denom, func_num, functions[func_num][0])
  
