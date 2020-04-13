import sys
import math
import torch
from timeit import default_timer as timer
import os
import json
from subprocess import PIPE, run
import numpy as np
import shutil
from datetime import datetime
import random, string

sys.path.append('tests/python_test_utils')
import us_utils
import tapenade_utils
import wenzel_utils
import generate_function

sys.path.append('src')
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
    param_f = open("params.txt", "w+")
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
    if os.path.exists(UTILS_FILENAME):
        os.remove(UTILS_FILENAME)
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
    if os.path.exists("utils/numpy_params"):
        shutil.rmtree("utils/numpy_params")
        os.mkdir("utils/numpy_params")
    if os.path.exists("utils"):
        folder = 'utils'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
    if os.path.exists("results"):
        folder = 'results'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    functions = [
    #     # ["(a*a+b*b+c*c+d*d)*(1+1/((a*d-b*c)*(a*d-b*c)))",["a","b","c","d"]],
            ["(a*a+b*b+c*c+d*d)*(1+1/((a*d-b*c)*(a*d-b*c*e*f*g*h*j*k*l*m*n*o*p*q*r*s*t*u*v*w*x*y*z)))", ["a", "b", "c", "d", "e", "f", "g", "h", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]]
    #     ["((k*k+3*k)-k/4)/k+k", ["k"]],
    #     ["((k*k+3*k)-k/4)/k+k*k*k*k+k*k", ["k"]],
    #     ["((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k*j", ["k", "j"]],
    #     ["((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k", ["k"]],
    #     ["sin(k) + cos(k) + pow(k, 2)", ["k"] ]
    ]
    functions = []
    alphabets = list(string.ascii_lowercase)
    alphabets.remove('i')

    for k in range(2, 3):
        function = generate_function.gen_other(k)
        functions.append(function)
        print(function)
    INPUT_FILENAME = './tests/utils/functions.c'
    DERIVATIVES_FILENAME = './tests/utils/derivatives'
    UTILS_FILENAME = './tests/utils/windows_utils.c'
    RUNNABLE_FILENAME = './tests/utils/static_code/runnable_single'
    OUTPUT_FILENAME = './tests/utils/us_output.txt'
    NUMPY_PARAMS_FILENAME = "./tests/utils/params.npy"
    PARAMS_FILENAME = './tests/utils/params.txt'

    PYTORCH_FILENAME = "./tests/utils/pytorch.py"
    PYTORCH_OUTPUT = "./tests/utils/pytorch_output.txt"

    RUNNABLE_TAPENADE = './tests/utils/runnable_tapenade'
    TAPENADE_OUTPUT = './tests/utils/tapenade_output.txt'

    INIT_NUM_PARAMS = 10
    num_vars = len(functions[0][1])
    NUM_ITERATIONS = 10
    NUM_THREADS_PYTORCH = 1
    RUN_C = True
    RUN_ISPC = False
    REVERSE = False
    SECOND_DER = True
    WENZEL_COMPILER_VERSION=""
    STATIC = True
    # cleanup()

    output = {}

    for func_num, func in enumerate(functions):

        print(func)

        output[func[0]] = {}

        num_params = INIT_NUM_PARAMS

        # generate and compile our code
        us_utils.generate_function_c_file(func_num, functions, INPUT_FILENAME)
        us_utils.generate_derivatives_c_file(func_num, functions, INPUT_FILENAME, RUN_C, DERIVATIVES_FILENAME, REVERSE, SECOND_DER)
        us_utils.compile_ours(RUN_C, RUNNABLE_FILENAME, DERIVATIVES_FILENAME)

        # generate and compile tapenade code
        tapenade_utils.generate_function_c_file(func_num, functions, './tests/utils/tapenade_func.c')
        tapenade_utils.generate_derivatives_c_file(func_num)
        tapenade_utils.generate_runnable_tapenade(func[1], len(func[1]), func_num)
        tapenade_utils.compile('./tests/utils/runnable_tapenade')

        while num_params <= 100:

            # generate parameters
            params = generate_params(num_params, func_num)
            print_param_to_file(params)

            wenzel_utils.generate_wenzel_file(func_num, num_params, functions, PARAMS_FILENAME, "single", STATIC)
            wenzel_utils.compile_wenzel("single", STATIC, compiler_version=WENZEL_COMPILER_VERSION)

            # initialize arrays for run
            our_times = []
            wenzel_times = []
            tapenade_times = []

            for i in range(NUM_ITERATIONS):

                ours = us_utils.run_ours(functions[func_num], num_params, functions, PARAMS_FILENAME, OUTPUT_FILENAME, RUNNABLE_FILENAME)
                tapenade = tapenade_utils.run_tapenade(functions[func_num], num_params, functions, PARAMS_FILENAME, TAPENADE_OUTPUT, RUNNABLE_TAPENADE)
                wenzel = wenzel_utils.run_wenzel("single", STATIC)
                
                our_times.append(float(ours[1]))
                tapenade_times.append(float(tapenade[1]))
                wenzel_times.append(float(wenzel[1]))

                assert len(tapenade[0]) == len(ours[0]) == len(wenzel[0])
                
                # for j in range(len(ours[0])):
                    # print("Us: {}, Tapenade: {}".format( float(ours[0][j]), float(tapenade[0][j]) ))
                    # print("Close? {}".format(math.isclose(float(ours[0][j]), float(tapenade[0][j]), abs_tol=10**-1)))
                    # assert math.isclose(float(ours[0][j]), float(tapenade[0][j]), abs_tol=10**-3)

            output[func[0]][num_params] = {
                "us": sum(our_times) / len(our_times),
                "tapenade": sum(tapenade_times) / len(tapenade_times),
                "flags": "-ffast-math -O3",
                "compiler_version": WENZEL_COMPILER_VERSION,
                "wenzel": sum(wenzel_times) / len(wenzel_times),
            }

            if num_params < 10000:
                num_params += 2000
            else:
                num_params = num_params + 10000

    file_suffix = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    output_file = open('./tests/results/grad/full_results-tapenade-{}.json'.format(file_suffix), "w+")
    output_file.write(json.dumps(output, indent=4, sort_keys=True))
    output_file.close()