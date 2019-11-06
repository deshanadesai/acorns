import os
import sys
import general_utils
import os
from subprocess import PIPE, run

OFFSET = "    "

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
    body += "\n" + OFFSET + "int p = " + function[0] + ";"
    body += "\n" + OFFSET + "return 0;"
    body += "\n}"
    output = signature + body
    f.write(output)
    f.close()

def generate_derivatives_c_file(func_num, functions, input_filename, run_c, derivatives_filename, reverse, second_der):
    vars = ",".join(str(x) for x in functions[func_num][1])
    cmd = "python3 forward_diff.py " + input_filename + " p -ccode " + str(run_c) + " -reverse " + str(
        reverse)+" -second_der "+ str(second_der)+" --vars \"" + vars + "\" -func \"function_" + str(func_num) + "\" --output_filename \"" + derivatives_filename + "\""
    os.system(cmd)

def run_ours(func, num_params, functions, params_filename, output_filename, runnable_filename):
    if sys.platform.startswith('win'):
        print("running....")
        run_command = "\"utils/program.exe\" " + \
            str(num_params) + " " + \
            str(len(func[1])) + " " + params_filename + " " + output_filename
    else:
        run_command = "./" + runnable_filename + " " + \
            str(num_params) + " " + \
            str(len(func[1])) + " " + params_filename + " " + output_filename
    print(run_command)
    run(run_command, stdout=PIPE, stderr=PIPE,
        universal_newlines=True, shell=True)
    return general_utils.parse_output(output_filename)

def compile_ours(run_c, runnable_filename, utils_filename, derivatives_filename):
    if run_c:
        if sys.platform.startswith('win'):
            cmd = "cl " + runnable_filename + ".c " + utils_filename + " " + \
                derivatives_filename + ".c  /link /out:utils/program.exe"
        else:
            cmd = "gcc -O3 -ffast-math -o " + runnable_filename + " " + runnable_filename + \
                ".c " + derivatives_filename + ".c " + " -lm"
        print(cmd)
        os.system(cmd)