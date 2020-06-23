import sys
import math
import matplotlib.pyplot as plt
import torch
from timeit import default_timer as timer
import os
import json
from subprocess import PIPE, run
import numpy as np
import shutil
from datetime import datetime
import multiprocessing as mp

sys.path.append('./tests/python_test_utils')
import random, string
import us_utils
import generate_function

sys.path.append('./acorns')
import forward_diff

def generate_params(num_params, function_num):
    print("Generating params for function_num", function_num) #, " which is: ", functions[function_num][0])
    num_variables = len(functions[function_num][1])
    function_params = np.zeros(shape=(num_variables, num_params))
    for i, var in enumerate(functions[function_num][1]):
        variable_params = np.random.rand(num_params) * 10
        np.save("./tests/utils/numpy_params/function_{}_param_{}.npy".format(function_num, var), variable_params)
        function_params[i] = variable_params
    reshaped = np.reshape(function_params, num_params*num_variables, order='F')
    param_string = "\n".join(str(x) for x in reshaped)
    param_f = open("./tests/utils/params.txt", "w+")
    param_f.write(param_string)
    param_f.close()
    return reshaped

def print_param_to_file(params):
    param_string = "\n".join(str(x) for x in params)
    param_f = open(PARAMS_FILENAME, "w+")
    param_f.write(param_string)
    param_f.close()

def cleanup():
    if os.path.exists(INPUT_FILENAME):
        os.remove(INPUT_FILENAME)
    if os.path.exists(DERIVATIVES_FILENAME):
        os.remove(DERIVATIVES_FILENAME)
    if os.path.exists(RUNNABLE_FILENAME):
        os.remove(RUNNABLE_FILENAME)
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)
    if os.path.exists(PARAMS_FILENAME):
        os.remove(PARAMS_FILENAME)
    if os.path.exists("./tests/utils/numpy_params"):
        shutil.rmtree("./tests/utils/numpy_params")
        os.mkdir("./tests/utils/numpy_params")
    if os.path.exists("./tests/utils"):
        folder = './tests/utils'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
    if os.path.exists("./tests/results"):
        folder = './tests/results'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    functions = [
            ["(a*a+b*b+c*c+d*d)*(1+1/((a*d-b*c)*(a*d-b*c*e*f*g*h*j*k*l*m*n*o*p*q*r*s*t*u*v*w*x*y*z)))", ["a", "b", "c", "d", "e", "f", "g", "h", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]]
    ]

    INPUT_FILENAME = './tests/utils/functions.c'
    DERIVATIVES_FILENAME = './tests/utils/derivatives'
    RUNNABLE_FILENAME = './tests/utils/static_code/runnable_hessian'
    OUTPUT_FILENAME = './tests/utils/us_output.txt'
    PARAMS_FILENAME = './tests/utils/params.txt'
    num_vars = len(functions[0][1])
    NUM_ITERATIONS = 10
    RUN_C = True

    num_cores_to_use = int(mp.cpu_count())
    print("Using {} cores".format(num_cores_to_use))
    num_cores_as_list = np.arange(1, num_cores_to_use)

    output = {}

    num_params = 100000

    for func_num, func in enumerate(functions):

        print(func)

        output[func[0]] = {}

        avg_us = []
        denom = []
        us_utils.generate_function_c_file(func_num, functions, INPUT_FILENAME)
        for num_cores in num_cores_as_list:

            num_cores_str = str(num_cores)
            print("Using {} threads".format(num_cores_str))

            # generate and compile our code
            us_utils.generate_derivatives_c_file(func_num, functions, INPUT_FILENAME, RUN_C, DERIVATIVES_FILENAME, False, True)
            us_utils.generate_omp_derivatives_c_file('./tests/utils/derivatives.c', num_cores_str)
            us_utils.compile_ours(RUN_C, RUNNABLE_FILENAME, DERIVATIVES_FILENAME)

            # generate parameters
            params = generate_params(num_params, func_num)
            print_param_to_file(params)

            # initialize arrays for run
            our_times = []

            for i in range(NUM_ITERATIONS):
                ours = us_utils.run_ours(functions[func_num], num_params, functions, PARAMS_FILENAME, OUTPUT_FILENAME, RUNNABLE_FILENAME)
                our_times.append(float(ours[1]))


            output[func[0]][num_cores_str] = {
                "us": sum(our_times) / len(our_times),
                "num_params": num_params,
                "num_vars": num_vars
            }

            print(output)

            denom.append(num_cores)

    file_suffix = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    output_file = open('./tests/results/hess/full_results_parallel-{}.json'.format(file_suffix), "w+")
    output_file.write(json.dumps(output, indent=4))
    output_file.close()