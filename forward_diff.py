from __future__ import print_function
import sys

from pycparser import parse_file

def differentiate(node):
    # print(show_attrs(node.__class__))
    if node.__class__.__name__ == 'BinaryOp':
        op = node.op
        if (op)=='+':
            print("x=a+b")
        elif (op) == '*':
            print("Mult")
        else:
            print(op)

    elif node.__class__.__name__ == 'FuncCall':
        print(node.name.name)
    return

def show_attrs(node):    
    for attr in dir(node):
        print("-----------------")
        print(attr)
        print(getattr(node,attr))

def get_traversal(fun,x):
    nodes = []
    stack = [fun]
    while stack:
        cur_node = stack[0]

        differentiate(cur_node)
        stack = stack[1:]
        nodes.append(cur_node)

        if 'left' in dir(cur_node):
            stack.append(cur_node.left)
        if 'right' in dir(cur_node):
            stack.append(cur_node.right)
    return 0


def grad(ast, x=0):
    """
    Returns a function which computes gradient of `fun` with respect to
    positional argument number `x`. The returned function takes the 
    same arguments as `fun` , but returns the gradient instead. The function
    `fun` is expected to be scalar valued. The gradient has the same type as argument."""
    assert type(x) in (int, tuple, list), x
    fun = ast.ext[-1].body.block_items[1].init
    fun.show()
    return get_traversal(fun,x)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename  = sys.argv[1]
    else:
        print("Please provide a filename as argument")

    ast = parse_file(filename, use_cpp=True,
            cpp_path='gcc',
            cpp_args=['-E', r'-Iutils/fake_libc_include'])
    # ast.show()
    grad(ast)
