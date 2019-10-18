import os
import general_utils

def generate_wenzel_file(func_num, num_params, functions, params_filename):
    with open('utils/static_code/wenzel.txt', 'r') as file:
        wenzel = file.read()
    wenzel_file = open("utils/wenzel.cpp", "w+")
    num_vars = len(functions[func_num][1])
    derivatives = generate_wenzel_ders(func_num, num_vars, functions)
    cpp_code = wenzel % (num_vars, num_vars, num_vars, num_params, num_vars, params_filename, num_vars, derivatives)
    wenzel_file.write(cpp_code)
    wenzel_file.close()

def compile_wenzel():
    os.system("g++-9 -DNDEBUG -std=c++11 -I utils/ext/ utils/wenzel.cpp -o utils/wenzel -ffast-math -O3")

def run_wenzel():
    os.system("utils/wenzel utils/wenzel_output.txt")
    return general_utils.parse_output("utils/wenzel_output.txt")

def generate_wenzel_ders(func_num, num_vars, functions):
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
