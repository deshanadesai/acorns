from __future__ import print_function
import sys
from collections import namedtuple
import math
from pycparser import parse_file
from pycparser import c_parser
import pycparser.c_ast
import acorns.c_generator as c_generator
import argparse
import numpy as np
import pycparser.c_parser as c_parser

# to do: using pow in reverse dif. might slow down.

class Expr(pycparser.c_ast.Node):
    def __init__(self,node):
        if isinstance(node, str):
            self.ast = node
            self.type = 'str'
        else:
            self.ast = node
            self.type = node.__class__.__name__

    def eval(self):
        if self.type=='UnaryOp':
            return self.eval_match_op()
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
        elif self.type == 'ArrayRef':
            if self.ast.name.__class__.__name__ == 'ArrayRef':
                return (self.__variable__(self.ast.name.name.name+'[{}]'.format(self.ast.name.subscript.value), self.ast.subscript.value))._eval() 
            else:
                if self.ast.subscript.__class__.__name__ == 'BinaryOp' or self.ast.subscript.__class__.__name__ == 'ID':
                    return (self.__variable__(self.ast.name.name, Expr(self.ast.subscript).eval()))._eval() 
                else:
                    return (self.__variable__(self.ast.name.name, self.ast.subscript.value))._eval() 


    def match_op(self, reverse = False,  adjoint = None, grad = {}):
        if reverse:
            if self.ast.op == '+':
                    return (self.__add__())._reverse_diff(self, adjoint, grad)
            elif self.ast.op == '-':
                return (self.__sub__())._reverse_diff(self, adjoint, grad)
            elif self.ast.op == '*':
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
                return (self.__mul__())._forward_diff(self)
            elif self.ast.op == '/':
                return (self.__truediv__())._forward_diff(self)
            else:
                raise NotImplementedError

    def match_funccall(self, reverse = False,  adjoint = None, grad = {}):
        func = self.ast.name.name

        if reverse:
            if func == 'pow':
                return (self.__pow__())._reverse_diff(self, adjoint, grad)
            elif func == 'sin':
                return (self.__sin__())._reverse_diff(self, adjoint, grad)
            elif func == 'cos':
                return (self.__cos__())._reverse_diff(self, adjoint, grad)
            elif func == 'log':
                return (self.__log__())._reverse_diff(self, adjoint, grad)
            else:
                raise NotImplementedError
        else:
            if func == 'pow':
                return (self.__pow__())._forward_diff(self)
            elif func == 'sin':
                return (self.__sin__())._forward_diff(self)
            elif func == 'cos':
                return (self.__cos__())._forward_diff(self)
            elif func == 'log':
                return (self.__log__())._forward_diff(self)
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
        elif func == 'sin':
            return (self.__sin__())._eval(self)
        elif func == 'cos':
            return (self.__cos__())._eval(self)
        elif func == 'log':
            return (self.__log__())._eval(self)
        else:
            raise NotImplementedError

    def _forward_diff(self):
        if self.type=='BinaryOp' or self.type=='UnaryOp':
            return self.match_op()
        elif self.type ==  'FuncCall':
            return self.match_funccall()
        elif self.type == 'str':
            return (self.__variable__(self.ast))._forward_diff()
        elif self.type == 'ID':
            return (self.__variable__(self.ast.name))._forward_diff()
        elif self.type == 'Constant':
            return (self.__variable__(self.ast.value))._forward_diff()
        elif self.type == 'ArrayRef':
            if self.ast.name.__class__.__name__ == 'ArrayRef':
                return (self.__variable__(self.ast.name.name.name+'[{}]'.format(self.ast.name.subscript.value), self.ast.subscript.value))._forward_diff() 
            else:
                if self.ast.subscript.__class__.__name__ == 'BinaryOp' or self.ast.subscript.__class__.__name__ == 'ID':
                    return (self.__variable__(self.ast.name.name, Expr(self.ast.subscript).eval()))._forward_diff() 
                else:
                    return (self.__variable__(self.ast.name.name, self.ast.subscript.value))._forward_diff() 




    def _reverse_diff(self, adjoint, grad):
        if self.type=='BinaryOp' :
            return self.match_op(reverse = True, adjoint = adjoint, grad = grad)
        elif self.type ==  'FuncCall':
            return self.match_funccall(reverse = True, adjoint = adjoint, grad = grad)
        elif self.type == 'str':
            return (self.__variable__(self.ast))._reverse_diff(adjoint, grad)
        elif self.type == 'ID':
            return (self.__variable__(self.ast.name))._reverse_diff(adjoint, grad)
        elif self.type == 'Constant':
            return (self.__variable__(self.ast.value))._reverse_diff(adjoint, grad)     
        elif self.type == 'ArrayRef':  
            if self.ast.name.__class__.__name__ == 'ArrayRef':      
                return (self.__variable__(self.ast.name.name.name+'[{}]'.format(self.ast.name.subscript.value), self.ast.subscript.value))._reverse_diff(adjoint, grad) 
            else:
                if self.ast.subscript.__class__.__name__ == 'BinaryOp' or self.ast.subscript.__class__.__name__ == 'ID':
                    return (self.__variable__(self.ast.name.name, Expr(self.ast.subscript).eval()))._reverse_diff(adjoint, grad) 
                else:
                    return (self.__variable__(self.ast.name.name, self.ast.subscript.value))._reverse_diff(adjoint, grad) 
                   


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

    def __log__(self):
        return Log()

    def __variable__(self, name, subscript=None):
        return Variable(name, subscript)


class Variable(Expr):
    def __init__(self, name, subscript=None):
        if subscript is not None:
            self.name = name+ "[{}]".format(str(subscript))
        else:
            self.name = name

    def _eval(self, subscript=None):
        # TODO
        return self.name

    def _forward_diff(self):
        if self.name == curr_base_variable._get():
            return "1"
        else:
            return "0"

    # adjoint: str variable. grad: dict type (str, str)
    def _reverse_diff(self, adjoint, grad):
        if self.name not in grad:
            pass
        elif grad[self.name] == '0':
            grad[self.name] = adjoint
        else:
            grad[self.name] = grad[self.name]+ " + "+ adjoint

    def _get(self):
        return self.name


class Constant(Expr):
    def __init__(self,value):
        self.value = value

    def _eval(self, cache):
        return self.value

    def _forward_diff(self):
        return "0"

    def _reverse_diff(self, adjoint, grad):
        pass



class Add(Expr):
    def __init__(self):
        pass

    def _eval(self,cur_node):
        if cur_node.type == 'UnaryOp':
            return "("+Expr(cur_node.ast.expr).eval()+")"
        temp= "("+Expr(cur_node.ast.left).eval() + " + " + Expr(cur_node.ast.right).eval()+")"
        return temp

    def _forward_diff(self,cur_node):
        if cur_node.type == 'UnaryOp':
            return "("+Expr(cur_node.ast.expr)._forward_diff()+")"
        return "(" + "(" + Expr(cur_node.ast.left)._forward_diff()+")" + " + " + "("+Expr(cur_node.ast.right)._forward_diff()+")"+")"

    def _reverse_diff(self, cur_node, adjoint, grad):
        Expr(cur_node.ast.left)._reverse_diff(adjoint, grad)
        Expr(cur_node.ast.right)._reverse_diff(adjoint, grad)





class Subtract(Expr):
    def __init__(self):
        pass
    def _eval(self,cur_node):
        if cur_node.type == 'UnaryOp':
            return "( -("+Expr(cur_node.ast.expr).eval()+"))"
        return "("+Expr(cur_node.ast.left).eval() + " - " + Expr(cur_node.ast.right).eval()+")"

    def _forward_diff(self,cur_node):
        if cur_node.type == 'UnaryOp':
            return "(-("+Expr(cur_node.ast.expr)._forward_diff()+"))"
        return "(" + "(" + Expr(cur_node.ast.left)._forward_diff()+")" + " - " + "("+Expr(cur_node.ast.right)._forward_diff()+")"+")"


    def _reverse_diff(self, cur_node, adjoint, grad):
        Expr(cur_node.ast.left)._reverse_diff(adjoint, grad)
        Expr(cur_node.ast.right)._reverse_diff("-1*(" + adjoint+")", grad)



class Multiply(Expr):
    def __init__(self):
        pass
    def _eval(self,cur_node):
        return "("+Expr(cur_node.ast.left).eval() + " * " + Expr(cur_node.ast.right).eval()+")"

    def _forward_diff(self,cur_node):
        lhs = Expr(cur_node.ast.left).eval() # Needs to be a string
        rhs = Expr(cur_node.ast.right).eval()

        return "(" + rhs+ " * " + "("+Expr(cur_node.ast.left)._forward_diff()+")" + " + " \
                        + lhs+ " * " + "("+Expr(cur_node.ast.right)._forward_diff() +")" +")"

    def _reverse_diff(self, cur_node, adjoint, grad):
        lhs = Expr(cur_node.ast.left).eval()
        rhs = Expr(cur_node.ast.right).eval()
        Expr(cur_node.ast.left)._reverse_diff("(("+ adjoint + ")" + "*" + "("+ rhs + "))", grad)
        Expr(cur_node.ast.right)._reverse_diff("(("+ adjoint + ")" + "*" + "("+ lhs + "))", grad)


class Divide(Expr):
    def __init__(self):
        pass

    def _eval(self,cur_node):
        return "("+Expr(cur_node.ast.left).eval() + " / " + Expr(cur_node.ast.right).eval()+")"

    def _forward_diff(self,cur_node):
        lhs = Expr(cur_node.ast.left).eval()
        rhs = Expr(cur_node.ast.right).eval()
        return "(" +rhs+ " * " +Expr(cur_node.ast.left)._forward_diff() + " - " \
                        + lhs+ " * " +Expr(cur_node.ast.right)._forward_diff()+")" + "/ (" + rhs + " * " + rhs+")"

    def _reverse_diff(self, cur_node, adjoint, grad):
        lhs = Expr(cur_node.ast.left).eval()
        rhs = Expr(cur_node.ast.right).eval()
        Expr(cur_node.ast.left)._reverse_diff("("+ adjoint + ")" + "/" + "("+ rhs + ")", grad)
        Expr(cur_node.ast.right)._reverse_diff("(-1*("+adjoint +") * ("+ lhs + "))/((" + rhs + ") * (" + rhs+"))", grad)



class Log(Expr):
    def __init__(self):
        pass


    def _eval(self,cur_node):
        try:
            exp = cur_node.ast.args.exprs[0].name
        except:
            exp = Expr(cur_node.ast.args.exprs[0]).eval()
        return "(log("+Expr(exp).eval()+"))"
    def _forward_diff(self,cur_node):   
        # skipped the try except - may break
        exp_eval = Expr(cur_node.ast.args.exprs[0]).eval()
        exp = cur_node.ast.args.exprs[0]
        return "(1/("+ exp_eval +")*"+Expr(exp)._forward_diff()+")"

    def _reverse_diff(self, cur_node, adjoint, grad):
        exp_eval = Expr(cur_node.ast.args.exprs[0]).eval()
        exp = cur_node.ast.args.exprs[0]
        Expr(exp)._reverse_diff("(" + adjoint + ") * "+" (1/("+exp_eval+"))", grad)           





class Pow(Expr):
    def __init__(self):
        pass
    def _eval(self,cur_node):
        try:
            base = cur_node.ast.args.exprs[0].name
        except:
            base = Expr(cur_node.ast.args.exprs[0]).eval()


        try:
            exp = cur_node.ast.args.exprs[1].value
        except AttributeError:
            exp = Expr(cur_node.ast.args.exprs[1]).eval()
        return "(pow(%s,%s))" % (Expr(base).eval(),exp) # TODO

    def _forward_diff(self,cur_node):
        try:
            base = cur_node.ast.args.exprs[0].name
        except:
            base = Expr(cur_node.ast.args.exprs[0]).eval()

        try:
            exp = cur_node.ast.args.exprs[1].value
        except AttributeError:
            exp = Expr(cur_node.ast.args.exprs[1]).eval()

        der_base = Expr(base)._forward_diff()
        der_exp = Expr(exp)._forward_diff()

        return "(pow("+base+",("+exp+"-1)) * "+\
                "("+exp+ " * "+ der_base +" + "+base+ " * "+ der_exp+ " * log("+base+")))"


    def _reverse_diff(self, cur_node, adjoint, grad):
        try:
            base = cur_node.ast.args.exprs[0].name
        except:
            base = Expr(cur_node.ast.args.exprs[0]).eval()

        try:
            exp = cur_node.ast.args.exprs[1].value
        except AttributeError:
            exp = Expr(cur_node.ast.args.exprs[1]).eval()
        Expr(base)._reverse_diff( "(" + adjoint + ")"+ "*"+ "("+ exp+")"+" * " + "(pow(" + base +","+ "("+exp +"- 1)"+"))", grad)
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


    def _reverse_diff(self, cur_node, adjoint, grad):
        exp = cur_node.ast.args.exprs[0].name
        Expr(exp)._reverse_diff("(" + adjoint + ") * "+" (cos("+exp+"))", grad)




class Cosine(Expr):
    def __init__(self):
        pass

    def _eval(self,cur_node):
        exp = cur_node.ast.args.exprs[0].name
        return "(cos("+Expr(exp).eval()+"))"

    def _forward_diff(self,cur_node):
        exp = cur_node.ast.args.exprs[0].name
        return "(-1*sin("+exp +")*"+Expr(exp)._forward_diff()+")"

    def _reverse_diff(self, cur_node, adjoint, grad):
        exp = cur_node.ast.args.exprs[0].name
        Expr(exp)._reverse_diff("(" + adjoint + ") * "+" (-1*sin("+exp+"))", grad)



def show_attrs(node):
    for attr in dir(node):
        print("-----------------")

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


# def grad(ast, x=0):
#     """
#     Returns a function which computes gradient of `fun` with respect to
#     positional argument number `x`. The returned function takes the
#     same arguments as `fun` , but returns the gradient instead. The function
#     `fun` is expected to be scalar valued. The gradient has the same type as argument."""
#     assert type(x) in (int, tuple, list), x

#     fun = ast.ext[-1].body.block_items[1].init
#     return get_traversal(fun,x)

def simplify_equation(equation):
    import re
    m = re.findall(r"(\d.)",equation)
    groups = np.unique(m)
    for digit in groups: equation = equation.replace("("+digit+")",digit)



    m = re.findall(r"(\d)",equation)
    groups = np.unique(m)
    for digit in groups: equation = equation.replace("("+digit+")",digit)


    return equation



def simplify_graph(old_ast):
    if old_ast.init.type() == 'decl':
        print('gotcha')
    elif old_ast.type() == 'BinaryOp':
        print('no gotcha')


def match_item(ast):
    if ast.block_items:
        for block in ast.block_items:
            if (type(block)) == 'c_ast.For':
                print("True")

def make_graph(ast):
    fun = None

    for funs in range(len(ast.ext)):
        if 'decl' not in  dir(ast.ext[funs]):
            continue

    fun_body = ast.ext[funs].body
    match_item(fun_body)


def expand_equation(equation, dict_):
    if equation.__class__.__name__ == 'ArrayRef':

        if equation.name.__class__.__name__ == 'ArrayRef':
            var_name = equation.name.name.name+'[{}][{}]'.format(str(equation.name.subscript.value),str(equation.subscript.value))
        else:
            var_name = equation.name.name + '[{}]'.format(str(equation.subscript.value))

        if var_name in dict_.keys():
            equation = dict_[var_name]

    if equation.__class__.__name__ == 'ID':
        if equation.name in dict_.keys():
            equation = dict_[equation.name]

    if 'left' in dir(equation):
        equation.left = expand_equation(equation.left, dict_)
    if 'right' in dir(equation):
        equation.right = expand_equation(equation.right, dict_)

    if 'args' in dir(equation):
        equation.args = expand_equation(equation.args, dict_)

    if 'exprs' in dir(equation):
        for i in range(len(equation.exprs)):
            equation.exprs[i] = expand_equation(equation.exprs[i], dict_)




    return equation


def grad(ast, expression, variables, func = 'function',
                          reverse_diff = False, second_der = False, output_filename = 'c_code',
                          output_func = 'compute'):
    """
    Returns a function which computes gradient of `fun` with respect to
    positional argument number `x`. The returned function takes the
    same arguments as `fun` , but returns the gradient instead. The function
    `fun` is expected to be scalar valued. The gradient has the same type as argument."""
    global ext_index
    fun = None

    for funs in range(len(ast.ext)):
        if 'decl' not in  dir(ast.ext[funs]):
            continue
        fun_name = ast.ext[funs].decl.name
        if fun_name == func:
            ext_index = funs
            break
    assert fun_name == func

    der_vars = ast.ext[ext_index].decl.type.args.params

    global curr_base_variable

    if(reverse_diff and second_der):
        print('Computing Hessian with Reverse Differentiation')
        c_code = c_generator.CGenerator(filename = output_filename, variable_count = len(variables), derivative_count = len(variables)*len(variables))
    elif (not reverse_diff and second_der):
        print('Computing Hessian with Forward Differentiation')
        c_code = c_generator.CGenerator(filename = output_filename, variable_count = len(variables), derivative_count = (len(variables)*(len(variables))))

    else:
        if reverse_diff:
            print('Computing Gradient with Reverse Differentiation')  
        else:
            print('Computing Gradient with Forward Differentiation')  

        c_code = c_generator.CGenerator(filename = output_filename, variable_count = len(variables), derivative_count = len(variables))

    file_pointer = open(output_filename+'.c','a')
    file_pointer = c_code._make_header(output_func, file_pointer)

    dict_ = {}


    # old code: looks for a new variable declaration and processes it only then.
    # for blocks in range(len(ast.ext[ext_index].body.block_items)):
    #     print(dir(ast.ext[ext_index].body.block_items[blocks]))
    #     if 'name' not in dir(ast.ext[ext_index].body.block_items[blocks]):
    #         continue

    #     if ast.ext[ext_index].body.block_items[blocks].type.__class__.__name__ == 'ArrayDecl':

    #         if ast.ext[ext_index].body.block_items[blocks].type.type.__class__.__name__ == 'ArrayDecl':
    #             expr_name = ast.ext[ext_index].body.block_items[blocks].name+'[{}][{}]'.format(ast.ext[ext_index].body.block_items[blocks].type.dim.value,ast.ext[ext_index].body.block_items[blocks].type.type.dim.value)
    #         else:
    #             expr_name = ast.ext[ext_index].body.block_items[blocks].name+'[{}]'.format(ast.ext[ext_index].body.block_items[blocks].type.dim.value)
    #     else:
    #         expr_name = ast.ext[ext_index].body.block_items[blocks].name
    #     if expr_name != expression:
    #         dict_[expr_name] = ast.ext[ext_index].body.block_items[blocks].init
    #         continue

    #     fun = ast.ext[ext_index].body.block_items[blocks].init




    # looks for an assignment
    for blocks in range(len(ast.ext[ext_index].body.block_items)):
        if ast.ext[ext_index].body.block_items[blocks].__class__.__name__ == 'Decl':
            if ast.ext[ext_index].body.block_items[blocks].type.__class__.__name__ == 'ArrayDecl':
                expr_name = ""
                arr = ast.ext[ext_index].body.block_items[blocks].type
                while arr.__class__.__name__!="TypeDecl":
                    expr_name += "[{}]".format(arr.dim.value)
                    arr = arr.type
                expr_name = arr.declname+expr_name
            else:
                expr_name = ast.ext[ext_index].body.block_items[blocks].name

            if expr_name in dict_.keys():
                substite_in_fun = ast.ext[ext_index].body.block_items[blocks].init
                dict_[expr_name] = expand_equation(substite_in_fun, dict_)
            else:
                dict_[expr_name] = expand_equation(ast.ext[ext_index].body.block_items[blocks].init, dict_)


            if expr_name != expression:
                continue


            fun = dict_[expr_name]







        if ast.ext[ext_index].body.block_items[blocks].__class__.__name__ == 'Assignment':

            # dealing with array names
            if ast.ext[ext_index].body.block_items[blocks].lvalue.__class__.__name__ == 'ArrayRef':
                expr_name = ""
                arr = ast.ext[ext_index].body.block_items[blocks].lvalue
                while arr.__class__.__name__!="ID":
                    expr_name += "[{}]".format(arr.subscript.value)
                    arr = arr.name
                expr_name = arr.name+expr_name
            # scalar variables
            else:
                expr_name = ast.ext[ext_index].body.block_items[blocks].lvalue.name


            # has the variable been encountered before
            if expr_name in dict_.keys():
                substite_in_fun = ast.ext[ext_index].body.block_items[blocks].rvalue
                dict_[expr_name] = expand_equation(substite_in_fun, dict_)
            else:
                dict_[expr_name] = expand_equation(ast.ext[ext_index].body.block_items[blocks].rvalue, dict_)


            if expr_name != expression:
                continue

            fun = dict_[expr_name]

    assert fun != None

    # fun.show()

    # print("dictionary: ")
    # print(dict_)

    # print("Function: ")
    # fun.show()

    # fun = expand_equation(fun, dict_)

    # print("Expanded equation:")
    # fun.show()


    grad = {}
    for i, vars_ in enumerate(variables):
        file_pointer = c_code._declare_vars(vars_,i,file_pointer=file_pointer)
        grad[vars_] = '0'




    # print(grad)

    if reverse_diff:
        if second_der:
            Expr(fun)._reverse_diff("1.",grad)


            ctr=0
            for i, vars_ in enumerate(variables):
                primary_base_variable = Variable(vars_)

                k = vars_
                v = grad[vars_]

                simplified = simplify_equation(v)

                new_parser = c_parser.CParser()
                new_ast = new_parser.parse("double f = {};".format(simplified), filename='<none>')


                grad_hess = {}
                for i_ctr, vars_ in enumerate(variables):
                    grad_hess[vars_] = '0'

                Expr(new_ast.ext[0].init)._reverse_diff("1.",grad_hess)

                for j in range(i, len(variables)):

                    k_hess = variables[j]
                    v_hess = grad_hess[k_hess]

                    secondary_base_variable = Variable(k_hess)

                    file_pointer = c_code._generate_expr([primary_base_variable._get(), secondary_base_variable._get()], v_hess,index=ctr, file_pointer=file_pointer)
                    ctr+=1



        else:
            Expr(fun)._reverse_diff("1.",grad)
            # print(grad)
            i = 0
            for k,v in grad.items():
                file_pointer=c_code._generate_expr(k, v,index=i, file_pointer=file_pointer)
                i += 1

    # forward hessian
    elif second_der:
        ctr=0
        dictionary = {}
        for i,vars_ in enumerate(variables):
            curr_base_variable = Variable(vars_)
            primary_base_variable = Variable(vars_)

            derivative = Expr(fun)._forward_diff()

            derivative = simplify_equation(derivative)
            new_parser = c_parser.CParser()
            new_ast = new_parser.parse("double f = {};".format(derivative), filename='<none>')

            for j in range(i, len(variables)):
                vars_second = variables[j]
                curr_base_variable = Variable(vars_second)
                secondary_base_variable = Variable(vars_second)

                second_derivative = Expr(new_ast.ext[0].init)._forward_diff()
                c_code._generate_expr([primary_base_variable._get(), secondary_base_variable._get()], second_derivative,index=ctr, file_pointer=file_pointer)
                string = str(i)+','+str(j)
                dictionary[string] = ctr

                ctr+=1

        pointer_index = 1

        for i,vars_ in enumerate(variables):
            curr_base_variable = Variable(vars_)
            primary_base_variable = Variable(vars_)
            for j in range(0,i):
                vars_second = variables[j]
                curr_base_variable = Variable(vars_second)
                secondary_base_variable = Variable(vars_second)
                string = str(j)+','+str(i)
                pointer_index = dictionary[string]
                c_code._generate_copy([primary_base_variable._get(), secondary_base_variable._get()], pointer_index=pointer_index,index=ctr,file_pointer=file_pointer)
                ctr += 1



    else:
        for i,vars_ in enumerate(variables):
            curr_base_variable = Variable(vars_)
            derivative = Expr(fun)._forward_diff() 
            c_code._generate_expr(curr_base_variable._get(), derivative,index=i,file_pointer=file_pointer)        

    c_code._make_footer(file_pointer)
        



def grad_with_split(ast, expression, variables, func = 'function', 
                          reverse_diff = False, second_der = False, output_filename = 'c_code',
                          output_func = 'compute', split_by = 20):

    """
    Returns a function which computes gradient of `fun` with respect to
    positional argument number `x`. The returned function takes the 
    same arguments as `fun` , but returns the gradient instead. The function
    `fun` is expected to be scalar valued. The gradient has the same type as argument."""
    global ext_index
    fun = None

    for funs in range(len(ast.ext)):
        if 'decl' not in  dir(ast.ext[funs]):
            continue
        fun_name = ast.ext[funs].decl.name
        if fun_name == func:
            ext_index = funs
            break
    assert fun_name == func

    der_vars = ast.ext[ext_index].decl.type.args.params

    global curr_base_variable

    if(reverse_diff and second_der):
        print('Computing Hessian with Reverse Differentiation')
        c_code = c_generator.CGenerator(filename = output_filename+'0', variable_count = len(variables), derivative_count = len(variables)*len(variables), split=True)
    elif (not reverse_diff and second_der):
        print('Computing Hessian with Forward Differentiation')        
        c_code = c_generator.CGenerator(filename = output_filename+'0', variable_count = len(variables), derivative_count = (len(variables)*(len(variables))), split=True)

    else:
        if reverse_diff:
            print('Computing Gradient with Reverse Differentiation')  
        else:
            print('Computing Gradient with Forward Differentiation')  

        c_code = c_generator.CGenerator(filename = output_filename+'0', variable_count = len(variables), derivative_count = len(variables), split=True)
    file_pointer = open(output_filename+'0.c','a')
    file_pointer = c_code._make_header(output_func, file_pointer)

    dict_ = {}
    # looks for an assignment
    for blocks in range(len(ast.ext[ext_index].body.block_items)):
        if ast.ext[ext_index].body.block_items[blocks].__class__.__name__ == 'Decl':
            if ast.ext[ext_index].body.block_items[blocks].type.__class__.__name__ == 'ArrayDecl':
                expr_name = ""
                arr = ast.ext[ext_index].body.block_items[blocks].type
                while arr.__class__.__name__!="TypeDecl":
                    expr_name += "[{}]".format(arr.dim.value)
                    arr = arr.type
                expr_name = arr.declname+expr_name            
            else:
                expr_name = ast.ext[ext_index].body.block_items[blocks].name

            if expr_name in dict_.keys():
                substite_in_fun = ast.ext[ext_index].body.block_items[blocks].init
                dict_[expr_name] = expand_equation(substite_in_fun, dict_)
            else:
                dict_[expr_name] = expand_equation(ast.ext[ext_index].body.block_items[blocks].init, dict_)     
                

            if expr_name != expression:
                continue       


            fun = dict_[expr_name]


        if ast.ext[ext_index].body.block_items[blocks].__class__.__name__ == 'Assignment':

            # dealing with array names
            if ast.ext[ext_index].body.block_items[blocks].lvalue.__class__.__name__ == 'ArrayRef':
                expr_name = ""
                arr = ast.ext[ext_index].body.block_items[blocks].lvalue
                while arr.__class__.__name__!="ID":
                    expr_name += "[{}]".format(arr.subscript.value)
                    arr = arr.name
                expr_name = arr.name+expr_name
            # scalar variables
            else:
                expr_name = ast.ext[ext_index].body.block_items[blocks].lvalue.name


            # has the variable been encountered before
            if expr_name in dict_.keys():
                substite_in_fun = ast.ext[ext_index].body.block_items[blocks].rvalue
                dict_[expr_name] = expand_equation(substite_in_fun, dict_)
            else:
                dict_[expr_name] = expand_equation(ast.ext[ext_index].body.block_items[blocks].rvalue, dict_)
            

            if expr_name != expression:
                continue

            fun = dict_[expr_name]

    assert fun != None







    job_finished = False

    if not reverse_diff:

        if second_der:

            grad = {}
            for i, vars_ in enumerate(variables):
                grad[vars_] = ''            


            ctr=0
            split_ctr = 0            


            # matrix size: i x j
            # matrix size flattened : i*j values

            # produce sub arrays after splitting          
            

            for i,vars_ in enumerate(variables):
                curr_base_variable = Variable(vars_)
                primary_base_variable = Variable(vars_)

                derivative = Expr(fun)._forward_diff()  

                derivative = simplify_equation(derivative)

                # produce new ast of derivative
                new_parser = c_parser.CParser()
                new_ast = new_parser.parse("double f = {};".format(derivative), filename='<none>')

                # compute upper triangular (with diagonal)
                for j in range(i, len(variables)):
                    vars_second = variables[j]
                    curr_base_variable = Variable(vars_second)
                    secondary_base_variable = Variable(vars_second)

                    second_derivative = Expr(new_ast.ext[0].init)._forward_diff()
                    print("[{},{} / {}] Second derivative : df / d{} d{}:".format(i,j,len(variables),vars_, vars_second))

                    flattened_mat_idx = i*len(variables) + j
                    flattened_mat_idx_mirror = i + j*len(variables)

                    # file_pointer returned to ensure file finishes writing this block
                    file_pointer = c_code._generate_expr([primary_base_variable._get(), secondary_base_variable._get()], second_derivative,index = split_ctr, mirrored_index = None, file_pointer = file_pointer)

                    ctr+=1
                    split_ctr += 1
                    if  ctr % split_by==0:
                        tmp = int(ctr//split_by)
                        print("Splitting file . Producing file ",tmp)
                        c_code._make_footer(file_pointer)
                        
                        
                        if not (i==(len(variables)-1) and j==(len(variables)-1)):
                            c_code = c_generator.CGenerator(filename = output_filename+str(tmp), variable_count = len(variables), 
                                derivative_count = (len(variables)*(len(variables))), split=True)
                            file_pointer = open(output_filename+str(tmp)+'.c','a')
                            file_pointer = c_code._make_header(output_func, file_pointer)
                            job_finished = True

                        split_ctr = 0
        else:
            ctr=0
            split_ctr = 0  
            
            for i,vars_ in enumerate(variables):
                ctr += 1
                split_ctr += 1
                
                curr_base_variable = Variable(vars_)
                derivative = Expr(fun)._forward_diff() 

                c_code._generate_expr(curr_base_variable._get(), derivative, index=i, file_pointer = file_pointer)        

        if not job_finished:
            c_code._make_footer(file_pointer)



    elif reverse_diff:
        grad = {}
        for i, vars_ in enumerate(variables):
            # c_code._declare_vars(vars_,i)
            grad[vars_] = '0'        

        if second_der:
            ctr=0
            split_ctr = 0            

            Expr(fun)._reverse_diff("1.",grad) 

            for i,vars_ in enumerate(variables):
                primary_base_variable = Variable(vars_)

                k = vars_
                v = grad[vars_]

                derivative = simplify_equation(v)

                new_parser = c_parser.CParser()
                new_ast = new_parser.parse("double f = {};".format(derivative), filename='<none>')

                grad_hess = {}
                for i_ctr, vars_ in enumerate(variables):
                    grad_hess[vars_] = '0'              

                Expr(new_ast.ext[0].init)._reverse_diff("1.",grad_hess)


                for j in range(i, len(variables)):

                    k_hess = variables[j]
                    v_hess = grad_hess[k_hess]

                    secondary_base_variable = Variable(k_hess)
                    

                    print("[{},{} / {}] Second derivative : df / d{} d{}:".format(i,j,len(variables),k, k_hess))

                    file_pointer = c_code._generate_expr([primary_base_variable._get(), secondary_base_variable._get()], v_hess, index = split_ctr, mirrored_index = None, file_pointer = file_pointer)

                    ctr+=1
                    split_ctr += 1
                    if  ctr % split_by==0:
                        tmp = int(ctr//split_by)
                        print("Splitting file . Producing file ",tmp)

                        c_code._make_footer(file_pointer)

                        
                        
                        if not (i==(len(variables)-1) and j==(len(variables)-1)):

                            c_code = c_generator.CGenerator(filename = output_filename+str(tmp), variable_count = len(variables), 
                                derivative_count = (len(variables)*(len(variables))), split=True)                            
                            file_pointer = open(output_filename+str(tmp)+'.c','a')
                            file_pointer = c_code._make_header(output_func, file_pointer)
                            job_finished = True

                        split_ctr = 0      

        else:
            ctr=0
            split_ctr = 0  

            Expr(fun)._reverse_diff("1.",grad) 

            for i,vars_ in enumerate(variables):
                ctr += 1
                split_ctr += 1
                
                curr_base_variable = Variable(vars_)
                v_grad = grad[vars_]

                file_pointer = c_code._generate_expr([primary_base_variable._get()], v_grad, index = split_ctr, mirrored_index = None, file_pointer = file_pointer)

        if not job_finished:
            c_code._make_footer(file_pointer)


def prepare_graph_from_file(filename):
    global curr_base_variable, ext_index
    ast = parse_file(filename, use_cpp=False,
            cpp_path='gcc',
            cpp_args=['-E', r'-Iutils/fake_libc_include'])

    curr_base_variable = Variable("temp")
    make_graph(ast)
    ext_index = 0
    return ast


def prepare_graph(function):
    c_parser_obj = c_parser.CParser()
    ast = c_parser_obj.parse(function)
    make_graph(ast)
    curr_base_variable = Variable("temp")
    ext_index = 0
    return ast


def autodiff(function, expression, variables, func = 'function',
                reverse_diff = False, second_der = False, output_filename = 'c_code',
                output_func = 'compute', split=False, split_by=20):


    ast = prepare_graph(function)
    if split:
        grad_with_split(ast, expression, variables, func = func, 
            reverse_diff = reverse_diff, second_der = second_der, output_filename = output_filename, 
            output_func = output_func, split_by=split_by)
    else:
        grad(ast, expression, variables, func = func, 
            reverse_diff = reverse_diff, second_der = second_der, output_filename = output_filename, 
            output_func = output_func)        





def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('filename', type = str, help='file name')
    parser.add_argument('expr', type = str, help='expression')
    parser.add_argument('-v', '--vars',
                      type=str, action='store',
                      dest='variables',
                      help='Variables to differentiate wrt to')
    parser.add_argument('--func', type = str, default = 'function', dest = 'func', help='function name (optional)')
    parser.add_argument('--reverse', default = False, action='store_true', dest = 'reverse', help='reverse differentiation')
    parser.add_argument('--second_der', default = False, action='store_true', dest = 'second_der', help='second derivative')
    parser.add_argument('--output_filename', type = str, default ='c_code', help='output file name')
    parser.add_argument('--output_function', type = str, default ='compute', help='output function name')


    parser = parser.parse_args()

    filename = parser.filename
    variables = parser.variables.split(",")
    expression = parser.expr
    output_filename = parser.output_filename
    reverse_diff = parser.reverse
    second_der = parser.second_der
    output_func = parser.output_function

    if reverse_diff:
        print("Differentiation Method: Reverse")
    else:
        print("Differentiation Method: Forward")

    if second_der:
        print("Derivative order: Second")
    else:
        print("Derivative order: First")

    print("Parallel : False")
    print("Splitted : False")

    ast = prepare_graph_from_file(filename)
    grad(ast, expression, variables, func = parser.func,
                          reverse_diff = reverse_diff, second_der = second_der, output_filename = output_filename,
                          output_func = output_func)


if __name__ == "__main__":
    main()