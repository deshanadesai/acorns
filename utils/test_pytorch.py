import torch
import time
import os
import numpy as np

# k = torch.tensor([1.], requires_grad=True, dtype=torch.float)
# j = torch.tensor([1.], requires_grad=True, dtype=torch.float)
# l = torch.tensor([1.], requires_grad=True, dtype=torch.float)
# torch.set_num_threads(1)
# y = torch.sin(k) + torch.cos(j) + torch.pow(l, 2)
# start_time_pytorch = time.time()
# y.backward(k, j, l)
# end_time_pytorch = time.time()
# runtime = (end_time_pytorch - start_time_pytorch)
# print(" ".join(str(x) for x in k.grad.tolist()))
# print(" ".join(str(x) for x in j.grad.tolist()))
# print(" ".join(str(x) for x in l.grad.tolist()))
# # print( str(runtime) + " " + " ".join(str(x) for x in k.grad.tolist()))

functions = [
    ["sin(k) + cos(j) + pow(l, 2)", ["k", "j", "l"] ] 
    # ["sin(k) + cos(k) + pow(k, 2)", ["k"]],
            ]

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

def generate_params(num_params, function_num):
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
    for var in functions[func_num][1]:
        print_string += "print(str({}_list[i]))\n".format(var)
    return print_string

def generate_pytorch_grads(func_num):
    grad_string = ""
    for var in functions[func_num][1]:
        grad_string += "\ny.backward({}, retain_graph=True)\n".format(var)
        grad_string += "{}.grad".format(var)
    return grad_string

def generate_to_lists(func_num):
    to_list_string = ""
    for var in functions[func_num][1]:
        to_list_string += "\n{}_list = {}.grad.tolist()\n".format(var, var)
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
    param_f = open("test_params.txt", "w+")
    param_f.write(param_string)
    param_f.close()

# params = generate_params(3, 0)

# print("Params:", params)
# reshaped = np.reshape(params, 9, order='F')
# print(reshaped)

# print(generate_pytorch_prints(0))

for i, func in enumerate(functions):
    for num_params in range(1, 5):
        params = generate_params(num_params, i)
        print("Params:", params)
        print_param_to_file(params)
        # generate_pytorch_file(i, num_params)
        # run_pytorch()
