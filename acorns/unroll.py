from __future__ import print_function
import sys
from collections import namedtuple
import math
from pycparser import parse_file
from pycparser import c_parser
import pycparser.c_ast
import acorns.c_generator
import argparse
import numpy as np
import pycparser.c_parser as c_parser
from pycparser import c_generator


class Generator(pycparser.c_ast.Node):
	"""
	Return stirng accumulation of expanded equations
	"""
	def __init__(self):
		self.indent_level = 0
		self.variables = {}
		self.names_vars= []
		self.symbols = []
		self.thresholds = []
		self.names_vars_init = []
		self.output_filename = ''
		self.constants = []

	def _make_indent(self):
		return ' ' * self.indent_level

	def visit(self, node, subscript = False, controller_vars = False):
		method = 'visit_' + node.__class__.__name__


		
		if subscript:
			if method == 'visit_Decl' or method == 'visit_DeclList':
				return getattr(self, method)(node, subscript, controller_vars=controller_vars)
			else:
				return getattr(self, method)(node, subscript)

		else:
			if method == 'visit_Decl' or method == 'visit_DeclList':
				return getattr(self, method)(node, controller_vars=controller_vars)
			else:
				return getattr(self, method)(node)

	def visit_Constant(self, n, subscript=False):
		return n.value

	def visit_ID(self, n, subscript=False):
		if subscript:
			if n.name in self.variables.keys():
				return self.variables[n.name]
		return n.name

	# def generic_visit(self, node):
	# 	if node is None:
	# 		return ''
	# 		# return ''.join(self.visit(c) for c_name, c in node.children())		

	def visit_FuncCall(self, n):
		if (n.name.name) == 'log':
			if n.args.__class__.__name__ == 'Expr':
				value = self.variables[self.visit(n.args.exprs[0])]
			elif n.args.__class__.__name__ == 'ExprList':
				value = self.visit_ExprList_from_FuncCall(n.args)
			else:
				raise "Unidentified expr in log"

			return 'log({})'.format(value)
		else:
			raise "Undefined function call"

	def visit_UnaryOp(self, n):
		if n.op == '*':
			return '*'+self.visit(n.expr)

	def visit_BinaryOp(self, n, subscript=False):
		if n.op == '+':
			left = self.visit(n.left, subscript=subscript)
			right = self.visit(n.right, subscript=subscript)


			if type(left).__name__ == 'list':
				
				arr_subscripts = self.flatten(left,[])
				left = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				left = left.format(*arr_subscripts[1:])

			if type(right).__name__ == 'list':
				arr_subscripts = self.flatten(right,[])
				right = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				right = right.format(*arr_subscripts[1:])

			if left in self.variables:
				left = self.variables[left]
			if right in self.variables:
				right = self.variables[right]

			if left.isnumeric() and right.isnumeric():
				return str(int(left)+int(right))

			return "("+left +") + ("+right+")"	
		elif n.op == '*':
			left = self.visit(n.left, subscript = subscript)
			right = self.visit(n.right, subscript = subscript)


			if type(left).__name__ == 'list':
				arr_subscripts = self.flatten(left,[])
				left = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				left = left.format(*arr_subscripts[1:])

			if type(right).__name__ == 'list':
				arr_subscripts = self.flatten(right,[])
				right = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				right = right.format(*arr_subscripts[1:])


			if left in self.variables:
				left = self.variables[left]
			if right in self.variables:
				right = self.variables[right]

			if left.isnumeric() and right.isnumeric():
				return str(int(left)*int(right))

			return "("+left +") * ("+right+")"	
		elif n.op == '-':
			left = self.visit(n.left, subscript = subscript)
			right = self.visit(n.right, subscript = subscript)


			if type(left).__name__ == 'list':
				arr_subscripts = self.flatten(left,[])
				left = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				left = left.format(*arr_subscripts[1:])

			if type(right).__name__ == 'list':
				arr_subscripts = self.flatten(right,[])
				right = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				right = right.format(*arr_subscripts[1:])

			if left in self.variables:
				left = self.variables[left]
			if right in self.variables:
				right = self.variables[right]


			if left.isnumeric() and right.isnumeric():
				return str(int(left)-int(right))

			return "("+left +") - ("+right+")"	
		elif n.op == '/':
			left = self.visit(n.left, subscript = subscript)
			right = self.visit(n.right, subscript = subscript)


			if type(left).__name__ == 'list':
				arr_subscripts = self.flatten(left,[])
				left = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				left = left.format(*arr_subscripts[1:])

			if type(right).__name__ == 'list':
				arr_subscripts = self.flatten(right,[])
				right = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				right = right.format(*arr_subscripts[1:])

			if left in self.variables:
				left = self.variables[left]
			if right in self.variables:
				right = self.variables[right]


			if left.isnumeric() and right.isnumeric():
				return str(int(left)/int(right))

			return "("+left +") / ("+right+")"	

	def visit_For(self, n):
		names_vars_init = self.visit(n.init, controller_vars = True)

		# for loop info extracted
		symbol = n.cond.op
		threshold = self.visit(n.cond.right)

		# if threshold is a variable, give it the value
		try:
			if str(threshold)!=str(int(threshold)):
				threshold = self.variables[threshold]
		except:
			threshold = self.variables[threshold]
		

		var_name = self.visit(n.cond.left)

		self.symbols.append(symbol)
		self.thresholds.append(int(threshold))
		self.names_vars.append(var_name)
		self.names_vars_init.append(names_vars_init)

		# Assuming next is one increment
		if n.stmt.__class__.__name__ == 'Compound' and n.stmt.block_items[0].__class__.__name__ == 'For':
			loop_stmt = self.visit(n.stmt)
		else:
			np_aranges = [np.array(np.arange(0,self.thresholds[i])) for i,s in enumerate(self.names_vars)]
			list_counters = np.array(np.meshgrid(*np_aranges)).T.reshape(-1,len(self.names_vars))

			for counter in list_counters:
				for i,item in enumerate(counter):
					self.variables[self.names_vars[i]] = str(item)
				vars_, value = self.visit(n.stmt)


				var_string = vars_[0]+'[{}]'*len(vars_[1:])
				f = open(output_filename+".c","a")
				f.write(var_string.format(*vars_[1:])+' = '+ str(value)+";\n")
				f.close()


			for v in self.names_vars:
				del self.variables[v]
			self.names_vars=[]
			self.names_vars_init=[]
			self.thresholds = []
			self.symbols = []

			return 
		return

	def visit_ArrayRef(self, n):

		return [self.visit(n.name), self.visit(n.subscript, subscript = True)]

	def visit_Compound(self, n):
		return self.visit(n.block_items[0])


	def flatten(self, x, flattened):
		if type(x).__name__!='list':
			return [x]
		elif len(x)==1:
			return x[0]
		for sublist in x:
			if type(sublist).__name__ == 'str':
				flattened.append(sublist)
			elif type(sublist).__name__ == 'list':
				self.flatten(sublist, flattened)

		return flattened

	def visit_Assignment(self, n, subscript=False):
		# print("@ Assignment")
		name = self.visit(n.lvalue, subscript=subscript)
		value = self.visit(n.rvalue, subscript=subscript)
		value = self.eval_arrayref(value)
		return self.flatten(name,[]), value

	def eval_arrayref(self, l):
		if type(l).__name__=='list':
			l = self.flatten(l,[])
			res = l[0]+'[{}]'*len(l[1:])
			return res.format(*l[1:])
		else:
			return l
	

	def visit_ExprList(self, n):
		visited_subexprs = []
		for expr in n.exprs:
			visited_subexprs.append(self.visit(expr))
		return "[{}]".format(','.join(visited_subexprs))

	# log(..) produces weird in pycparser
	def visit_ExprList_from_FuncCall(self, n):
		visited_subexprs = []
		for expr in n.exprs:
			visited_subexprs.append(self.visit(expr))
		return "{}".format(','.join(visited_subexprs))


	def visit_Return(self, n):
		f = open(output_filename+".c","a")
		f.write("return " +n.expr.name+";\n")
		f.close()		

	def visit_Decl(self, n, no_type=False, controller_vars = False):
		# no_type is used when a Decl is part of a DeclList, where the type is
		# explicitly only for the first declaration in a list.
		#

		if n.init.__class__.__name__=='BinaryOp':
			self.variables[n.name] = self.visit(n.init)
		elif n.init.__class__.__name__ == 'FuncCall':
			self.variables[n.name] = self.visit(n.init)
		elif n.init == None:
			if n.name in constants:
				self.variables[n.name] = None

			if not controller_vars:
				f = open(output_filename+".c","a")
				f.write(n.type.type.names[0] + " " +n.type.declname+";\n")
				f.close()

		else:
			if n.name in constants:
				self.variables[n.name] = n.init.value

			if not controller_vars:
				f = open(output_filename+".c","a")
				f.write(n.type.type.names[0] + " " +n.type.declname+" = " + n.init.value+";\n")
				f.close()

		return n.name



	def visit_DeclList(self, n, controller_vars = False):
		names = []
		for decl in n.decls:
			# this will break if something other than a decl is passed
			names.append(self.visit(decl, controller_vars = controller_vars))
		return names
		# s = self.visit(n.decls[0])
		# print("in decl list")
		# print(s)
		# if len(n.decls) > 1:
		# 	s += ', ' + ', '.join(self.visit_Decl(decl, no_type=True)
		# 		for decl in n.decls[1:])
		# return s
		


        # s = 'for ('
        # if n.init: s += self.visit(n.init)
        # s += ';'
        # if n.cond: s += ' ' + self.visit(n.cond)
        # s += ';'
        # if n.next: s += ' ' + self.visit(n.next)
        # s += ')\n'
        # s += self._generate_stmt(n.stmt, add_indent=True)
        # return s



def match_item(ast):
	gen = Generator()
	if ast.block_items:
		for block in ast.block_items:
			# print('In match item')
			# print(type(block))
			# print(block)
			res = gen.visit(block)
			if type(res).__name__=='tuple':
				# came from assignment or array ref. assumed assignment
				f = open(output_filename+".c","a")
				f.write(res[0][0]+' = '+ res[1]+";\n")
				f.close()


def make_graph(ast, output_filename):
    fun = None

    for funs in range(len(ast.ext)):
        if 'decl' not in  dir(ast.ext[funs]):
            continue
    
    generator = c_generator.CGenerator()
    function_decl = generator.visit(ast.ext[funs].decl)

    f = open(output_filename+".c",'w')
    f.write(function_decl+"{\n")
    f.close()


    fun_body = ast.ext[funs].body
    match_item(fun_body)

    f = open(output_filename+".c",'a')
    f.write('\n}')
    f.close()


def prepare_graph_from_file(filename, output_file, constants_list = []):
    
    global  output_filename,  constants

    output_filename = output_file
    constants =  constants_list

    ast = parse_file(filename, use_cpp=False,
            cpp_path='gcc',
            cpp_args=['-E', r'-Iutils/fake_libc_include'])

    make_graph(ast, output_filename)

    return ast


def prepare_graph(function, output_file, constants_list = []):
    
    global  output_filename, constants

    output_filename = output_file
    constants =  constants_list

    c_parser_obj = c_parser.CParser()
    ast = c_parser_obj.parse(function)
    make_graph(ast, output_filename)

    return ast    




if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('filename', type = str, help='file name')
    parser.add_argument('output_filename', type = str, default ='output_fun', help='op file name')    
    parser.add_argument('--constants', type = str, default ='', help = 'constants separated by commas')    



    parser = parser.parse_args()
    filename = parser.filename
    output_filename = parser.output_filename
    constants = parser.constants.split(',')




    ast = parse_file(filename, use_cpp=False,
            cpp_path='gcc',
            cpp_args=['-E', r'-Iutils/fake_libc_include'])
    # ast.show()
    make_graph(ast, output_filename)
    # ast.show()