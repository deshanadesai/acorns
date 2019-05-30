from __future__ import print_function
import sys
from collections import namedtuple
import math
from pycparser import parse_file
import pycparser.c_ast
import c_generator
import argparse

class Expr(pycparser.c_ast.Node):
    def __init__(self,node):
        if isinstance(node, str):
            # print("Making new node: ")
            # print("New node: ",node)
            self.ast = node
            self.type = 'str'
        else:
            # print("Making a new Expression",node)
            self.ast = node
            print("AST: ",self.ast.show())
            self.type = node.__class__.__name__ 
            print("type: ",self.type)

    def _eval(self):
        if self.type=='BinaryOp':
            return self.eval_match_op()
        elif self.type ==  'FuncCall':
            return self.eval_match_funccall()
        elif self.type == 'str':
            return (self.__variable__(self.ast))._eval()
        elif self.type == 'ID':
            return (self.__variable__(self.ast.name))._eval()            
        elif self.type == 'Constant':
            return (self.__variable__(self.ast.value))._eval()        


    def match_op(self):
        if self.ast.op == '+':
            return (self.__add__())._forward_diff(self)
        elif self.ast.op == '-':
            return (self.__sub__())._forward_diff(self)
        elif self.ast.op == '*':
            return (self.__mul__())._forward_diff(self)
        elif self.ast.op == '/':
            return (self.__truediv__())._forward_diff(self)
        else:
            raise NotImplementedError

    def match_funccall(self):
        func = self.ast.name.name
        # print(func)
        if func == 'pow':
            return (self.__pow__())._forward_diff(self)
        elif func == 'sin':
            return (self.__sin__())._forward_diff(self)
        elif func == 'cos':
            return (self.__cos__())._forward_diff(self)
        else:
            raise NotImplementedError


    def eval_match_op(self):
        if self.ast.op == '+':
            return (self.__add__())._eval(self)
        elif self.ast.op == '-':
            return (self.__sub__())._eval(self)
        elif self.ast.op == '*':
            return (self.__mul__())._eval(self)
        elif self.ast.op == '/':
            return (self.__truediv__())._eval(self)
        else:
            raise NotImplementedError

    def eval_match_funccall(self):
        func = self.ast.name.name
        if func == 'pow':
            return (self.__pow__())._eval(self)
        if func == 'sin':
            return (self.__sin__())._eval(self)
        if func == 'cos':
            return (self.__cos__())._eval(self)                        
        else:
            raise NotImplementedError

    def _forward_diff(self):
        if self.type=='BinaryOp':
            return self.match_op()
        elif self.type ==  'FuncCall':
            return self.match_funccall()
        elif self.type == 'str':
            return (self.__variable__(self.ast))._forward_diff() 
        elif self.type == 'ID':
            return (self.__variable__(self.ast.name))._forward_diff() 
        elif self.type == 'Constant':
            return (self.__variable__(self.ast.value))._forward_diff()


    def __add__(self):
        return Add()

    def __sub__(self):
        return Subtract()

    def __mul__(self):
        return Multiply()

    def __truediv__(self):
        return Divide()

    def __pow__(self):
        return Pow()

    def __sin__(self):
        return Sine()

    def __cos__(self):
        return Cosine()

    def __variable__(self, name):
        # if name == curr_base_variable._get():
        #     return base_vars[0]
        # else:
        print("Making new variable",name)
        return Variable(name)


class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def _eval(self):
        # TODO
        return self.name

    def _forward_diff(self):
        print("Getting derivative for ",self.name, " when base is ",curr_base_variable._get())
        if self.name == curr_base_variable._get():
            return "1"
        else:
            return "0"

    def _get(self):
        return self.name


class Constant(Expr):
    def __init__(self,value):
        self.value = value

    def _eval(self, cache):
        # TODO
        return self.value

    def _forward_diff(self):
        return "0"



class Add(Expr):
    def __init__(self):
        pass

    def _eval(self,cur_node):
        return Expr(cur_node.ast.left).__eval() + " + " + Expr(cur_node.ast.right).__eval()

    def _forward_diff(self,cur_node):
        # print(type(cur_node.ast))
        print("Forward Diff through add")
        cur_node.ast.show()
        print(cur_node.ast.right)
        return Expr(cur_node.ast.left)._forward_diff() + " + " + Expr(cur_node.ast.right)._forward_diff()


class Subtract(Expr):
    def __init__(self):
        print("initiating subtract")
        pass    
    def _eval(self,cur_node):
        return Expr(cur_node.ast.left).__eval() + " - " + Expr(cur_node.ast.right).__eval()

    def _forward_diff(self,cur_node):
        return Expr(cur_node.ast.left)._forward_diff() + " - " + Expr(cur_node.ast.right)._forward_diff()


class Multiply(Expr):
    def __init__(self):
        pass    
    def _eval(self,cur_node):
        # print("printing left tree:",cur_node.ast)
        # print("left eval: ",Expr(cur_node.ast.left).__eval())
        # print("right eval: ",Expr(cur_node.ast.right).__eval())
        return Expr(cur_node.ast.left).__eval() + " * " + Expr(cur_node.ast.right).__eval()

    def _forward_diff(self,cur_node):
        lhs = Expr(cur_node.ast.left)._eval() # Needs to be a string
        rhs = Expr(cur_node.ast.right)._eval()
        return rhs+ " * " +Expr(cur_node.ast.left)._forward_diff() + " + " \
                        + lhs+ " * " +Expr(cur_node.ast.right)._forward_diff()


class Divide(Expr):
    def __init__(self):
        print("initiating divide")
        pass    
    def _eval(self,cur_node):
        return Expr(cur_node.ast.left).__eval() + " / " + Expr(cur_node.ast.right).__eval()

    def _forward_diff(self,cur_node):
        # print("in divide forward:",cur_node.ast)
        lhs = Expr(cur_node.ast.left)._eval()
        # print("lhs: ",lhs)
        rhs = Expr(cur_node.ast.right)._eval()
        return "(" +rhs+ " * " +Expr(cur_node.ast.left)._forward_diff() + " - " \
                        + lhs+ " * " +Expr(cur_node.ast.right)._forward_diff()+")" + "/ " + rhs + " * " + rhs

class Pow(Expr):
    def __init__(self):
        pass    
    def _eval(self,cur_node):
        return "pow" # TODO

    def _forward_diff(self,cur_node):
        base = cur_node.ast.args.exprs[0].name
        exp = cur_node.ast.args.exprs[1].value

        der_base = Expr(base)._forward_diff()
        der_exp = Expr(exp)._forward_diff()

        return "(pow("+base+",("+exp+"-1)) * "+\
                "("+exp+ " * "+ der_base +" + "+base+ " * "+ der_exp+ " * log("+base+")))"


class Sine(Expr):        
    def __init__(self):
        pass    

    def _eval(self,cur_node):
        exp = cur_node.ast.args.exprs[0].name
        return "sin("+Expr(exp)._eval()+")"

    def _forward_diff(self,cur_node):       
        exp = cur_node.ast.args.exprs[0].name
        return "cos("+ exp +")*"+Expr(exp)._forward_diff()


class Cosine(Expr):
    def __init__(self):
        pass    

    def _eval(self,cur_node):
        exp = cur_node.ast.args.exprs[0].name
        return "cos("+Expr(exp)._eval()+")"

    def _forward_diff(self,cur_node):
        exp = cur_node.ast.args.exprs[0].name
        return "-1*sin("+exp +")*"+Expr(exp)._forward_diff()

# def differentiate(node):
#     # print(show_attrs(node.__class__))
#     if node.__class__.__name__ == 'BinaryOp':
#         op = node.op
#         if (op)=='+':
#             print("x=a+b")
#         elif (op) == '*':
#             print("Mult")
#         else:
#             print(op)

#     elif node.__class__.__name__ == 'FuncCall':
#         print(node.name.name)
#     return

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


def grad_without_traversal(ast, x=0):
    """
    Returns a function which computes gradient of `fun` with respect to
    positional argument number `x`. The returned function takes the 
    same arguments as `fun` , but returns the gradient instead. The function
    `fun` is expected to be scalar valued. The gradient has the same type as argument."""
    assert type(x) in (int, tuple, list), x
    global ext_index
    fun = None

    for funs in range(len(ast.ext)):
        if 'decl' not in  dir(ast.ext[funs]):
            continue
        fun_name = ast.ext[funs].decl.name
        if fun_name == parser.func:
            ext_index = funs
            break
    assert fun_name == parser.func

    der_vars = ast.ext[ext_index].decl.type.args.params

    global curr_base_variable
    c_code = c_generator.CGenerator(filename = output_filename, variable_count = len(variables), c_code = ccode, ispc = ispc)
    c_code._make_header()

    # for vars_ in der_vars:
    #     c_code._make_decls(vars_.name)

    # look for function to differentiate.
    for blocks in range(len(ast.ext[ext_index].body.block_items)):
        if 'name' not in dir(ast.ext[ext_index].body.block_items[blocks]):
            continue
        expr_name = ast.ext[ext_index].body.block_items[blocks].name

        if expr_name != expression:
            continue

        fun = ast.ext[ext_index].body.block_items[blocks].init

    assert fun != None

    fun.show()

    for i, vars_ in enumerate(variables):
        c_code._declare_vars(vars_,i)

    for vars_ in variables:
        curr_base_variable = Variable(vars_)
        derivative = Expr(fun)._forward_diff() 
        print(derivative) 
        c_code._generate_expr(curr_base_variable._get(), derivative)

    c_code._make_footer()
        
    # c_code._write(derivative)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('filename', type = str, help='file name')
    parser.add_argument('expr', type = str, help='file name')
    parser.add_argument('-v', '--vars',
                      type=str, action='store',
                      dest='variables',
                      help='Variables to differentiate wrt to')
    parser.add_argument('-func', type = str, dest = 'func', help='function name')
    parser.add_argument('-ccode', type = str, dest = 'ccode', help='function name')
    parser.add_argument('-ispc', type = str, dest = 'ispc', help='function name')

    parser.add_argument('--output_filename', type = str, default ='c_code', help='file name')    
    parser.add_argument('--nth_der', type = int, help='nth derivative')


    parser = parser.parse_args()

    filename = parser.filename
    variables = parser.variables.split(",")
    expression = parser.expr
    output_filename = parser.output_filename

    if parser.ccode == 'True':
        ccode = True
    else:
        ccode = False

    if parser.ispc == 'True':
        ispc = True
    else:
        ispc = False

    print("CCODE: ",ccode)
    print("ISPC CODE: ",ispc)
    ast = parse_file(filename, use_cpp=True,
            cpp_path='gcc',
            cpp_args=['-E', r'-Iutils/fake_libc_include'])

    curr_base_variable = Variable("temp")
    # ast.show()
    ext_index = 0
    grad_without_traversal(ast)
