from __future__ import print_function
import sys
from collections import namedtuple
import math
from pycparser import parse_file
import pycparser.c_ast
import c_generator
import argparse

# to do: using pow in reverse dif. might slow down.

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
            # print("AST: ",self.ast.show())
            self.type = node.__class__.__name__ 
            # print("type: ",self.type)

    def eval(self):
        # print("trying to evaluate----")
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


    def match_op(self, reverse = False,  adjoint = None, grad = {}):
        # print("Matching operation",self.ast.op)
        if reverse:
            if self.ast.op == '+':
                    return (self.__add__())._reverse_diff(self, adjoint, grad)
            elif self.ast.op == '-':
                return (self.__sub__())._reverse_diff(self, adjoint, grad)
            elif self.ast.op == '*':
                # print("trying to multiply")            
                return (self.__mul__())._reverse_diff(self, adjoint, grad)
            elif self.ast.op == '/':
                return (self.__truediv__())._reverse_diff(self, adjoint, grad)
            else:
                raise NotImplementedError
        else:
            if self.ast.op == '+':
                return (self.__add__())._forward_diff(self)
            elif self.ast.op == '-':
                return (self.__sub__())._forward_diff(self)
            elif self.ast.op == '*':
                # print("trying to multiply")            
                return (self.__mul__())._forward_diff(self)
            elif self.ast.op == '/':
                return (self.__truediv__())._forward_diff(self)
            else:
                raise NotImplementedError

    def match_funccall(self, reverse = False,  adjoint = None, grad = {}):
        func = self.ast.name.name
        print(func)

        if reverse:
            if func == 'pow':
                return (self.__pow__())._reverse_diff(self, adjoint, grad)
            elif func == 'sin':
                return (self.__sin__())._reverse_diff(self, adjoint, grad)
            elif func == 'cos':
                return (self.__cos__())._reverse_diff(self, adjoint, grad)
            else:
                raise NotImplementedError
        else:
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



    def _reverse_diff(self, adjoint, grad):
        if self.type=='BinaryOp':
            return self.match_op(reverse = True, adjoint = adjoint, grad = grad)
        elif self.type ==  'FuncCall':
            return self.match_funccall(reverse = True, adjoint = adjoint, grad = grad)
        elif self.type == 'str':
            return (self.__variable__(self.ast))._reverse_diff(adjoint, grad) 
        elif self.type == 'ID':
            return (self.__variable__(self.ast.name))._reverse_diff(adjoint, grad) 
        elif self.type == 'Constant':
            return (self.__variable__(self.ast.value))._reverse_diff(adjoint, grad)            


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
        # print("Making new variable",name)
        return Variable(name)


class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def _eval(self):
        # TODO
        return self.name

    def _forward_diff(self):
        if self.name == curr_base_variable._get():
            return "1"
        else:
            return "0"

    # adjoint: str variable. grad: dict type (str, str)
    def _reverse_diff(self, adjoint, grad):
        grad[self.name] = grad[self.name]+ " + "+ adjoint

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

    def _reverse_diff(self):
        pass



class Add(Expr):
    def __init__(self):
        pass

    def _eval(self,cur_node):
        # print("evaluating through addition, left nodes are: ",cur_node.ast.left)
        # print("evaluating through addition, right nodes are: ",cur_node.ast.right)
        # print(Expr(cur_node.ast.left).eval())
        # print("Addition evaluation of: ")
        # cur_node.ast.show()

        temp= "("+Expr(cur_node.ast.left).eval() + " + " + Expr(cur_node.ast.right).eval()+")"
        # print(temp)
        return temp

    def _forward_diff(self,cur_node):
        # print(type(cur_node.ast))
        # print("Forward Diff through add")
        # cur_node.ast.show()
        # print(cur_node.ast.right)
        # print("right value will be: ",Expr(cur_node.ast.right)._forward_diff())
        return "(" + "(" + Expr(cur_node.ast.left)._forward_diff()+")" + " + " + "("+Expr(cur_node.ast.right)._forward_diff()+")"+")"

    def _reverse_diff(self, cur_node, adjoint, grad):
        Expr(cur_node.ast.left)._reverse_diff(adjoint, grad)
        Expr(cur_node.ast.right)._reverse_diff(adjoint, grad)




class Subtract(Expr):
    def __init__(self):
        # print("initiating subtract")
        pass    
    def _eval(self,cur_node):
        return "("+Expr(cur_node.ast.left).eval() + " - " + Expr(cur_node.ast.right).eval()+")"

    def _forward_diff(self,cur_node):
        return "(" + "(" + Expr(cur_node.ast.left)._forward_diff()+")" + " - " + "("+Expr(cur_node.ast.right)._forward_diff()+")"+")"


    def _reverse_diff(self, cur_node, adjoint, grad):
        Expr(cur_node.ast.left)._reverse_diff(adjoint, grad)
        Expr(cur_node.ast.right)._reverse_diff("-" + adjoint, grad)



class Multiply(Expr):
    def __init__(self):
        pass    
    def _eval(self,cur_node):
        # print("evaluating multiplication, printing left tree:",cur_node.ast)
        # print("left eval: ",Expr(cur_node.ast.left).eval())
        # print("right eval: ",Expr(cur_node.ast.right).eval())
        return "("+Expr(cur_node.ast.left).eval() + " * " + Expr(cur_node.ast.right).eval()+")"

    def _forward_diff(self,cur_node):
        lhs = Expr(cur_node.ast.left).eval() # Needs to be a string
        rhs = Expr(cur_node.ast.right).eval()
        # print("multiplication evaluation of: ")
        # cur_node.ast.show() 
        # print("left:",lhs)
        # print("Right:",rhs)       

        return "(" + rhs+ " * " + "("+Expr(cur_node.ast.left)._forward_diff()+")" + " + " \
                        + lhs+ " * " + "("+Expr(cur_node.ast.right)._forward_diff() +")" +")" 

    def _reverse_diff(self, cur_node, adjoint, grad):
        lhs = Expr(cur_node.ast.left).eval()
        rhs = Expr(cur_node.ast.right).eval()
        Expr(cur_node.ast.left)._reverse_diff("("+ adjoint + ")" + "*" + "("+ rhs + ")", grad)
        Expr(cur_node.ast.right)._reverse_diff("("+ adjoint + ")" + "*" + "("+ lhs + ")", grad)


class Divide(Expr):
    def __init__(self):
        pass    
    def _eval(self,cur_node):
        return "("+Expr(cur_node.ast.left).eval() + " / " + Expr(cur_node.ast.right).eval()+")"

    def _forward_diff(self,cur_node):
        # print("in divide forward:",cur_node.ast)
        lhs = Expr(cur_node.ast.left).eval()
        # print("lhs: ",lhs)
        rhs = Expr(cur_node.ast.right).eval()
        return "(" +rhs+ " * " +Expr(cur_node.ast.left)._forward_diff() + " - " \
                        + lhs+ " * " +Expr(cur_node.ast.right)._forward_diff()+")" + "/ (" + rhs + " * " + rhs+")"

    def _reverse_diff(self, cur_node, adjoint, grad):
        lhs = Expr(cur_node.ast.left).eval()
        rhs = Expr(cur_node.ast.right).eval()
        Expr(cur_node.ast.left)._reverse_diff("("+ adjoint + ")" + "/" + "("+ rhs + ")", grad)
        Expr(cur_node.ast.right)._reverse_diff("(-("+adjoint +") * ("+ lhs + "))/" + "pow(("+ rhs + "),2)", grad)        





class Pow(Expr):
    def __init__(self):
        pass    
    def _eval(self,cur_node):
        # print("evaluation of: ")
        # cur_node.ast.show()
        base = cur_node.ast.args.exprs[0].name
        exp = cur_node.ast.args.exprs[1].value        
        return "(pow(%s,%s))" % (Expr(base).eval(),exp) # TODO

    def _forward_diff(self,cur_node):
        base = cur_node.ast.args.exprs[0].name
        exp = cur_node.ast.args.exprs[1].value

        der_base = Expr(base)._forward_diff()
        der_exp = Expr(exp)._forward_diff()

        return "(pow("+base+",("+exp+"-1)) * "+\
                "("+exp+ " * "+ der_base +" + "+base+ " * "+ der_exp+ " * log("+base+")))"


    def _reverse_diff(self, cur_node, adjoint, grad):
        base = cur_node.ast.args.exprs[0].name
        exp = cur_node.ast.args.exprs[1].value
        Expr(base)._reverse_diff( "(" + adjoint + ")"+ "*"+ "("+ exp+")"+" * " + "(pow(" + base +","+ (exp - 1)+"))", grad)
        Expr(exp)._reverse_diff("(" +  adjoint + ")"+ "*"+ "log("+base+")" +" * " + "pow(" + base +"," + exp +")", grad)


class Sine(Expr):        
    def __init__(self):
        pass    

    def _eval(self,cur_node):
        exp = cur_node.ast.args.exprs[0].name
        return "(sin("+Expr(exp).eval()+"))"

    def _forward_diff(self,cur_node):       
        exp = cur_node.ast.args.exprs[0].name
        return "(cos("+ exp +")*"+Expr(exp)._forward_diff()+")"


    # def _reverse_diff(self, cur_node, adjoint, grad):



class Cosine(Expr):
    def __init__(self):
        pass    

    def _eval(self,cur_node):
        exp = cur_node.ast.args.exprs[0].name
        return "(cos("+Expr(exp).eval()+"))"

    def _forward_diff(self,cur_node):
        exp = cur_node.ast.args.exprs[0].name
        return "(-1*sin("+exp +")*"+Expr(exp)._forward_diff()+")"

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
    # fun.show()
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

    # fun.show()

    grad = {}
    for i, vars_ in enumerate(variables):
        c_code._declare_vars(vars_,i)
        grad[vars_] = ''

    print(grad)

    # Expr(fun)._reverse_diff("1.",grad) 
    # print(grad)
    for i,vars_ in enumerate(variables):
        curr_base_variable = Variable(vars_)
        derivative = Expr(fun)._forward_diff() 
        print(derivative) 
        c_code._generate_expr(curr_base_variable._get(), derivative,index=i)

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
