import torch
import time
import os
import numpy as np

import forward_diff

functions = [ ["sin(k)*cos(k)+pow(k,2)", ["k"] ] ]
INPUT_FILENAME = "functions.c"
DERIVATIVES_FILENAME = "derivatives"
RUNNABLE_FILENAME = "runnable"
OUTPUT_FILENAME = "output.txt"
OFFSET = "    "
NUM_PARAMS = 1000


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
		body = "{\n"
		body += OFFSET + "unsigned int long c = 4;"
		body += "\n" + OFFSET + "int p = " + function[0] + ";"
		body += "\n" + OFFSET + "return 0;"
		body += "\n}"
		output = signature + body
		f.write(output)
	f.close()

def generate_runnable_c_file():
	vars = ",".join(str(x) for x in functions[0][1])
	cmd = "python3 forward_diff.py " + INPUT_FILENAME + " 'p' --vars \"" + vars + "\" -func \"function_0\" --output_filename \"" + DERIVATIVES_FILENAME + "\""
	os.system(cmd)
	der_f = open(DERIVATIVES_FILENAME + ".c", "r")
	der_func = der_f.read()
	der_f.close()
	run_f = open(RUNNABLE_FILENAME + ".c", "w")
	include = "#include <math.h>\n#include <stdlib.h>\n#include <time.h>\n#include <stdio.h>\n"
	# global_args = "double args[argc-1][2];"
	# global_ders = "double ders[" + str(NUM_PARAMS + "][2];"
	main = """\nint main(int argc, char *argv[]) {
	double args[argc-1][2];
	for(int i = 1; i < argc; i++) {
		args[i-1][0] = atof(argv[i]);
	}
		long num_points = ((int) (sizeof (args) / sizeof (args)[0]));\n
	"""
	main += "double ders[" + str(NUM_PARAMS) + "][2];\n"
	main += """
	struct timeval stop, start;
	gettimeofday(&start, NULL);
	long long start_ms = (((long long)start.tv_sec)*1000)+(start.tv_usec/1000);
	compute(args, num_points, ders);
	gettimeofday(&stop, NULL);
	long long stop_ms = (((long long)stop.tv_sec)*1000)+(stop.tv_usec/1000);
	printf("start: %lu", start_ms);
	printf("stop: %lu", stop_ms);
	long long delta = stop_ms - start_ms;
	FILE *fp;\n
	"""
	main += "fp = fopen(\""
	main += OUTPUT_FILENAME
	main += "\", \"w+\");\n"
	main += """
    fprintf(fp, "%lu ", delta);
	for(int i = 0; i < ( (int) sizeof(ders) / sizeof(ders[0]) ); i++) {
        fprintf(fp, "%f ", ders[i][0]);
    }
	fclose(fp);
	return 0;
}
	"""
	output = include + der_func + main
	run_f.write(output)
	run_f.close()



def generate_params():
	all_params = []
	for func in functions:
		func_params = np.random.rand(NUM_PARAMS, len(func[1])) * 10
		all_params.append(func_params)
	return all_params


def run_pytorch(params):
	x = torch.tensor(params[0], requires_grad=True)
	y = torch.sin(x)*torch.cos(x)+torch.pow(x,2)
	start_time_pytorch = time.time()
	y.backward(torch.ones_like(x))
	x.grad
	end_time_pytorch = time.time()
	runtime = end_time_pytorch - start_time_pytorch
	return [x.grad, runtime]

def run_ours(param_string):
	os.system("gcc " + RUNNABLE_FILENAME + ".c -o " + RUNNABLE_FILENAME + " -lm")
	run_command = "./" + RUNNABLE_FILENAME + " " + param_string
	start_time_us = time.time()
	os.system(run_command)
	end_time_us = time.time()
	runtime = end_time_us - start_time_us
	print(runtime)
	f = open(OUTPUT_FILENAME, "r")
	output = f.read()
	output_array = output.split()
	# time = output_array[0]
	values = output_array[1:]
	return [values, runtime]


if __name__ == "__main__":
	params = generate_params()
	generate_function_c_file()
	generate_runnable_c_file()
	param_string = " ".join(str(x[0]) for x in params[0])
	pytorch = run_pytorch(params)
	ours = run_ours(param_string)
	print(pytorch[1])
	print(ours[1])