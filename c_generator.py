#------------------------------------------------------------------------------
# autodiff: c_generator.py
#
# C code generator from autodiff nodes.
#
#------------------------------------------------------------------------------


class CGenerator(object):
	"""Writes a file with C code, hardcoded function definitions,
		uses string accumulation for returning expressions.
	"""

	def __init__(self, filename = 'c_code.c', points = 4):
		self.indent_level = 0
		self.filename=filename
		self.points = points

	def _make_indent(self):
		return ' ' * self.indent_level

	def _make_header(self):
		f = open(self.filename,'w')
		f.write("#include <math.h>\n\n")
		funcdecl = "void compute(" + "double x){"+"\n\n"
		f.write(funcdecl)
		f.close()

	def _generate_expr(self,derivative_string):
		f = open(self.filename,'a')
		f.write("return "+derivative_string+"\n")
		f.close()		


	def _make_footer(self):
		f = open(self.filename,'a')
		f.write("}\n\n")
		funcdecl = "void main(){\n\ncompute("+str(self.points)+")\n\n}"
		f.write(funcdecl)
		f.close()	

	def _write(self,derivative_string):
		self._make_header()
		self._generate_expr(derivative_string)
		self._make_footer()