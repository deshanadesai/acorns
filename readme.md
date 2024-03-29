### Readme


### About acorns

Home: https://github.com/deshanadesai/acorns

Package license: MIT

Feedstock license: BSD 3-Clause

Current Version: 3.0 - Fixes bugs and supports features described in the [user guide](https://github.com/deshanadesai/acorns/blob/master/doc/ACORNS_user_guide.pdf)

Summary: An easy-to-use Code Generator for Gradients and Hessians

ACORNS is an algorithm for automatic differention of algorithms written in a subset of C99 code and its efficient implementation as a Python script.

### Installation

Installing acorns from the conda-forge channel can be achieved by adding conda-forge to your channels with:

`conda config --add channels conda-forge`

Once the conda-forge channel has been enabled, acorns can be installed with:

`conda install acorns`

### Usage

Please refer to the `examples/` directory and the `basic_example.ipynb` for more examples. Here is a basic usage of the package:


```
import acorns

    
c_function = "int function_test(double a, double p){ \
    double energy = a*a*a*a*p+1/(p*p) - 1/p * p/a; \
    return 0; \
}"

acorns.autodiff(c_function, 'energy', ['a','p'], func = 'function_test', output_filename = 'test_grad_forward',
       output_func = 'compute_grad_forward')
```

### Examples directory:

1. `c_code_basic.py` - basic examples of forward and reverse, single and double autodifferentiation

2. `c_code_basic_parallel.py` - example of including parallel for loops

3. `c_code_basic_split.py` - example script for splitting derivatives into multiple files

4. `run_sample_c_functions.py` - runs sample functions from the `examples/sample_functions/` directory, includes single and double dimensional array examples

5. For unrolling - example input  `examples/unrolled_example.c` and output code `examples/unrolled_example_output.c` along with differentiation of the output code `examples/unrolled_example_fd_output.c` are provided.

### Known problems

- Support for nested loops is limited to two.
- Does not currently support complicated data structures.

Please refer to the user guide for further reading: [user guide](https://github.com/deshanadesai/acorns/blob/master/doc/ACORNS_user_guide.pdf)
### Package Contents:

***README.rst:***
  This README file.
  
***LICENSE:***
  MIT
  
***setup.py:***
  Installation script
  
***examples/:***
  A directory with some examples of using Acorns
  
***acorns/:***
  The acorns module source code.
  



