import torch
from timeit import default_timer as timer
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
NUM_ITERATIONS = 1


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
	global_num_params = "#define N " + str(NUM_PARAMS) + "\n"
	main = """\nint main(int argc, char *argv[]) {
	double **args = malloc(N * sizeof(double *));
	double **ders = malloc(N * sizeof(double *));
	for(int i = 0; i < N; i++) {
   		args[i] = malloc(2 * sizeof(double));
   		ders[i] = malloc(2 * sizeof(double));
	}
	for(int i = 0; i < N; i++) {
		args[i][0] = atof(argv[i+1]);
	}

	struct timespec tstart={0,0}, tend={0,0};
    clock_gettime(CLOCK_MONOTONIC, &tstart);
	struct timeval stop, start;
	compute(args, (long) N, ders);
	clock_gettime(CLOCK_MONOTONIC, &tend);
	double delta = ((double)tend.tv_sec + 1.0e-9*tend.tv_nsec) - ((double)tstart.tv_sec + 1.0e-9*tstart.tv_nsec);
	FILE *fp;\n
	"""
	main += "fp = fopen(\""
	main += OUTPUT_FILENAME
	main += "\", \"w+\");\n"
	main += """
    fprintf(fp, "%f ", delta);
	for(int i = 0; i < N; i++) {
        fprintf(fp, "%f ", ders[i][0]);
    }
	fclose(fp);
	return 0;
}
	"""
	output = include + global_num_params + der_func + main
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
	start_time_pytorch = timer()
	y.backward(torch.ones_like(x))
	x.grad
	end_time_pytorch = timer()
	runtime = end_time_pytorch - start_time_pytorch
	return [x.grad, runtime]

def run_ours(param_string):
	os.system("gcc " + RUNNABLE_FILENAME + ".c -o " + RUNNABLE_FILENAME + " -lm")
	run_command = "./" + RUNNABLE_FILENAME + " " + param_string
	os.system(run_command)
	f = open(OUTPUT_FILENAME, "r")
	output = f.read()
	output_array = output.split()
	runtime = output_array[0]
	values = output_array[1:]
	return [values, runtime]


if __name__ == "__main__":
	generate_function_c_file()
	generate_runnable_c_file()
	our_times = []
	py_times = []
	for i in range(NUM_ITERATIONS):
		params = generate_params()
		param_string = " ".join(str(x[0]) for x in params[0])
		pytorch = run_pytorch(params)
		ours = run_ours(param_string)
		our_times.append(float(ours[1]))
		py_times.append(float(pytorch[1]))
	avg_us = sum(our_times) / len(our_times)
	avg_pytorch = sum(py_times) / len(py_times)
	print("Avg Us: " + str(avg_us) )
	print("Avg Pytorch: " + str(avg_pytorch) )
