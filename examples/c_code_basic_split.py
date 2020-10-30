import sys, os
import pytest
sys.path.append('../')
import acorns

    
c_function = "int function_test(double a, double p, double g, double h, double f, double t){ \
    double energy = a*a*a*a*p+1/(p*p) - 1/p * p/a +t*a +h/f*h + (f*f*g)/t; \
    return 0; \
}"


if not os.path.exists('output_split'):
    os.mkdir('output_split')

acorns.autodiff(c_function, 'energy', ['a','p', 'g', 'h', 'f', 't'], func = 'function_test', second_der = True, output_filename = 'output_split/test_hessian_forward',
       output_func = 'compute_hessian_forward', split = True, split_by = 3)
acorns.autodiff(c_function, 'energy', ['a','p', 'g', 'h', 'f', 't'], func = 'function_test', second_der = True, reverse_diff = True, 
        output_filename = 'output_split/test_hessian_reverse',  output_func = 'compute_hessian_reverse', split = True, split_by = 4)


