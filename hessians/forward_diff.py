from __future__ import print_function
import sys
from collections import namedtuple
import math
from pycparser import parse_file
from pycparser import c_parser
import pycparser.c_ast
import c_generator
import argparse
import numpy as np

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

    def eval(self):
        # print("trying to evaluate----")
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
                return (self.__variable__(self.ast.name.name, self.ast.subscript.value))._eval() 


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
                return (self.__variable__(self.ast.name.name.name+'[{}]'.format(self.ast.name.subscript.value), self.ast.subscript.value))._eval() 
            else:
                return (self.__variable__(self.ast.name.name, self.ast.subscript.value))._eval() 



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
        # if name == curr_base_variable._get():
        #     return base_vars[0]
        # else:
        # print("Making new variable",name)
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
        # print("VAR:")
        # print(self.name)
        # print(adjoint)
        # print(grad)         
        if self.name not in grad:
            pass
        elif grad[self.name] == '':
            grad[self.name] = adjoint
        else:            
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

    def _reverse_diff(self, adjoint, grad):
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
        if cur_node.type == 'UnaryOp':
            # print("Add unary op")
            # print(cur_node.ast.expr)
            return "("+Expr(cur_node.ast.expr).eval()+")"
        temp= "("+Expr(cur_node.ast.left).eval() + " + " + Expr(cur_node.ast.right).eval()+")"
        # print(temp)
        return temp

    def _forward_diff(self,cur_node):
        # print(type(cur_node.ast))
        # print("Forward Diff through add")
        # cur_node.ast.show()
        # print(cur_node.ast.right)
        # print("right value will be: ",Expr(cur_node.ast.right)._forward_diff())
        if cur_node.type == 'UnaryOp':
            return "("+Expr(cur_node.ast.expr)._forward_diff()+")"
        return "(" + "(" + Expr(cur_node.ast.left)._forward_diff()+")" + " + " + "("+Expr(cur_node.ast.right)._forward_diff()+")"+")"

    def _reverse_diff(self, cur_node, adjoint, grad):
        # print("ADD:")
        # print(cur_node)
        # print(adjoint)
        # print(grad)        
        Expr(cur_node.ast.left)._reverse_diff(adjoint, grad)
        Expr(cur_node.ast.right)._reverse_diff(adjoint, grad)





class Subtract(Expr):
    def __init__(self):
        # print("initiating subtract")
        pass    
    def _eval(self,cur_node):
        if cur_node.type == 'UnaryOp':
            # print("Unary opppppp")
            # print(cur_node.ast.expr)
            return "( -("+Expr(cur_node.ast.expr).eval()+"))"
        return "("+Expr(cur_node.ast.left).eval() + " - " + Expr(cur_node.ast.right).eval()+")"

    def _forward_diff(self,cur_node):
        if cur_node.type == 'UnaryOp':
            return "(-("+Expr(cur_node.ast.expr)._forward_diff()+"))"
        return "(" + "(" + Expr(cur_node.ast.left)._forward_diff()+")" + " - " + "("+Expr(cur_node.ast.right)._forward_diff()+")"+")"


    def _reverse_diff(self, cur_node, adjoint, grad):
        # print("SUBTRACT:")
        # print(cur_node)
        # print(adjoint)
        # print(grad)        
        Expr(cur_node.ast.left)._reverse_diff(adjoint, grad)
        Expr(cur_node.ast.right)._reverse_diff("-1*(" + adjoint+")", grad)



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
        # cur_node.ast.show() 


        return "(" + rhs+ " * " + "("+Expr(cur_node.ast.left)._forward_diff()+")" + " + " \
                        + lhs+ " * " + "("+Expr(cur_node.ast.right)._forward_diff() +")" +")" 

    def _reverse_diff(self, cur_node, adjoint, grad):
        # print("MULTIPLY:")
        lhs = Expr(cur_node.ast.left).eval()
        rhs = Expr(cur_node.ast.right).eval()
        # print(cur_node)
        # print(adjoint)
        # print(grad)
        # the adjoint of the left node is the adjoint of the current node * the diff of current node wrt the left node
        Expr(cur_node.ast.left)._reverse_diff("(("+ adjoint + ")" + "*" + "("+ rhs + "))", grad)
        Expr(cur_node.ast.right)._reverse_diff("(("+ adjoint + ")" + "*" + "("+ lhs + "))", grad)


class Divide(Expr):
    def __init__(self):
        pass    

    def _eval(self,cur_node):
        # print(cur_node.ast.left)
        # print(Expr(cur_node.ast.left).eval())
        # print(cur_node.ast.right)
        # print(Expr(cur_node.ast.right).eval())
        return "("+Expr(cur_node.ast.left).eval() + " / " + Expr(cur_node.ast.right).eval()+")"

    def _forward_diff(self,cur_node):
        # print("in divide forward:",cur_node.ast)
        lhs = Expr(cur_node.ast.left).eval()
        # print("lhs: ",lhs)
        rhs = Expr(cur_node.ast.right).eval()
        return "(" +rhs+ " * " +Expr(cur_node.ast.left)._forward_diff() + " - " \
                        + lhs+ " * " +Expr(cur_node.ast.right)._forward_diff()+")" + "/ (" + rhs + " * " + rhs+")"

    def _reverse_diff(self, cur_node, adjoint, grad):
        # print("DIVIDE:")
        # print(cur_node)
        # print(adjoint)
        # print(grad)        
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
        # exp = cur_node.ast.args.exprs[0].name
        return "(log("+Expr(exp).eval()+"))"

    def _forward_diff(self,cur_node):       
        # exp = cur_node.ast.args.exprs[0].name
        try:
            exp = cur_node.ast.args.exprs[0].name
        except:
            exp = Expr(cur_node.ast.args.exprs[0]).eval()
        return "(1/("+ exp +")*"+Expr(exp)._forward_diff()+")"

    def _reverse_diff(self, cur_node, adjoint, grad):
        exp = cur_node.ast.args.exprs[0].name
        Expr(exp)._reverse_diff("(" + adjoint + ") * "+" (1/("+exp+"))")           




class Pow(Expr):
    def __init__(self):
        pass    
    def _eval(self,cur_node):
        # print("evaluation of: ")
        # cur_node.ast.show()
        # print(cur_node.ast.args.exprs)
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

    # def _second_der(self, cur_node):
    #     exp = cur_node.ast.args.exprs[0].name

    #     firstder_fn = "(cos("+ exp +")*"+Expr(exp)._forward_diff()+")"

    #     parser = c_parser.CParser()
    #     new_secder_ast = parser.parse(firstder_fn, filename='<none>')


    #     return Expr(new_secder_ast)._forward_diff()




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
        # print(attr)
        # print(getattr(node,attr))

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

def simplify_equation(equation):
    # assert type(equation) in (str)

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
            # print(type(block))
            # print(block.__class__.__name__ )
            if (type(block)) == 'c_ast.For':
                print("True")

def make_graph(ast):
    fun = None

    for funs in range(len(ast.ext)):
        if 'decl' not in  dir(ast.ext[funs]):
            continue

    fun_body = ast.ext[funs].body
    match_item(fun_body)



    # fun_body.block_items[0].show()

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

    if(reverse_diff and second_der):
        c_code = c_generator.CGenerator(filename = output_filename, variable_count = len(variables), derivative_count = len(variables)*len(variables), c_code = ccode, ispc = ispc)
    elif (not reverse_diff and second_der):
        c_code = c_generator.CGenerator(filename = output_filename, variable_count = len(variables), derivative_count = (len(variables)*(len(variables))), c_code = ccode, ispc = ispc)

    else:
        c_code = c_generator.CGenerator(filename = output_filename, variable_count = len(variables), derivative_count = len(variables), c_code = ccode, ispc = ispc)
    c_code._make_header()

    # for vars_ in der_vars:
    #     c_code._make_decls(vars_.name)

    # look for function to differentiate.
    dict_ = {}
    # fix the expanding eqn here
    for blocks in range(len(ast.ext[ext_index].body.block_items)):
        if 'name' not in dir(ast.ext[ext_index].body.block_items[blocks]):
            continue

        if ast.ext[ext_index].body.block_items[blocks].type.__class__.__name__ == 'ArrayDecl':

            if ast.ext[ext_index].body.block_items[blocks].type.type.__class__.__name__ == 'ArrayDecl':
                expr_name = ast.ext[ext_index].body.block_items[blocks].name+'[{}][{}]'.format(ast.ext[ext_index].body.block_items[blocks].type.dim.value,ast.ext[ext_index].body.block_items[blocks].type.type.dim.value)
            else:
                expr_name = ast.ext[ext_index].body.block_items[blocks].name+'[{}]'.format(ast.ext[ext_index].body.block_items[blocks].type.dim.value)
        else:
            expr_name = ast.ext[ext_index].body.block_items[blocks].name
        if expr_name != expression:
            dict_[expr_name] = ast.ext[ext_index].body.block_items[blocks].init
            continue

        fun = ast.ext[ext_index].body.block_items[blocks].init

    assert fun != None

    # fun.show()

    # print("dictionary: ")
    # print(dict_)
    # print("==============================================")

    # print("Function: ")
    # fun.show()

    fun = expand_equation(fun, dict_)

    # print("Expanded equation:")

    # fun.show()    


    grad = {}
    for i, vars_ in enumerate(variables):
        c_code._declare_vars(vars_,i)
        grad[vars_] = ''


      

    # print(grad)

    if reverse_diff:
        if second_der:
            Expr(fun)._reverse_diff("1.",grad) 


            ctr=0
            for i, vars_ in enumerate(variables):
                primary_base_variable = Variable(vars_)

                k = vars_
                v = grad[vars_]

                # print("First derivative: ")
                # print(vars_)
                # print(v)
                simplified = simplify_equation(v)
                # print("Simplified equation: ")
                # print(simplified)


                new_parser = c_parser.CParser()
                new_ast = new_parser.parse("double f = {};".format(simplified), filename='<none>')


                grad_hess = {}
                for i_ctr, vars_ in enumerate(variables):
                    grad_hess[vars_] = ''  



                Expr(new_ast.ext[0].init)._reverse_diff("1.",grad_hess)
                # print("Second Derivative: ")

                for j in range(i, len(variables)):

                    k_hess = variables[j]
                    v_hess = grad_hess[k_hess]

                    secondary_base_variable = Variable(k_hess)

                    # print("Second derivative : df / d{} d{}:".format(k, k_hess))

                    # print(k_hess)
                    # print(v_hess)

                    c_code._generate_expr([primary_base_variable._get(), secondary_base_variable._get()], v_hess,index=ctr)
                    ctr+=1



        else:
            Expr(fun)._reverse_diff("1.",grad) 
            # print(grad)
            i = 0
            for k,v in grad.items():
                c_code._generate_expr(k, v,index=i)
                i += 1


    elif second_der:
        ctr=0
        dictionary = {}
        for i,vars_ in enumerate(variables):
            curr_base_variable = Variable(vars_)
            # print("current base var: ",curr_base_variable. _get())
            primary_base_variable = Variable(vars_)

            derivative = Expr(fun)._forward_diff() 
            # print("First derivative: ")
            # print(derivative) 

            derivative = simplify_equation(derivative)
            new_parser = c_parser.CParser()
            new_ast = new_parser.parse("double f = {};".format(derivative), filename='<none>')

            for j in range(i, len(variables)):
                vars_second = variables[j]
                curr_base_variable = Variable(vars_second)
                secondary_base_variable = Variable(vars_second)

                second_derivative = Expr(new_ast.ext[0].init)._forward_diff()
                # print("Second derivative : df / d{} d{}:".format(vars_, vars_second))
                # print(second_derivative)
                c_code._generate_expr([primary_base_variable._get(), secondary_base_variable._get()], second_derivative,index=ctr)
                string = str(i)+','+str(j)
                dictionary[string] = ctr
                print(dictionary)
                
                ctr+=1

        pointer_index = 1

        for i,vars_ in enumerate(variables):
            curr_base_variable = Variable(vars_)
            # print("current base var: ",curr_base_variable. _get())
            primary_base_variable = Variable(vars_)                
            for j in range(0,i):
                vars_second = variables[j]
                curr_base_variable = Variable(vars_second)
                secondary_base_variable = Variable(vars_second)
                string = str(j)+','+str(i)
                pointer_index = dictionary[string]
                print(i,j,pointer_index)
                c_code._generate_copy([primary_base_variable._get(), secondary_base_variable._get()], pointer_index=pointer_index,index=ctr)
                ctr += 1



    else:
        for i,vars_ in enumerate(variables):
            curr_base_variable = Variable(vars_)
            derivative = Expr(fun)._forward_diff() 
            # print(derivative) 
            c_code._generate_expr(curr_base_variable._get(), derivative,index=i)        

    c_code._make_footer()
        

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
    parser.add_argument('-reverse', type = str, default = 'False', dest = 'reverse', help='function name')
    parser.add_argument('-second_der', type = str, default = 'False', dest = 'second_der', help='function name')
    parser.add_argument('--output_filename', type = str, default ='c_code', help='file name')    
    parser.add_argument('--nth_der', type = int, help='nth derivative')


    parser = parser.parse_args()


    filename = parser.filename
    variables = parser.variables.split(",")
    expression = parser.expr
    output_filename = parser.output_filename

    # print(output_filename)



    if parser.ccode == 'True':
        ccode = True
    else:
        ccode = False

    if parser.ispc == 'True':
        ispc = True
    else:
        ispc = False


    if parser.reverse == 'True':
        reverse_diff = True
    else:
        reverse_diff = False

    if parser.second_der == 'True':
        second_der = True
    else:
        second_der = False


    print("CCODE: ",ccode)
    print("ISPC CODE: ",ispc)
    ast = parse_file(filename, use_cpp=True,
            cpp_path='gcc',
            cpp_args=['-E', r'-Iutils/fake_libc_include'])

    curr_base_variable = Variable("temp")
    make_graph(ast)
    # ast.show()
    ext_index = 0
    # if len(ast.ext[0].body.block_items)>0:
    #     ast.ext[0].body.block_items[0].show()
    #     simplify_graph(ast.ext[0].body.block_items[0])
    grad_without_traversal(ast)
