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

	def __init__(self, filename = 'c_code', variable_count = 1, ispc = True, c_code = True):
		self.indent_level = 0
		self.filename=filename
		self.variable_count = 2 # number of variables
		self.count = 0
		self.ispc = ispc
		self.c_code = c_code

	def _make_indent(self):
		return ' ' * self.indent_level

	def _make_header(self):

		if self.c_code:
			ext = '.c'

			f = open(self.filename+ext,'w')
			f.write("void compute(double **values, long num_points, double **ders){\n\n")
			f.write("\tfor(int i = 0; i < num_points; ++i)\n\t{\n") # iterate over 
			f.close()


		if(self.ispc):
			ext = '.ispc'
			f = open(self.filename+ext,'w')
			f.write("export void compute(double **values, long num_points, double **ders){\n\n")
			f.write("\tforeach (index = 0 ... num_points)\n\t{\n") # iterate over 
			f.close()

	def _generate_expr(self, var, derivative_string):

		if self.c_code:

			ext = '.c'		
			f = open(self.filename+ext,'a')
			f.write("\t\tders[i]["+str(self.count)+"]"+"= "+derivative_string+";\n")
			f.close()		
		

		if(self.ispc):

			ext = '.ispc'	
			f = open(self.filename+ext,'a')
			f.write("\t\tders[index]["+str(self.count)+"]"+"= "+derivative_string+";\n")
			f.close()	
		self.count += 1	

	def _declare_vars(self, var, index):

		if self.c_code:

			ext = '.c'			
			f = open(self.filename+ext,'a')
			f.write("\t\tdouble %s = values[i][%d];\n" % (var, index))
			f.close()

		if(self.ispc):

			ext = '.ispc'				
			f = open(self.filename+ext,'a')
			f.write("\t\tdouble %s = values[index][%d];\n" % (var, index))
			f.close()			

	def _make_footer(self):

		if self.c_code:

			ext = '.c'			
			f = open(self.filename+ext,'a')
			f.write("\t}\n}\n\n")
			f.close()	

		if (self.ispc):

			ext = '.ispc'				
			f = open(self.filename+ext,'a')
			f.write("\t}\n}\n\n")	
			f.close()		


	def _write(self,derivative_string):
		self._make_header()
		self._generate_expr(derivative_string)
		self._make_footer()


