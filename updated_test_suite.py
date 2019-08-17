import sys
import math
import matplotlib.pyplot as plt
import torch
from timeit import default_timer as timer
import os
from subprocess import PIPE, run
import forward_diff
import numpy as np
# matplotlib.use('Agg')


def generate_function_c_file():
    f = open(INPUT_FILENAME, 'w')
    for i in range(len(functions)):
        signature = ""
        if i != 0:
            signature += "\n"
        function = functions[i]
        signature += "int function_" + str(i) + "("
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


def generate_derivatives_c_file():
    vars = ",".join(str(x) for x in functions[0][1])
    cmd = "python3 forward_diff.py " + INPUT_FILENAME + " p -ccode " + str(RUN_C) + " -ispc " + str(
        RUN_ISPC)+" --vars \"" + vars + "\" -func \"function_0\" --output_filename \"" + DERIVATIVES_FILENAME + "\""
    os.system(cmd)


def generate_params(num_params):
    all_params = []
    for func in functions:
        func_params = np.random.rand(num_params*num_vars)
        all_params.append(func_params)
    return all_params


def parse_pytorch(func):
    finalEq = ""
    lastIndex = 0
    stripped = func.strip()
    for i in range(len(stripped)):
        if stripped[i] == "*" or stripped[i] == "/" or stripped[i] == "+" or stripped[i] == "-":
            substring = stripped[lastIndex:i] + stripped[i]
            if "sin" in substring or "cos" in substring or "pow" in substring:
                substring = "torch." + substring
            lastIndex = i + 1
            finalEq += substring
    substring = stripped[lastIndex:]
    if "sin" in substring or "cos" in substring or "pow" in substring:
        substring = "torch." + substring
    finalEq += substring
    return finalEq


def generate_pytorch_file(func_num):
    np.savez(NUMPY_PARAMS_FILENAME, params)
    with open('utils/static_code/pytorch.txt', 'r') as file:
        pytorch = file.read()
    pytorch_file = open("utils/pytorch.py", "w+")
    pytorch_code = pytorch % (parse_pytorch(functions[func_num][0]))
    pytorch_file.write(pytorch_code)
    pytorch_file.close()


def generate_wenzel_file(func_num, params, num_params):
    param_string = ", ".join(str(x) for x in params[0])
    with open('utils/static_code/wenzel.txt', 'r') as file:
        wenzel = file.read()
    wenzel_file = open("utils/wenzel.cpp", "w+")
    cpp_code = wenzel % (num_params, PARAMS_FILENAME, num_params, str(
        functions[func_num][1][0]), str(functions[func_num][0]))
    wenzel_file.write(cpp_code)
    wenzel_file.close()


def compile_wenzel():
    os.system("g++ -std=c++11 -I utils/ext/ utils/wenzel.cpp -o utils/wenzel")


def run_wenzel(num_params):
    os.system("./utils/wenzel utils/wenzel_output.txt")
    return parse_output("utils/wenzel_output.txt", True)


def parse_output(filename, is_wenzel):
    f = open(filename, "r")
    output = f.read()
    output_array = output.split()
    if is_wenzel == True:
        runtime = output_array[-1]
        values = output_array[0:-1]
    else:
        runtime = output_array[0]
        values = output_array[1:]
    return [values, runtime]


def run_pytorch():
    cmd = "python3 " + PYTORCH_FILENAME + " > " + PYTORCH_OUTPUT
    os.system(cmd)
    return parse_output(PYTORCH_OUTPUT, False)


def run_ours(params, func, num_params):
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
    return parse_output(OUTPUT_FILENAME, False)


def compile_ours():
    if RUN_ISPC:
        # if target==1:
        cmd = "ispc -O3 --opt=fast-math utils/derivatives.ispc -o objs/derivatives_ispc.o -h objs/derivatives_ispc.h"
        os.system(cmd)
        cmd = "gcc -O3 -o " + RUNNABLE_FILENAME + " objs/derivatives_ispc.o " + \
            RUNNABLE_FILENAME + ".c" + DERIVATIVES_FILENAME + ".c " + " -lm"
        print(cmd)
        os.system(cmd)
        # if target==2:
        # 	cmd = "ispc -O3 --target=sse4 --opt=fast-math derivatives.ispc -o objs/derivatives_ispc.o -h objs/derivatives_ispc.h"
        # 	os.system(cmd)
        # 	cmd = "gcc -O3 -o " + RUNNABLE_FILENAME + " objs/derivatives_ispc.o " + RUNNABLE_FILENAME + ".c" + " -lm"
        # 	os.system(cmd)
        # if target ==3:
        # 	cmd = "ispc -O3 --target=avx --opt=fast-math derivatives.ispc -o objs/derivatives_ispc.o -h objs/derivatives_ispc.h"
        # 	os.system(cmd)
        # 	cmd = "gcc -O3 -o " + RUNNABLE_FILENAME + " objs/derivatives_ispc.o " + RUNNABLE_FILENAME + ".c" + " -lm"
        # 	os.system(cmd)
    if RUN_C:
        if sys.platform.startswith('win'):
            cmd = "cl " + RUNNABLE_FILENAME + ".c " + UTILS_FILENAME + " " + \
                DERIVATIVES_FILENAME + ".c  /link /out:utils/program.exe"
        else:
            cmd = "gcc -O3 -o " + RUNNABLE_FILENAME + " " + RUNNABLE_FILENAME + \
                ".c " + DERIVATIVES_FILENAME + ".c " + " -lm"
        print(cmd)
        os.system(cmd)


def print_param_to_file(params):
    param_string = "\n".join(str(x) for x in params[0])
    np.save(NUMPY_PARAMS_FILENAME, params[0])
    param_f = open(PARAMS_FILENAME, "w+")
    param_f.write(param_string)
    param_f.close()


def convert_params_to_list(params):
    current_params = []
    for param in params[0]:
        current_params.append(float(param))
    return current_params


if __name__ == "__main__":
    functions = [
        ["((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k", ["k"]]]
    INPUT_FILENAME = 'utils/functions.c'
    DERIVATIVES_FILENAME = 'utils/derivatives'
    UTILS_FILENAME = 'utils/windows_utils.c'
    RUNNABLE_FILENAME = 'utils/runnable'
    OUTPUT_FILENAME = 'utils/output.txt'
    NUMPY_PARAMS_FILENAME = "utils/params.npy"
    PARAMS_FILENAME = 'utils/params.txt'
    PYTORCH_FILENAME = "utils/pytorch.py"
    PYTORCH_OUTPUT = "utils/pytorch_output.txt"
    OFFSET = "    "
    INIT_NUM_PARAMS = 10
    num_vars = len(functions[0][1])
    NUM_ITERATIONS = 10
    NUM_THREADS_PYTORCH = 1
    RUN_C = True
    RUN_ISPC = False

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

    avg_us = []
    avg_pytorch = []
    avg_wenzel = []
    denom = []
    num_params = INIT_NUM_PARAMS

    # generate and compile our code
    generate_function_c_file()
    generate_derivatives_c_file()
    compile_ours()

    while num_params <= 100000:

        # generate parameters
        params = generate_params(num_params)
        print_param_to_file(params)

        # generate other files
        generate_pytorch_file(0)
        generate_wenzel_file(0, params, num_params)
        compile_wenzel()

        # initialize arrays for run
        our_times = []
        py_times = []
        wenzel_times = []

        for i in range(NUM_ITERATIONS):
            pytorch = run_pytorch()
            ours = run_ours(params, functions[0], num_params)
            wenzel = run_wenzel(num_params)
    # 		# for j in range(len(ours[0])):
    # 		# 	assert math.isclose(float(pytorch[0][j]), float(ours[0][j]), abs_tol=10**-1)
            our_times.append(float(ours[1]))
            py_times.append(float(pytorch[1]))
            wenzel_times.append(float(wenzel[1]))
        print("Parameters: ", params[0][: 10])
        print("Snapshot of Our Results:", ours[0][: 10])
        print("Snapshot of Pytorch results: ", pytorch[0][: 10])
        print("Snapshot of Wenzel results: ", wenzel[0][: 10])

        avg_us.append(sum(our_times) / len(our_times))
        avg_pytorch.append(sum(py_times) / len(py_times))
        avg_wenzel.append(sum(wenzel_times) / len(wenzel_times))
        denom.append(num_params)
        if num_params < 10000:
            num_params += 2000
        else:
            num_params = num_params + 10000

    # '''
    # RUN ISPC
    # '''

    # # params = generate_params()
    # avg_ispc = []
    # denom = []
    # NUM_PARAMS = 0
    # RUN_C = False
    # RUN_ISPC = True
    # RUN_ISPC_1 = True
    # target = 1
    # # run_pytorch(params)
    # while NUM_PARAMS <= 100000:
    # 	generate_function_c_file()
    # 	generate_runnable_c_file()
    # 	ispc_times = []
    # 	for i in range(NUM_ITERATIONS):
    # 		params = generate_params()
    # 		ispc_time = run_ours(params)
    # 		ispc_times.append(float(ispc_time[1]))
    # 	avg_ispc.append(sum(ispc_times) / len(ispc_times))
    # 	denom.append(NUM_PARAMS)
    # 	if NUM_PARAMS<10000:
    # 		NUM_PARAMS += 2000
    # 	else:
    # 		NUM_PARAMS = NUM_PARAMS +10000
    print("Time taken by C code:", our_times)
    # print("Time taken by ISPC code: ",ispc
    #
    # _times)
    plt.figure(1)
    plt.subplot(211)
    print(denom)
    plt.plot(denom, avg_us, marker='o')
    # plt.plot(denom, avg_ispc, marker='o')
    plt.plot(denom, avg_pytorch, '--', marker='o')
    plt.plot(denom, avg_wenzel, 'go--', marker='o')
    plt.xticks(denom)
    # plt.legend(['Us','ISPC target=default', 'Pytorch'])
    plt.title('C Code vs Pytorch vs. Wenzel. # It: ' +
              str(NUM_ITERATIONS) + str(torch.__version__))
    plt.savefig('results/graph.png')

    print("Avg Us: " + str(avg_us))
    # print("Avg ISPC: " + str(avg_ispc) )
    print("Avg Pytorch: " + str(avg_pytorch))
    print("Avg Wenzel: " + str(avg_wenzel))