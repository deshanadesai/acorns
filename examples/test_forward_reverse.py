import sys, os
import pytest
sys.path.append('../')
import acorns
c_function = "int function_test(double p, double a){ \
    int energy = p*p*a+log((p)); \
    return 0; \
}"
if not os.path.exists('output'):
    os.mkdir('output')
acorns.autodiff(c_function, 'energy', ['p'], func = 'function_test', output_filename = 'output/test_grad_forward',
       output_func = 'compute_grad_forward')
acorns.autodiff(c_function, 'energy', ['p'], func = 'function_test', reverse_diff = True, output_filename = 'output/test_grad_reverse',
       output_func = 'compute_grad_reverse')


print("\n\n%========= Run ===========%\n")

if not os.path.exists('output/obj/'):
    os.mkdir('output/obj/')
if not os.path.exists('output/files/'):
    os.mkdir('output/files/')

os.system("gcc -std=c99 -I . -O3 -ffast-math -o output/obj/test_forward_reverse_main test_forward_reverse.c ")
os.system("./output/obj/test_forward_reverse_main")