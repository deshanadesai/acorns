import sys, os
import pytest
sys.path.append('../')
import acorns

    
c_function = "int function_test(double a, double p){ \
    double energy = a*a*a*a*p+1/(p*p) - 1/p * p/a; \
    return 0; \
}"


if not os.path.exists('output'):
    os.mkdir('output')
acorns.autodiff(c_function, 'energy', ['a','p'], func = 'function_test', output_filename = 'output/test_grad_forward',
       output_func = 'compute_grad_forward')
acorns.autodiff(c_function, 'energy', ['a','p'], func = 'function_test', reverse_diff = True, output_filename = 'output/test_grad_reverse',
       output_func = 'compute_grad_reverse')
acorns.autodiff(c_function, 'energy', ['a','p'], func = 'function_test', second_der = True, output_filename = 'output/test_hessian_forward',
       output_func = 'compute_hessian_forward')
acorns.autodiff(c_function, 'energy', ['a','p'], func = 'function_test', second_der = True, reverse_diff = True, 
        output_filename = 'output/test_hessian_reverse',  output_func = 'compute_hessian_reverse')

print("\n\n%========= Run ===========%\n")

if not os.path.exists('output/obj/'):
    os.mkdir('output/obj/')
if not os.path.exists('output/files/'):
    os.mkdir('output/files/')

os.system("gcc -std=c99 -I . -O3 -ffast-math -o output/obj/c_code_basic_main c_code_basic_main.c ")
os.system("./output/obj/c_code_basic_main")

print("\n\n%=========== Testing ===========%\n")

file = open("./output/files/compute_grad_forward.txt", "r")
expected = open("./expected_ccode_basic/compute_grad_forward.txt", "r")
assert file.read() == expected.read()


file = open("./output/files/compute_grad_reverse.txt", "r")
expected = open("./expected_ccode_basic/compute_grad_reverse.txt", "r")
assert file.read() == expected.read()

file = open("./output/files/compute_hess_forward.txt", "r")
expected = open("./expected_ccode_basic/compute_hess_forward.txt", "r")
assert file.read() == expected.read()

file = open("./output/files/compute_hess_reverse.txt", "r")
expected = open("./expected_ccode_basic/compute_hess_reverse.txt", "r")
assert file.read() == expected.read()

print("Complete")
