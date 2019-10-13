import sys
import math
import matplotlib.pyplot as plt
import torch
from timeit import default_timer as timer
import os
from subprocess import PIPE, run
import forward_diff
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
    cmd = "python3 " + "utils/pytorch.py" + " > " + "utils/pytorch_output.txt"
    os.system(cmd)
    return parse_output("utils/pytorch_output.txt")

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
    plt.savefig('results/graph_{}.png'.format(func_num))
    plt.clf()

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
    os.system("g++-9 -std=c++11 -I utils/ext/ utils/wenzel.cpp -o utils/wenzel -ffast-math -O3")

def run_wenzel():
    os.system("./utils/wenzel utils/wenzel_output.txt")
    return parse_output("utils/wenzel_output.txt")

def generate_wenzel_ders(func_num, num_vars):
    ders_string = "\t\tDScalar "
    for i, var in enumerate(functions[func_num][1]):
        ders_string += "{}({}, args[index * {} + {}])".format(var, i, num_vars, i)
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

def generate_enoki_file(func_num, num_params):
    with open('utils/static_code/enoki.txt', 'r') as file:
        enoki = file.read()
    enoki_file = open("utils/enoki.cpp", "w+")

    num_vars = len(functions[func_num][1])

    derivative = functions[func_num][0]
    enoki_init_vars = generate_enoki_init_vars(functions[func_num][1])
    enoki_fill = generate_enoki_fill(functions[func_num][1])
    enoki_us_vars = generate_enoki_us_vars(functions[func_num][1])
    set_requires_grads = generate_set_requires_grads(functions[func_num][1])
    grads = generate_grads(functions[func_num][1])
    print_to_outfile = generate_print_to_outfile(functions[func_num][1])

    param_filename = "params.txt"

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
    cmd = "g++-9 -std=c++17 -I utils/ext/enoki/include/ -I utils/ext/ utils/enoki.cpp -o utils/enoki -ffast-math -O3"
    os.system(cmd)

def run_enoki():
    cmd = "./utils/enoki utils/enoki_output.txt"
    os.system(cmd)
    return parse_output("utils/enoki_output.txt")

if __name__ == "__main__":
    functions = [
        ["((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k*j", ["k", "j"]],
        ["((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k", ["k"]],
        ["sin(k) + cos(k) + pow(k, 2)", ["k"] ]
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
    REVERSE = False
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
        avg_enoki = []
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
            # generate_enoki_file(func_num, num_params)
            # compile_enoki()
            generate_wenzel_file(func_num, num_params)
            compile_wenzel()

            # initialize arrays for run
            our_times = []
            py_times = []
            wenzel_times = []
            enoki_times = []

            for i in range(NUM_ITERATIONS):
                pytorch = run_pytorch()
                ours = run_ours(functions[func_num], num_params)
                # enoki = run_enoki()
                wenzel = run_wenzel()
                # for j in range(len(ours[0])):
                #     assert math.isclose(float(pytorch[0][j]), float(wenzel[0][j]), abs_tol=10**-1)
                #     assert math.isclose(float(wenzel[0][j]), float(ours[0][j]), abs_tol=10**-1)
                #     assert math.isclose(float(ours[0][j]), float(enoki[0][j]), abs_tol=10**-1)
                our_times.append(float(ours[1]))
                py_times.append(float(pytorch[1]))
                # enoki_times.append(float(enoki[1]))
                wenzel_times.append(float(wenzel[1]))

            # print for debug purposes
            print("Parameters: ", params[:10])
            print("Snapshot of Our Results:", ours[0][: 10])
            print("Snapshot of Pytorch results: ", pytorch[0][: 10])
            print("Snapshot of Wenzel results: ", wenzel[0][: 10])
            # print("Snapshot of Enoki results: ", enoki[0][: 10])

            # get the average time
            avg_us.append(sum(our_times) / len(our_times))
            avg_pytorch.append(sum(py_times) / len(py_times))
            # avg_enoki.append(sum(enoki_times) / len(enoki_times))
            avg_wenzel.append(sum(wenzel_times) / len(wenzel_times))
            denom.append(num_params)

            if num_params < 10000:
                num_params += 2000
            else:
                num_params = num_params + 10000
        print("Avg Us: " + str(avg_us))
        print("Avg Pytorch: " + str(avg_pytorch))
        # print("Avg Enoki: " + str(avg_enoki))
        print("Avg Wenzel: " + str(avg_wenzel))   
        generate_graph(avg_us, avg_pytorch, avg_wenzel, denom, func_num, functions[func_num][0])
  
