import torch
from timeit import default_timer as timer
import os
from subprocess import PIPE, run
import forward_diff
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import sys

def generate_function_c_file():
	f = open(INPUT_FILENAME,'w')
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
	cmd = "python forward_diff.py " + INPUT_FILENAME + " p -ccode "+ str(RUN_C) + " -ispc "+ str(RUN_ISPC)+" --vars \"" + vars + "\" -func \"function_0\" --output_filename \"" + DERIVATIVES_FILENAME + "\""
	os.system(cmd)

def generate_params(num_params):
	all_params = []
	for func in functions:
		func_params = np.random.rand(num_params*num_vars) * 10
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
	pytorch_f = open(PYTORCH_FILENAME, "w+")
	importString = "import torch\nimport time\nimport numpy as np\n\n"
	var = functions[func_num][1][0]
	threads = "torch.set_num_threads(" + str(NUM_THREADS_PYTORCH) + ")\n"
	varString = var + " = torch.tensor(np.load('" + NUMPY_PARAMS_FILENAME + "'), requires_grad=True)\n"
	eqString = "y = " + parse_pytorch(functions[func_num][0]) + "\n"
	main = "start_time_pytorch = time.time()\ny.backward(torch.ones_like(" + var + "))\n" + var + ".grad\n"
	main += "end_time_pytorch = time.time()\nruntime = end_time_pytorch - start_time_pytorch\n"
	main += "print( str(runtime) + \" \" + \" \".join(str(x) for x in " + var + ".grad.tolist()))\n"
	output = importString + varString + threads + eqString + main
	pytorch_f.write(output)
	pytorch_f.close()

def parse_output(filename):
	f = open(filename, "r")
	output = f.read()
	output_array = output.split()
	runtime = output_array[0]
	values = output_array[1:]
	return [values, runtime]

def run_pytorch():
	cmd = "python " + PYTORCH_FILENAME + " > " + PYTORCH_OUTPUT
	os.system(cmd)
	return(parse_output(PYTORCH_OUTPUT))

def run_ours(params, func, num_params):
	if sys.platform.startswith('win'):
		print("running....")
		run_command = "\"utils/program.exe\" " + str(num_params) + " " +  str(len(func[1])) + " " + PARAMS_FILENAME + " " + OUTPUT_FILENAME
	else:
		run_command = "./" + RUNNABLE_FILENAME + " "  + str(num_params) + " " +  str(len(func[1])) + " " + PARAMS_FILENAME + " " + OUTPUT_FILENAME
	print(run_command)
	run(run_command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	f = open(OUTPUT_FILENAME, "r")
	output = f.read()
	output_array = output.split()
	runtime = output_array[0]
	values = output_array[1:]
	return [values, runtime]

def compile_code():
    if RUN_ISPC:
        # if target==1:
        cmd = "ispc -O3 --opt=fast-math utils/derivatives.ispc -o objs/derivatives_ispc.o -h objs/derivatives_ispc.h"
        os.system(cmd)
        cmd = "gcc-5 -O3 -o " + RUNNABLE_FILENAME + " objs/derivatives_ispc.o " + RUNNABLE_FILENAME + ".c" + DERIVATIVES_FILENAME + ".c " + " -lm"
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
            cmd = "cl " + RUNNABLE_FILENAME + ".c " + UTILS_FILENAME + " " + DERIVATIVES_FILENAME + ".c  /link /out:utils/program.exe"
        else:
            cmd = "gcc-5 -O3 -o " + RUNNABLE_FILENAME + " " + RUNNABLE_FILENAME + ".c " + DERIVATIVES_FILENAME + ".c " + " -lm"
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
    # functions = [ ["sin(k)*cos(k)+pow(k,2)", ["k"] ] ]
    # # 	functions = [ ["((k*k+3*k)-k/4)/k+k*k*k*k", ["k"] ] ]
    functions = [ ["((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k", ["k"] ] ]
    # functions = [ ["((k+k)*2 + pow(k,2))*k", ["k"] ]] 
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

    avg_us = []
    avg_pytorch = []
    denom = []
    num_params = INIT_NUM_PARAMS

    # generate and compile our code
    generate_function_c_file()
    generate_derivatives_c_file()
    compile_code()
    
    while num_params <= 100000:

        # generate parameters 
        params = generate_params(num_params)
        print_param_to_file(params)

        # generate pytorch file
        generate_pytorch_file(0)

        #initialize arrays for run
        our_times = []
        py_times = []
        
        for i in range(NUM_ITERATIONS):
            pytorch = run_pytorch()
            ours = run_ours(params, functions[0], num_params)
	# 		# for j in range(len(ours[0])):
	# 		# 	assert math.isclose(float(pytorch[0][j]), float(ours[0][j]), abs_tol=10**-1)   			
            our_times.append(float(ours[1]))
            py_times.append(float(pytorch[1]))
        print("Parameters: ",params[0][:10])
        print("Snapshot of Our Results:", ours[0][:10])
        print("Snapshot of Pytorch results: ",pytorch[0][:10])
        
        avg_us.append(sum(our_times) / len(our_times))
        avg_pytorch.append(sum(py_times) / len(py_times))
        denom.append(num_params) 
        if num_params<10000:
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
    print("Time taken by C code:",our_times)
    # print("Time taken by ISPC code: ",ispc
    # 
    # _times)
    plt.figure(1)
    plt.subplot(211)
    print(denom)
    plt.plot(denom, avg_us, marker='o')
	# plt.plot(denom, avg_ispc, marker='o')
    
    plt.plot(denom, avg_pytorch, '--', marker='o')
    plt.xticks(denom)    
	# plt.legend(['Us','ISPC target=default', 'Pytorch'])
    plt.title('C Code vs Pytorch. # It: '+str(NUM_ITERATIONS))
    plt.savefig('results/graph.png')
    
    print("Avg Us: " + str(avg_us) )
	# print("Avg ISPC: " + str(avg_ispc) )
    print("Avg Pytorch: " + str(avg_pytorch) )



