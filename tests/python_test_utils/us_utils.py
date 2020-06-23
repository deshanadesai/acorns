import os
import sys
import general_utils
import os
from subprocess import PIPE, run

def generate_function_c_file(func_num, functions, input_filename):
    f = open(input_filename, 'w')
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
    body += "\n\tint p = " + function[0] + ";"
    body += "\n\treturn 0;"
    body += "\n}"
    output = signature + body
    f.write(output)
    f.close()

def generate_derivatives_c_file(func_num, functions, input_filename, run_c, derivatives_filename, reverse, second_der):
    vars = ",".join(str(x) for x in functions[func_num][1])
    reverse_string = ""
    if reverse:
        reverse_string += " --reverse "
    second_der_string = ""
    if second_der:
        second_der_string += " --second_der "
    cmd = "python3 acorns/forward_diff.py " + input_filename + " p " + reverse_string + second_der_string +" --vars \"" + vars + "\" --func \"function_" + str(func_num) + "\" --output_filename \"" + derivatives_filename + "\""
    os.system(cmd)

def generate_omp_derivatives_c_file(filename, num_threads):
    with open(filename) as file:
        c_code = file.read()
        c_code = "#include <omp.h>\n" + c_code.replace("{", "{\n\tomp_set_dynamic(0);\n\tomp_set_num_threads(NUM_THREADS);\n\t#pragma omp parallel for\n", 1)
        c_code = c_code.replace("NUM_THREADS", num_threads)
        output_file = open(filename, "w+")
        output_file.write(c_code)
        output_file.close()

def run_ours(func, num_params, functions, params_filename, output_filename, runnable_filename):
    if sys.platform.startswith('win'):
        print("running....")
        run_command = "\"utils/program.exe\" " + \
            str(num_params) + " " + \
            str(len(func[1])) + " " + params_filename + " " + output_filename
    else:
        run_command = runnable_filename + " " + \
            str(num_params) + " " + \
            str(len(func[1])) + " " + params_filename + " " + output_filename
    print(run_command)
    run(run_command, stdout=PIPE, stderr=PIPE,
        universal_newlines=True, shell=True)
    return general_utils.parse_output(output_filename)

def compile_ours(run_c, runnable_filename, derivatives_filename):
    if run_c:
        if sys.platform.startswith('win'):
            cmd = "cl " + runnable_filename + ".c " + derivatives_filename + ".c  /link /out:utils/program.exe"
        else:
            cmd = "gcc -O3 -ffast-math -o " + runnable_filename + " " + runnable_filename + \
                ".c " + derivatives_filename + ".c -lm -fopenmp"
        print(cmd)
        os.system(cmd)