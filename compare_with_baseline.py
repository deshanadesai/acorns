import torch
from timeit import default_timer as timer
import os
import numpy as np
from subprocess import PIPE, run
import forward_diff
import numpy as np
import matplotlib.pyplot as plt

functions = [ ["sin(k)*cos(k)+pow(k,2)", ["k"] ] ]
INPUT_FILENAME = "functions.c"
DERIVATIVES_FILENAME = "derivatives"
RUNNABLE_FILENAME = "runnable"
OUTPUT_FILENAME = "us_output.txt"
PARAMS_FILENAME = "params.txt"
ISPC_C_FILENAME = "ispc.c"
PYTORCH_FILENAME = "pytorch.py"
PYTORCH_OUTPUT = "pytorch_output.txt"
OFFSET = "    "
INIT_NUM_PARAMS = 10
SCALE = 10
MAX_NUM_PARAMS = 10
NUM_ITERATIONS = 1
NUM_THREADS_PYTORCH = 1


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

def generate_runnable_c_file(num_params):
	vars = ",".join(str(x) for x in functions[0][1])
	cmd = "python3 forward_diff.py " + INPUT_FILENAME + " 'p' --vars \"" + vars + "\" -func \"function_0\" --output_filename \"" + DERIVATIVES_FILENAME + "\""
	os.system(cmd)
	ispc_cmd = "ispc " + DERIVATIVES_FILENAME + ".ispc -h " + ISPC_C_FILENAME
	der_f = open(DERIVATIVES_FILENAME + ".c", "r")
	# der_f = open(ISPC_C_FILENAME, "r")
	der_func = der_f.read()
	der_f.close()
	run_f = open(RUNNABLE_FILENAME + ".c", "w")
	include = "#include <math.h>\n#include <stdlib.h>\n#include <time.h>\n#include <stdio.h>\n"
	read_file_func = generate_read_file()
	global_num_params = "#define N " + str(num_params) + "\n"
	main = """\nint main(int argc, char *argv[]) {
	double **args = malloc(N * sizeof(double *));
	double **ders = malloc(N * sizeof(double *));
	for(int i = 0; i < N; i++) {
   		args[i] = malloc(2 * sizeof(double));
   		ders[i] = malloc(2 * sizeof(double));
	}

	read_file_to_array(argv[1], args);
	compute(args, (long) N, ders);
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
	output = include + global_num_params + der_func + read_file_func + main
	run_f.write(output)
	run_f.close()

def generate_read_file():
	return """void read_file_to_array(char* filename, double **args) {
    FILE *file = fopen ( filename, "r" );
    if ( file != NULL ) {
    	char line [ 200 ]; 
   		int i = 0;
    	while ( fgets ( line, sizeof line, file ) != NULL )  {
      		args[i][0] = atof(line);
      		i++;
        }
        fclose ( file );
    } else {
    	perror ( filename ); /* why didn't the file open? */
    }
}"""

def generate_params(num_params):
	all_params = []
	for func in functions:
		func_params = np.random.rand(num_params, len(func[1])) * 10
		all_params.append(func_params)
	return all_params

def parse_pytorch(func):
    finalEq = ""
    lastIndex = 0
    stripped = func.strip()
    for i in range(len(stripped)):
        if stripped[i] == "*" or stripped[i] == "/" or stripped[i] == "+" or stripped[i] == "-":
            substring = stripped[lastIndex:i]
            torched = "torch." + substring + stripped[i]
            lastIndex = i + 1
            finalEq += torched
    substring = stripped[lastIndex:]
    torched = "torch." + substring
    finalEq += torched
    return finalEq

def generate_pytorch_file(func_num, params):
	pytorch_f = open(PYTORCH_FILENAME, "w+")
	importString = "import torch\nimport time\n"
	var = functions[func_num][1][0]
	threads = "torch.set_num_threads(" + str(NUM_THREADS_PYTORCH) + ")\n"
	varString = var + " = torch.tensor(" + str(convert_params_to_list(params)) + ", requires_grad=True)\n"
	print(varString)
	eqString = "y = " + parse_pytorch(functions[func_num][0]) + "\n"
	main = "start_time_pytorch = time.time()\ny.backward(torch.ones_like(" + var + "))\n" + var + ".grad\n"
	main += "end_time_pytorch = time.time()\nruntime = end_time_pytorch - start_time_pytorch\n"
	main += "print( str(runtime) + \" \" + \" \".join(str(x) for x in " + var + ".grad.tolist()))\n"
	output = importString + varString + threads + eqString + main
	pytorch_f.write(output)
	pytorch_f.close()

def run_pytorch():
	cmd = "python3 " + PYTORCH_FILENAME + " > " + PYTORCH_OUTPUT
	os.system(cmd)
	return(parse_output(PYTORCH_OUTPUT))

def parse_output(filename):
	f = open(filename, "r")
	output = f.read()
	output_array = output.split()
	runtime = output_array[0]
	values = output_array[1:]
	return [values, runtime]

def run_ours(params):
	print_param_to_file(params)
	os.system("gcc " + RUNNABLE_FILENAME + ".c -O3 -o " + RUNNABLE_FILENAME + " -lm")
	run_command = "./" + RUNNABLE_FILENAME  + " " + PARAMS_FILENAME
	result = run(run_command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	return(parse_output(OUTPUT_FILENAME))

def print_param_to_file(params):
	param_string = "\n".join(str(x[0]) for x in params)
	param_f = open(PARAMS_FILENAME, "w+")
	param_f.write(param_string)
	param_f.close()

def convert_params_to_list(params):
	current_params = []
	for param in params:
		current_params.append(param[0])
	print(current_params)
	return current_params

if __name__ == "__main__":
	avg_us = []
	avg_pytorch = []
	denom = []
	num_params = INIT_NUM_PARAMS
	while num_params <= MAX_NUM_PARAMS:
		generate_function_c_file()
		generate_runnable_c_file(num_params)
		our_times = []
		py_times = []
		for i in range(NUM_ITERATIONS):
			params = generate_params(num_params)
			generate_pytorch_file(0, params[0])
			pytorch = run_pytorch()
			ours = run_ours(params[0])
			round_ours = " ".join(format(float(x), '.4f') for x in ours[0])
			round_py = " ".join(format(float(x), '.4f') for x in pytorch[0])
			assert(round_ours == round_py, "Values did not match!")
			our_times.append(float(ours[1]))
			py_times.append(float(pytorch[1]))
		avg_us.append(sum(our_times) / len(our_times))
		avg_pytorch.append(sum(py_times) / len(py_times))
		denom.append(num_params) 
		num_params = num_params * SCALE
	plt.figure(1)
	plt.subplot(211)
	plt.plot(denom, avg_us, 'b')
	plt.plot(denom, avg_pytorch, 'r--')
	plt.savefig('graph.png')
	print("Avg Us: " + str(avg_us) )
	print("Avg Pytorch: " + str(avg_pytorch) )
