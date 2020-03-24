import os
import general_utils

def generate_wenzel_file(func_num, num_params, functions, params_filename, degree, static):
    if static:
        if degree == 'single':
            with open('./tests/utils/static_code/grad/wenzel_single_static.txt', 'r') as file:
                wenzel = file.read()
                wenzel_file = open("./tests/utils/wenzel_single_static.cpp", "w+")
                num_vars = len(functions[func_num][1])
                derivatives = generate_wenzel_ders(func_num, num_vars, functions, degree)
                cpp_code = wenzel % (num_vars, num_params, num_vars, params_filename, num_vars, derivatives)
                wenzel_file.write(cpp_code)
                wenzel_file.close()
        else:
            with open('./tests/utils/static_code/hess/wenzel_hessian_static.txt', 'r') as file:
                wenzel = file.read()  
                wenzel_file = open("./tests/utils/wenzel_hessian_static.cpp", "w+")
                num_vars = len(functions[func_num][1])
                derivatives = generate_wenzel_ders(func_num, num_vars, functions, degree)
                cpp_code = wenzel % (num_vars, num_vars, num_vars, num_params, num_vars, params_filename, num_vars, derivatives)
                wenzel_file.write(cpp_code)
                wenzel_file.close()
    else:
        if degree == 'single':
            with open('./tests/utils/static_code/grad/wenzel_single_dynamic.txt', 'r') as file:
                wenzel = file.read()
                wenzel_file = open("./tests/utils/wenzel_single_dynamic.cpp", "w+")
                num_vars = len(functions[func_num][1])
                derivatives = generate_wenzel_ders(func_num, num_vars, functions, degree)
                cpp_code = wenzel % (num_params, num_vars, params_filename, num_vars, derivatives)
                wenzel_file.write(cpp_code)
                wenzel_file.close()
        else:
            with open('./tests/utils/static_code/hess/wenzel_hessian_dynamic.txt', 'r') as file:
                wenzel = file.read()  
                wenzel_file = open("./tests/utils/wenzel_hessian_dynamic.cpp", "w+")
                num_vars = len(functions[func_num][1])
                derivatives = generate_wenzel_ders(func_num, num_vars, functions, degree)
                cpp_code = wenzel % (num_params, num_vars, params_filename, num_vars, derivatives)
                wenzel_file.write(cpp_code)
                wenzel_file.close()       

def compile_wenzel(degree, static, compiler_version=""):
    if static:
        if degree == 'single':
            os.system("g++{} -std=c++11 -I ./tests/utils/ext/ ./tests/utils/wenzel_single_static.cpp -o ./tests/utils/wenzel_single_static -ffast-math -O3".format(compiler_version))
        else:
            os.system("g++{} -std=c++11 -I ./tests/utils/ext/ ./tests/utils/wenzel_hessian_static.cpp -o ./tests/utils/wenzel_hessian_static -ffast-math -O3".format(compiler_version))
    else:
        if degree == 'single':
            os.system("g++{} -std=c++11 -I ./tests/utils/ext/ ./tests/utils/wenzel_single_dynamic.cpp -o ./tests/utils/wenzel_single_dynamic -ffast-math -O3".format(compiler_version))
        else:
            os.system("g++{} -std=c++11 -I ./tests/utils/ext/ ./tests/utils/wenzel_hessian_dynamic.cpp -o ./tests/utils/wenzel_hessian_dynamic -ffast-math -O3".format(compiler_version))

def run_wenzel(degree, static):
    if static:
        if degree == 'single':
            os.system("./tests/utils/wenzel_single_static ./tests/utils/wenzel_output_single_static.txt")
            return general_utils.parse_output("./tests/utils/wenzel_output_single_static.txt")
        else:
            os.system("./tests/utils/wenzel_hessian_static ./tests/utils/wenzel_output_hessian_static.txt")
            return general_utils.parse_output("./tests/utils/wenzel_output_hessian_static.txt")
    else:
        if degree == 'single':
            os.system("./tests/utils/wenzel_single_dynamic ./tests/utils/wenzel_output_single_dynamic.txt")
            return general_utils.parse_output("./tests/utils/wenzel_output_single_dynamic.txt")
        else:
            os.system("./tests/utils/wenzel_hessian_dynamic ./tests/utils/wenzel_output_hessian_dynamic.txt")
            return general_utils.parse_output("./tests/utils/wenzel_output_hessian_dynamic.txt")

def generate_wenzel_ders(func_num, num_vars, functions, degree):
    ders_string = "\t\tDScalar "
    for i, var in enumerate(functions[func_num][1]):
        ders_string += "{}({}, args[index * {} + {}])".format(var, i, num_vars, i)
        if i == num_vars - 1:
            ders_string += ";\n"
        else:
            ders_string += ", "
    func_string = "\t\tDScalar Fx = {};\n".format(functions[func_num][0])
    grad_string = ""
    if degree == "single":
        for i in range(num_vars):
            grad_string += "\t\tders[index * {} + {}] = Fx.getGradient()({});".format(num_vars, i, i) 
            if i != num_vars - 1:
                grad_string += "\n"
    else:
        num_ders = num_vars * num_vars
        list_ders = list(range(num_ders))
        ders_count = 0
        count = 0
        for i in range(num_vars):
            for j in range(num_vars):
                if j >= i:
                    grad_string += "\t\tders[index * {} + {}] = Fx.getHessian()({});".format(num_ders, count, ders_count) 
                    count += 1
                    list_ders.remove(ders_count)
                    if i != num_ders - 1:
                        grad_string += "\n"
                ders_count += 1
        for i in list_ders:
            grad_string += "\t\tders[index * {} + {}] = Fx.getHessian()({});".format(num_ders, count, i) 
            count += 1
            if i != num_vars - 1:
                grad_string += "\n"
    return ders_string + func_string + grad_string