import os
import general_utils

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

def generate_pytorch_vars(func_num, functions):
    variable_string = ""
    for i, var in enumerate(functions[func_num][1]):
        variable_string += "{} = torch.tensor(np.load('./tests/utils/numpy_params/function_{}_param_{}.npy'), requires_grad=True, dtype=torch.float)".format(var, func_num, var)
        if i != len(functions[func_num][1]) - 1: # if it's the last one, don't include a newline
            variable_string += "\n"
    return variable_string

def generate_pytorch_prints(func_num, functions):
    print_string = ""
    for i, var in enumerate(functions[func_num][1]):
        print_string += "\tprint(str({}_list[i]))\n".format(var)
    return print_string

def generate_pytorch_grads(func_num, functions):
    grad_string = ""
    for var in functions[func_num][1]:
        grad_string += "{}.grad\n".format(var)
    return grad_string

def generate_to_lists(func_num, functions):
    to_list_string = ""
    for var in functions[func_num][1]:
        to_list_string += "{}_list = {}.grad.tolist()\n".format(var, var)
    return to_list_string

def generate_pytorch_file(func_num, num_params, functions):
    with open('./tests/utils/static_code/pytorch.txt', 'r') as file:
        pytorch = file.read()
    pytorch_file = open("./tests/utils/pytorch.py", "w+")
    variables = generate_pytorch_vars(func_num, functions)
    function = parse_pytorch(functions[func_num][0])
    grads = generate_pytorch_grads(func_num, functions)
    to_lists = generate_to_lists(func_num, functions)
    prints = generate_pytorch_prints(func_num, functions)
    pytorch_code = pytorch %  (num_params, variables, function, grads, to_lists, prints)
    pytorch_file.write(pytorch_code)
    pytorch_file.close()
    

def generate_variable(func_num, functions):
    var_str = ""
    for i, var in enumerate(functions[func_num][1]):
        var_str += str(var)
        if i != len(functions[func_num][1]) - 1:
            var_str += ","
    return var_str   

def generate_variable_data(func_num, functions):
    var_data_str = "("
    for i, var in enumerate(functions[func_num][1]):
        var_data_str += "{}.data".format(var)
        if i != len(functions[func_num][1]) - 1:
            var_data_str += ","
    var_data_str += ")"
    return var_data_str  
    
def generate_pytorch_hessian_file(func_num, num_params, functions):
    with open('./tests/utils/static_code/pytorch_hessian.txt', 'r') as file:
        pytorch = file.read()
    pytorch_file = open("./tests/utils/pytorch_hessian.py", "w+")
    num_vars = len(functions[func_num][1])
    variables = generate_pytorch_vars(func_num, functions)
    function = parse_pytorch(functions[func_num][0])
    vars_tensor = generate_variable(func_num, functions)
    vars_data = generate_variable_data(func_num, functions)
    pytorch_code = pytorch %  (num_vars, num_params, variables, vars_tensor, function, vars_data)
    pytorch_file.write(pytorch_code)
    pytorch_file.close()    

def run_pytorch():
    cmd = "python3 " + "./tests/utils/pytorch.py" + " > " + "./tests/utils/pytorch_output.txt"
    os.system(cmd)
    return general_utils.parse_output("./tests/utils/pytorch_output.txt")


def run_pytorch_hessian():
    cmd = "python3 " + "./tests/utils/pytorch_hessian.py" + " > " + "./tests/utils/pytorch_output.txt"
    os.system(cmd)
    return general_utils.parse_output("./tests/utils/pytorch_output.txt")