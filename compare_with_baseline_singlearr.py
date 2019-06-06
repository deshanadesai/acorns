import torch
from timeit import default_timer as timer
import os
import numpy as np
from subprocess import PIPE, run
import forward_diff
import numpy as np
import matplotlib.pyplot as plt




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
	cmd = "python3 forward_diff.py " + INPUT_FILENAME + " 'p' -ccode "+ str(RUN_C) + " -ispc "+ str(RUN_ISPC)+" --vars \"" + vars + "\" -func \"function_0\" --output_filename \"" + DERIVATIVES_FILENAME + "\""
	os.system(cmd)
	der_f = open(DERIVATIVES_FILENAME + ".c", "r")
	der_func = der_f.read()
	der_f.close()
	run_f = open(RUNNABLE_FILENAME + ".c", "w")
	if RUN_ISPC:
		include = "#include <math.h>\n#include <stdlib.h>\n#include <time.h>\n#include <stdio.h>\n#include \"objs/derivatives_ispc.h\"\n"
	elif RUN_C:
		include = "#include <math.h>\n#include <stdlib.h>\n#include <time.h>\n#include <stdio.h>\n"

	read_file_func = generate_read_file()
	global_num_params = "#define N " + str(NUM_PARAMS) + "\n"
	main = """\nint main() {
	double values[N];
	double ders[N];
	char variable[] = "params.txt"; 
	read_file_to_array(variable, values);

	struct timespec tstart={0,0}, tend={0,0};
    struct timeval stop, start;
    clock_gettime(CLOCK_MONOTONIC, &tstart);
	
    compute(values, N, ders);


	clock_gettime(CLOCK_MONOTONIC, &tend);
	double delta = ((double)tend.tv_sec + 1.0e-9*tend.tv_nsec) - ((double)tstart.tv_sec + 1.0e-9*tstart.tv_nsec);
    printf("%f ", delta);
	FILE *fp;\n
	"""
	main += "fp = fopen(\""
	main += OUTPUT_FILENAME
	main += "\", \"w+\");\n"
	main += """
    fprintf(fp, "%f ", delta);
	for(int i = 0; i < N; i++) {
        fprintf(fp, "%f ", ders[i]);
    }
	fclose(fp);
	return 0;
}
	"""
	output = include + global_num_params + der_func + read_file_func + main
	run_f.write(output)
	run_f.close()

def generate_read_file():
	return """void read_file_to_array(char* filename, double *args) {
    FILE *file = fopen (filename, "r" );

    if ( file != NULL ) {


    char line [ 200 ]; 
    int i = 0;        

    for(int i=0;i<N;i++){
        fscanf(file, "%lf", &args[i]);
//        printf("%f ", args[i]);
    }

    fclose ( file );
    } else {
    	perror ( filename ); /* why didn't the file open? */
    }
}"""

def generate_params():
	all_params = []
	for func in functions:
		func_params = np.random.rand(NUM_PARAMS, len(func[1])) * 10
		all_params.append(func_params)
	return all_params


def run_pytorch(params):
	torch.set_num_threads(1)
	x = torch.tensor(params[0], requires_grad=True)
	# y = ((x+x)*2 + torch.pow(x,2))*x
	y = ((x*x+3*x)-x/4)/x
	# y = torch.sin(x)*torch.cos(x)+torch.pow(x,2)
	start_time_pytorch = timer()
	y.backward(torch.ones_like(x))
	x.grad
	end_time_pytorch = timer()
	runtime = end_time_pytorch - start_time_pytorch
	return [x.grad, runtime]

def run_ours(params):
	print_param_to_file(params)

	if RUN_ISPC:
		# if target==1:
		cmd = "ispc -O3 --target=sse2 --opt=fast-math derivatives.ispc -o objs/derivatives_ispc.o -h objs/derivatives_ispc.h"
		os.system(cmd)
		cmd = "gcc -O3 -o " + RUNNABLE_FILENAME + " objs/derivatives_ispc.o " + RUNNABLE_FILENAME + ".c" + " -lm"
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
		os.system("gcc " + RUNNABLE_FILENAME + ".c -O3 -o " + RUNNABLE_FILENAME + " -lm")
	run_command = "./" + RUNNABLE_FILENAME  + " " + PARAMS_FILENAME
	result = run(run_command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	f = open(OUTPUT_FILENAME, "r")
	output = f.read()
	output_array = output.split()
	runtime = output_array[0]
	values = output_array[1:]
	return [values, runtime]

def print_param_to_file(params):
	param_string = "\n".join(str(x[0]) for x in params[0])
	param_f = open(PARAMS_FILENAME, "w+")
	param_f.write(param_string)

if __name__ == "__main__":

	RUN_C = False
	RUN_ISPC = True


	# functions = [ ["sin(k)*cos(k)+pow(k,2)", ["k"] ] ]
	functions = [ ["((k*k+3*k)-k/4)/k", ["k"] ] ]
	# functions = [ ["1/4+k*k", ["k"] ] ]
	# functions = [ ["((k+k)*2 + pow(k,2))*k", ["k"] ]] 

	# need to manually change the function in pytorch


	INPUT_FILENAME = "functions.c"
	DERIVATIVES_FILENAME = "derivatives"
	RUNNABLE_FILENAME = "runnable"
	OUTPUT_FILENAME = "output.txt"
	PARAMS_FILENAME = "params.txt"
	OFFSET = "    "
	NUM_PARAMS = 1
	NUM_ITERATIONS = 10	


	RUN_C = True
	RUN_ISPC = False


	'''
	RUN C
	'''
	# params = generate_params()
	avg_us = []
	avg_pytorch = []
	denom = []
	# run_pytorch(params)
	while NUM_PARAMS < 1000000:
		generate_function_c_file()
		generate_runnable_c_file()
		our_times = []
		ispc_times = []
		py_times = []
		for i in range(NUM_ITERATIONS):
			params = generate_params()
			pytorch = run_pytorch(params)
			ours = run_ours(params)
			our_times.append(float(ours[1]))
			py_times.append(float(pytorch[1]))
		print("Parameters: ",params[0][:10])
		print("Snapshot of Our Results:", ours[0][:10])
		print("Snapshot of Pytorch results: ",pytorch[0][:10])

		avg_us.append(sum(our_times) / len(our_times))
		avg_pytorch.append(sum(py_times) / len(py_times))
		denom.append(NUM_PARAMS) 
		NUM_PARAMS = NUM_PARAMS * 10



	'''
	RUN ISPC
	'''


	# params = generate_params()
	avg_ispc = []
	denom = []
	NUM_ITERATIONS = 10	
	NUM_PARAMS = 1
	RUN_C = False
	RUN_ISPC = True
	RUN_ISPC_1 = True
	target = 1
	# run_pytorch(params)
	while NUM_PARAMS < 1000000:
		generate_function_c_file()
		generate_runnable_c_file()
		ispc_times = []
		for i in range(NUM_ITERATIONS):
			params = generate_params()
			ispc_time = run_ours(params)	
			ispc_times.append(float(ispc_time[1]))
		avg_ispc.append(sum(ispc_times) / len(ispc_times))
		denom.append(NUM_PARAMS) 
		NUM_PARAMS = NUM_PARAMS * 10			


	print("Time taken by C code:",our_times)
	print("Time taken by ISPC code: ",ispc_times)
	plt.figure(1)
	plt.subplot(211)
	plt.plot(denom, avg_us)
	plt.plot(denom, avg_ispc)

	plt.plot(denom, avg_pytorch, '--')
	plt.legend(['Us','ISPC target=sse2', 'Pytorch'])
	plt.title('C Code vs Pytorch. # It: '+str(NUM_ITERATIONS))
	plt.savefig('results/graph.png')

	print("Avg Us: " + str(avg_us) )
	print("Avg ISPC: " + str(avg_ispc) )
	print("Avg Pytorch: " + str(avg_pytorch) )



