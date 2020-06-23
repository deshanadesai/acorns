from __future__ import absolute_import
__version__ = '0.0.4'
__all__ = [
    'autodiff', 'unroll_file', 'unroll'
]

from .forward_diff import prepare_graph as prep_graph_ad
from .forward_diff import grad
from .unroll import prepare_graph_from_file, prepare_graph



def autodiff(function, expression, variables, func = 'function', 
                reverse_diff = False, second_der = False, output_filename = 'c_code',
                output_func = 'compute'):

    ast = prep_graph_ad(function)
    grad(ast, expression, variables, func = func, 
        reverse_diff = reverse_diff, second_der = second_der, output_filename = output_filename, 
        output_func = output_func)


def unroll_file(filename, output_filename,  constants = []):
	ast  = prepare_graph_from_file(filename, output_filename, constants_list=constants)
	return ast

def unroll(function, output_filename, constants = []):
	ast = prepare_graph(function, output_filename, constants_list=constants)
	return ast