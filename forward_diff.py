from __future__ import print_function
import sys

from pycparser import parse_file


def grad(fun, x=0):
	"""
	Returns a function which computes gradient of `fun` with respect to
	positional argument number `x`. The returned function takes the 
	same arguments as `fun` , but returns the gradient instead. The function
	`fun` is expected to be scalar valued. The gradient has the same type as argument."""
	assert type(x) in (int, tuple, list), x
	return get_traversal(fun,x)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename  = sys.argv[1]
    else:
        print("Please provide a filename as argument")

    ast = parse_file(filename, use_cpp=True,
            cpp_path='gcc',
            cpp_args=['-E', r'-Iutils/fake_libc_include'])
    ast.show()
    # grad(ast)
