import sys
import math
import matplotlib.pyplot as plt
import torch
from timeit import default_timer as timer
import os
from subprocess import PIPE, run
import forward_diff
import numpy as np

def parse_output(filename, is_wenzel):
    f = open(filename, "r")
    output = f.read()
    output_array = output.split()
    runtime = output_array[0]
    values = output_array[1:]
    return [values, runtime]

def generate_params(num_params, function_num):
    print("Generating params for function_num", function_num) #, " which is: ", functions[function_num][0])
    num_variables = len(functions[function_num][1])
    function_params = np.zeros(shape=(num_variables, num_params))
    for i, var in enumerate(functions[function_num][1]):
        variable_params = np.random.rand(num_params) * 10
        np.save("utils/numpy_params/function_{}_param_{}.npy".format(function_num, var), variable_params)
        function_params[i] = variable_params
    reshaped = np.reshape(function_params, num_params*num_variables, order='F')
    param_string = "\n".join(str(x) for x in reshaped)
    param_f = open("params.txt", "w+")
    param_f.write(param_string)
    param_f.close()
    return reshaped

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
    finalEq = "(" + finalEq + ").sum()"
    return finalEq

def generate_pytorch_vars(func_num):
    variable_string = ""
    for i, var in enumerate(functions[func_num][1]):
        variable_string += "{} = torch.tensor(np.load('utils/numpy_params/function_{}_param_{}.npy'), requires_grad=True, dtype=torch.float)".format(var, func_num, var)
        if i != len(functions[func_num][1]) - 1: # if it's the last one, don't include a newline
            variable_string += "\n"
    return variable_string

def generate_pytorch_prints(func_num):
    print_string = ""
    for i, var in enumerate(functions[func_num][1]):
        print_string += "\tprint(str({}_list[i]))\n".format(var)
    return print_string

def generate_pytorch_grads(func_num):
    grad_string = ""
    for var in functions[func_num][1]:
        grad_string += "{}.grad\n".format(var)
    return grad_string

def generate_to_lists(func_num):
    to_list_string = ""
    for var in functions[func_num][1]:
        to_list_string += "{}_list = {}.grad.tolist()\n".format(var, var)
    return to_list_string

def generate_pytorch_file(func_num, num_params):
    with open('utils/static_code/pytorch.txt', 'r') as file:
        pytorch = file.read()
    pytorch_file = open("utils/pytorch.py", "w+")
    num_vars = len(functions[func_num][1])
    variables = generate_pytorch_vars(func_num)
    function = parse_pytorch(functions[func_num][0])
    grads = generate_pytorch_grads(func_num)
    to_lists = generate_to_lists(func_num)
    prints = generate_pytorch_prints(func_num)
    pytorch_code = pytorch %  (num_params, variables, function, grads, to_lists, prints)
    pytorch_file.write(pytorch_code)
    pytorch_file.close()

def run_pytorch():
    cmd = "python3 " + "utils/pytorch.py" + " > " + "pytorch_output.txt"
    os.system(cmd)
    return parse_output("pytorch_output.txt", False)

def print_param_to_file(params):
    param_string = "\n".join(str(x) for x in params)
    param_f = open(PARAMS_FILENAME, "w+")
    param_f.write(param_string)
    param_f.close()

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

def generate_derivatives_c_file(func_num):
    vars = ",".join(str(x) for x in functions[func_num][1])
    cmd = "python3 forward_diff.py " + INPUT_FILENAME + " p -ccode " + str(RUN_C) + " -reverse " + str(
        REVERSE)+" -second_der "+ str(SECOND_DER)+" --vars \"" + vars + "\" -func \"function_" + str(func_num) + "\" --output_filename \"" + DERIVATIVES_FILENAME + "\""
    os.system(cmd)

# def plot_graph(avg_us, avg_pytorch, avg_wenzel, denom):
#     plt.figure(1)
#     plt.subplot(211)
#     print(denom)
#     plt.plot(denom, avg_us, marker='o')
#     plt.plot(denom, avg_pytorch, '--', marker='o')
#     # # # plt.plot(denom, avg_wenzel, 'go--', marker='o')
#     plt.xticks(denom)
#     plt.title('C Code vs Pytorch vs. Wenzel. # It: ' +
#             str(NUM_ITERATIONS) + str(torch.__version__))
#     plt.savefig('results/graph_{}.png'.format(func_num))
#     plt.clf()
#     print("Avg Us: " + str(avg_us))
#     print("Avg Pytorch: " + str(avg_pytorch))
#     # # print("Avg Wenzel: " + str(avg_wenzel))

def generate_wenzel_file(func_num, num_params):
    with open('utils/static_code/wenzel.txt', 'r') as file:
        wenzel = file.read()
    wenzel_file = open("utils/wenzel.cpp", "w+")
    num_vars = len(functions[func_num][1])
    derivatives = generate_wenzel_ders(func_num, num_vars)
    cpp_code = wenzel % (num_params, num_vars, PARAMS_FILENAME, derivatives)
    wenzel_file.write(cpp_code)
    wenzel_file.close()

def compile_wenzel():
    os.system("g++ -std=c++11 -I utils/ext/ utils/wenzel.cpp -o utils/wenzel")

def run_wenzel(num_params):
    os.system("./utils/wenzel utils/wenzel_output.txt")
    return parse_output("utils/wenzel_output.txt", True)

def generate_wenzel_ders(func_num, num_vars):
    ders_string = "\t\tDScalar "
    for i, var in enumerate(functions[func_num][1]):
        ders_string += "{}(0, args[index * {} + {}])".format(var, num_vars, i)
        if i == num_vars - 1:
            ders_string += ";\n"
        else:
            ders_string += ", "
    func_string = "\t\tDScalar Fx = {};\n".format(functions[func_num][0])
    grad_string = ""
    for i, var in enumerate(functions[func_num][1]):
        grad_string += "\t\tders[index * {} + {}] = Fx.getGradient()({});".format(num_vars, i, i) 
        if i != num_vars - 1:
            grad_string += "\n"
    return ders_string + func_string + grad_string

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
    return parse_output(OUTPUT_FILENAME, False)

def compile_ours():
    if RUN_C:
        if sys.platform.startswith('win'):
            cmd = "cl " + RUNNABLE_FILENAME + ".c " + UTILS_FILENAME + " " + \
                DERIVATIVES_FILENAME + ".c  /link /out:utils/program.exe"
        else:
            cmd = "gcc -O3 -ffast-math -o " + RUNNABLE_FILENAME + " " + RUNNABLE_FILENAME + \
                ".c " + DERIVATIVES_FILENAME + ".c " + " -lm"
        print(cmd)
        os.system(cmd)

if __name__ == "__main__":
    # functions = [
    #     ["((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k", ["k"]],
    #     ["((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k*j", ["k", "j"]]
    #     ]
    functions = [
        ["((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k", ["k"]]

    # ["a+a*a*b*c*d*1/(a+b+c+d)+a*b*c*c*c*c*c+(a-b)*(c-d)+(a-b)/(c-d)+d*d*d*c/((a+b-c)*(a+d-c+b))*k+1/k-1/(k+l)", ["k", "l", "a", "b", "c", "d"] ]
    # ["sin(k) + cos(k) + pow(k, 2)", ["k"] ]
            ]

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
    REVERSE = True
    SECOND_DER = False

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

    for func_num, func in enumerate(functions):

        avg_us = []
        avg_pytorch = []
        avg_wenzel = []
        denom = []
        num_params = INIT_NUM_PARAMS

        # generate and compile our code
        generate_function_c_file(func_num)
        generate_derivatives_c_file(func_num)
        compile_ours()

        while num_params <= 100000:

            # generate parameters
            params = generate_params(num_params, func_num)
            print_param_to_file(params)

            # generate pytorch file
            generate_pytorch_file(func_num, num_params)

            # generate and compile wenzel code
            # generate_wenzel_file(func_num, num_params)
            # compile_wenzel()

            # initialize arrays for run
            our_times = []
            py_times = []
            wenzel_times = []

            for i in range(NUM_ITERATIONS):
                pytorch = run_pytorch()
                ours = run_ours(functions[func_num], num_params)
                # wenzel = run_wenzel(num_params)
                # for j in range(len(ours[0])):
                #     assert math.isclose(float(pytorch[0][j]), float(ours[0][j]), abs_tol=10**-1)
                our_times.append(float(ours[1]))
                py_times.append(float(pytorch[1]))
                # wenzel_times.append(float(wenzel[1]))

            # print for debug purposes
            # print("Parameters: ", params[0][: 10])
            print("Snapshot of Our Results:", ours[0][: 10])
            print("Snapshot of Pytorch results: ", pytorch[0][: 10])
            # print("Snapshot of Wenzel results: ", wenzel[0][: 10])

            # get the average time
            avg_us.append(sum(our_times) / len(our_times))
            avg_pytorch.append(sum(py_times) / len(py_times))
            # avg_wenzel.append(sum(wenzel_times) / len(wenzel_times))
            denom.append(num_params)

            if num_params < 10000:
                num_params += 2000
            else:
                num_params = num_params + 10000
        print("Avg Us: " + str(avg_us))
        print("Avg Pytorch: " + str(avg_pytorch))
        # print("Avg Wenzel: " + str(avg_wenzel))     
