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

sys.path.append('./tests/python_test_utils')
import random, string
import enoki_utils
import pytorch_utils
import wenzel_utils
import us_utils
import generate_function
import tapenade_utils

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
    if os.path.exists(NUMPY_PARAMS_FILENAME):
        os.remove(NUMPY_PARAMS_FILENAME)
    if os.path.exists(PARAMS_FILENAME):
        os.remove(PARAMS_FILENAME)
    if os.path.exists(PYTORCH_FILENAME):
        os.remove(PYTORCH_FILENAME)
    if os.path.exists(PYTORCH_OUTPUT):
        os.remove(PYTORCH_OUTPUT)
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

def generate_graph(avg_us, avg_pytorch, avg_wenzel, denom, func_num, function):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(denom, avg_us,
             denom, avg_pytorch,
             denom, avg_wenzel)
    plt.xticks(denom)
    plt.title('C Code vs Pytorch vs. Wenzel # It: 10')
    # legend
    plt.legend( ('Ours', 'Pytorch', 'Wenzel'),
            shadow=True, loc=(0.01, 0.48), handlelength=1.5, fontsize=16)
    plt.xlabel(function)
    plt.savefig('./tests/results/graph_{}.png'.format(func_num))
    plt.clf()

if __name__ == "__main__":
    functions = []
    alphabets = list(string.ascii_lowercase)
    alphabets.remove('i')

    for k in range(2, 3):
        function = generate_function.gen_other(k)
        functions.append(function)
        print(function)

    INPUT_FILENAME = './tests/utils/functions.c'
    DERIVATIVES_FILENAME = './tests/utils/derivatives'
    RUNNABLE_FILENAME = './tests/utils/static_code/runnable_single'
    OUTPUT_FILENAME = './tests/utils/us_output.txt'
    NUMPY_PARAMS_FILENAME = "./tests/utils/params.npy"
    PARAMS_FILENAME = './tests/utils/params.txt'
    PYTORCH_FILENAME = "./tests/utils/pytorch.py"
    PYTORCH_OUTPUT = "./tests/utils/pytorch_output.txt"
    INIT_NUM_PARAMS = 10
    num_vars = len(functions[0][1])
    NUM_ITERATIONS = 10
    NUM_THREADS_PYTORCH = 1
    RUN_C = True
    WENZEL_COMPILER_VERSION="-5"
    RUNNABLE_TAPENADE = './tests/utils/runnable_tapenade'
    TAPENADE_OUTPUT = './tests/utils/tapenade_output.txt'
    # STATIC = True
    # cleanup()

    output = {}

    for func_num, func in enumerate(functions):

        print(func)

        output[func[0]] = {}

        avg_us = []
        avg_pytorch = []
        avg_wenzel_static = []
        avg_wenzel_dynamic = []
        avg_enoki = []
        denom = []
        num_params = INIT_NUM_PARAMS

        # generate and compile our code
        us_utils.generate_function_c_file(func_num, functions, INPUT_FILENAME)
        us_utils.generate_derivatives_c_file(func_num, functions, INPUT_FILENAME, RUN_C, DERIVATIVES_FILENAME, False, False)
        us_utils.compile_ours(RUN_C, RUNNABLE_FILENAME, DERIVATIVES_FILENAME)

        # generate and compile tapenade code
        tapenade_utils.generate_function_c_file(func_num, functions, './tests/utils/tapenade_func.c')
        tapenade_utils.generate_derivatives_c_file(func_num)
        tapenade_utils.generate_runnable_tapenade(func[1], len(func[1]), func_num)
        tapenade_utils.compile('./tests/utils/runnable_tapenade')



        while num_params <= 100000:

            # generate parameters
            params = generate_params(num_params, func_num)
            print_param_to_file(params)

            # generate pytorch file
            pytorch_utils.generate_pytorch_file(func_num, num_params, functions)

            # generate and compile wenzel code
            enoki_utils.generate_enoki_file(functions, func_num, num_params)
            enoki_utils.compile_enoki()

            wenzel_utils.generate_wenzel_file(func_num, num_params, functions, PARAMS_FILENAME, "single", static=True)
            wenzel_utils.compile_wenzel("single",True, WENZEL_COMPILER_VERSION)
            wenzel_utils.generate_wenzel_file(func_num, num_params, functions, PARAMS_FILENAME, "single", static=False)
            wenzel_utils.compile_wenzel("single", False, WENZEL_COMPILER_VERSION)

            # initialize arrays for run
            our_times = []
            py_times = []
            wenzel_times_static = []
            wenzel_times_dynamic = []
            enoki_times = []
            tapenade_times = []

            for i in range(NUM_ITERATIONS):

                pytorch = pytorch_utils.run_pytorch()
                ours = us_utils.run_ours(functions[func_num], num_params, functions, PARAMS_FILENAME, OUTPUT_FILENAME, RUNNABLE_FILENAME)
                enoki = enoki_utils.run_enoki()
                wenzel_static = wenzel_utils.run_wenzel("single", True)
                wenzel_dynamic = wenzel_utils.run_wenzel("single", False)
                tapenade = tapenade_utils.run_tapenade(functions[func_num], num_params, functions, PARAMS_FILENAME, TAPENADE_OUTPUT, RUNNABLE_TAPENADE)

                print("Pytorch: {}\n Us: {}\n Enoki: {}\n Tapenade: {}\n Wenzel Static: {}\n Wenzel Dynamic: {}".format(pytorch, ours, enoki, tapenade, wenzel_static, wenzel_dynamic))

                # for j in range(len(ours[0])):
                #     assert math.isclose(float(pytorch[0][j]), float(wenzel[0][j]), abs_tol=10**-3)
                #     assert math.isclose(float(wenzel[0][j]), float(ours[0][j]), abs_tol=10**-3)
                    # assert math.isclose(float(ours[0][j]), float(enoki[0][j]), abs_tol=10**-1)
                our_times.append(float(ours[1]))
                py_times.append(float(pytorch[1]))
                enoki_times.append(float(enoki[1]))
                wenzel_times_static.append(float(wenzel_static[1]))
                wenzel_times_dynamic.append(float(wenzel_dynamic[1]))
                tapenade_times.append(float(tapenade[1]))
            
            # print for debug purposes
            print("Parameters: ", params[:10])


            output[func[0]][num_params] = {
                "us": sum(our_times) / len(our_times),
                "pytorch": sum(py_times) / len(py_times),
                "enoki": sum(enoki_times) / len(enoki_times),
                "wenzel_static": sum(wenzel_times_static) / len(wenzel_times_static),
                "wenzel_dynamic": sum(wenzel_times_dynamic) / len(wenzel_times_dynamic),
                "flags": "-ffast-math -O3",
                "tapenade": sum(tapenade_times) / len(tapenade_times),
                "WENZEL_COMPILER_VERSION": WENZEL_COMPILER_VERSION,
                "enoki_speedup": (sum(enoki_times) / len(enoki_times)),
                "wenzel_static_speedup": (sum(wenzel_times_static) / len(wenzel_times_static)),
                "wenzel_dynamic_speedup": (sum(wenzel_times_dynamic) / len(wenzel_times_dynamic)),
                "pytorch_speedup": (sum(py_times) / len(py_times))
            }

            denom.append(num_params)
            if num_params < 10000:
                num_params += 2000
            else:
                num_params = num_params + 10000

    file_suffix = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    output_file = open('./tests/results/grad/full_results_random-{}.json'.format(file_suffix), "w+")
    output_file.write(json.dumps(output, indent=4, sort_keys=True))
    output_file.close()