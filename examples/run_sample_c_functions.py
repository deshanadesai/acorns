import sys, os
import pytest
sys.path.append('../')
import acorns.forward_diff as fd
import glob

print("============== Testing ==============")


output_loc = 'output/sample_c_functions/'
input_loc = 'sample_c_functions/'
if not os.path.exists(output_loc):
	    os.makedirs(output_loc)




c_file = 'basic_expand.c'
print("running for .." ,c_file)

target = "loss"
variables = ['a[0][0]','a[0][1]','a[1][0]','a[1][1]','b[0][0]','b[0][1]','b[1][0]','b[1][1]']


with open(input_loc + c_file,'r') as f:
	c_function = f.read()
ast = fd.prepare_graph(c_function)
basename = os.path.basename(c_file)

	
fd.grad(ast, target, variables, func = 'function_test', output_filename = output_loc+'/'+basename+'_grad_forward',
       output_func = 'compute_grad_forward')
fd.grad(ast, target, variables, func = 'function_test', reverse_diff = True, output_filename = output_loc+'/'+basename+'_grad_reverse',
       output_func = 'compute_grad_reverse')
fd.grad(ast, target, variables, func = 'function_test', second_der = True, output_filename = output_loc+'/'+basename+'_hessian_forward',
       output_func = 'compute_hessian_forward')
# fd.grad(ast, target, variables, func = 'function_test', second_der = True, reverse_diff = True, 
#         output_filename = output_loc+'/'+basename+'_hessian_reverse',  output_func = 'compute_hessian_reverse')




c_file = 'basic_expand1d.c'
print("running for .." ,c_file)

target = "loss[0]"
variables = ['a[0][0]','a[0][1]','a[1][0]','a[1][1]','b[0][0]','b[0][1]','b[1][0]','b[1][1]']


with open(input_loc + c_file,'r') as f:
	c_function = f.read()
ast = fd.prepare_graph(c_function)
basename = os.path.basename(c_file)

	
fd.grad(ast, target, variables, func = 'function_test', output_filename = output_loc+'/'+basename+'_grad_forward',
       output_func = 'compute_grad_forward')
fd.grad(ast, target, variables, func = 'function_test', reverse_diff = True, output_filename = output_loc+'/'+basename+'_grad_reverse',
       output_func = 'compute_grad_reverse')
fd.grad(ast, target, variables, func = 'function_test', second_der = True, output_filename = output_loc+'/'+basename+'_hessian_forward',
       output_func = 'compute_hessian_forward')
# fd.grad(ast, target, variables, func = 'function_test', second_der = True, reverse_diff = True, 
#         output_filename = output_loc+'/'+basename+'_hessian_reverse',  output_func = 'compute_hessian_reverse')





c_file = 'basic_expand2d.c'
print("running for .." ,c_file)

target = "loss[0][0]"
variables = ['a[0][0]','a[0][1]','a[1][0]','a[1][1]','b[0][0]','b[0][1]','b[1][0]','b[1][1]']


with open(input_loc + c_file,'r') as f:
	c_function = f.read()
ast = fd.prepare_graph(c_function)
basename = os.path.basename(c_file)

	
fd.grad(ast, target, variables, func = 'function_test', output_filename = output_loc+'/'+basename+'_grad_forward',
       output_func = 'compute_grad_forward')
fd.grad(ast, target, variables, func = 'function_test', reverse_diff = True, output_filename = output_loc+'/'+basename+'_grad_reverse',
       output_func = 'compute_grad_reverse')
fd.grad(ast, target, variables, func = 'function_test', second_der = True, output_filename = output_loc+'/'+basename+'_hessian_forward',
       output_func = 'compute_hessian_forward')
# fd.grad(ast, target, variables, func = 'function_test', second_der = True, reverse_diff = True, 
#         output_filename = output_loc+'/'+basename+'_hessian_reverse',  output_func = 'compute_hessian_reverse')





c_file = 'basic_simple.c'
print("running for .." ,c_file)

target = "energy"
variables = ['a','p']


with open(input_loc + c_file,'r') as f:
	c_function = f.read()
ast = fd.prepare_graph(c_function)
basename = os.path.basename(c_file)

	
fd.grad(ast, target, variables, func = 'function_test', output_filename = output_loc+'/'+basename+'_grad_forward',
       output_func = 'compute_grad_forward')
fd.grad(ast, target, variables, func = 'function_test', reverse_diff = True, output_filename = output_loc+'/'+basename+'_grad_reverse',
       output_func = 'compute_grad_reverse')
fd.grad(ast, target, variables, func = 'function_test', second_der = True, output_filename = output_loc+'/'+basename+'_hessian_forward',
       output_func = 'compute_hessian_forward')
# fd.grad(ast, target, variables, func = 'function_test', second_der = True, reverse_diff = True, 
#         output_filename = output_loc+'/'+basename+'_hessian_reverse',  output_func = 'compute_hessian_reverse')






c_file = 'decl_array1d.c'
print("running for .." ,c_file)

target = "energy[0]"
variables = ['a','p']


with open(input_loc + c_file,'r') as f:
	c_function = f.read()
ast = fd.prepare_graph(c_function)
basename = os.path.basename(c_file)

	
fd.grad(ast, target, variables, func = 'function_test', output_filename = output_loc+'/'+basename+'_grad_forward',
       output_func = 'compute_grad_forward')
fd.grad(ast, target, variables, func = 'function_test', reverse_diff = True, output_filename = output_loc+'/'+basename+'_grad_reverse',
       output_func = 'compute_grad_reverse')
fd.grad(ast, target, variables, func = 'function_test', second_der = True, output_filename = output_loc+'/'+basename+'_hessian_forward',
       output_func = 'compute_hessian_forward')
# fd.grad(ast, target, variables, func = 'function_test', second_der = True, reverse_diff = True, 
#         output_filename = output_loc+'/'+basename+'_hessian_reverse',  output_func = 'compute_hessian_reverse')






c_file = 'decl_array2d.c'
print("running for .." ,c_file)

target = "energy[0][0]"
variables = ['a','p']


with open(input_loc + c_file,'r') as f:
	c_function = f.read()
ast = fd.prepare_graph(c_function)
basename = os.path.basename(c_file)

	
fd.grad(ast, target, variables, func = 'function_test', output_filename = output_loc+'/'+basename+'_grad_forward',
       output_func = 'compute_grad_forward')
fd.grad(ast, target, variables, func = 'function_test', reverse_diff = True, output_filename = output_loc+'/'+basename+'_grad_reverse',
       output_func = 'compute_grad_reverse')
fd.grad(ast, target, variables, func = 'function_test', second_der = True, output_filename = output_loc+'/'+basename+'_hessian_forward',
       output_func = 'compute_hessian_forward')
# fd.grad(ast, target, variables, func = 'function_test', second_der = True, reverse_diff = True, 
#         output_filename = output_loc+'/'+basename+'_hessian_reverse',  output_func = 'compute_hessian_reverse')


print("=============== Tests successful ==============")
