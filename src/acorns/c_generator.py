#------------------------------------------------------------------------------
# autodiff: c_generator.py
#
# C code generator from autodiff nodes.
#
#------------------------------------------------------------------------------
import math

class CGenerator(object):
	"""Writes a file with C code, hardcoded function definitions,
		uses string accumulation for returning expressions.
	"""

	def __init__(self, filename = 'c_code', variable_count = 1, derivative_count = 1):
		self.indent_level = 0
		self.filename=filename
		self.variable_count = variable_count # number of variables
		self.derivative_count = derivative_count # number of derivatives
		self.count = 0
		f = open(self.filename+'.c','w')
		f.close()

	def _make_indent(self):
		return ' ' * self.indent_level

	def _make_header(self, output_func):

		ext = '.c'

		print("Overwrite previous header files: ",self.filename)
		f = open(self.filename+'.h','w')
			
		f.write("void "+output_func+"(double values[], int num_points, double ders[]);")
		f.close()
            

		f = open(self.filename+ext,'w')
		f.write("void "+output_func+"(double values[], int num_points, double ders[]){\n\n")
		f.write("\tfor(int i = 0; i < num_points; ++i)\n\t{\n") # iterate over
		f.close()

	def _generate_expr(self, var, derivative_string, index):
		base = ''
		if type(var) is list:
			base = 'd'+ 'd'.join(var)
		elif type(var) is str:
			base = var

		ext = '.c'		
		f = open(self.filename+ext,'a')
		f.write("\t\tders[i*"+str(self.derivative_count)+"+"+str(index)+"]"+"= "+derivative_string+"; // {} \n".format('df/('+base+')'))
		f.close()


		self.count += 1

	def _generate_copy(self, var, pointer_index, index):

		base = ''
		if type(var) is list:
			base = 'd'+ 'd'.join(var)
		elif type(var) is str:
			base = var

		ext = '.c'
		f = open(self.filename+ext,'a')
		f.write("\t\tders[i*"+str(self.derivative_count)+"+"+str(index)+"]"+"= ders[i*"+str(self.derivative_count)+"+"+str(pointer_index)+"]; // {} \n".format('df/('+base+')'))
		f.close()
		
		self.count += 1

	def _declare_vars(self, var, index):


		ext = '.c'
		f = open(self.filename+ext,'a')
		f.write("\t\tdouble %s = values[i* %d + %d ];\n" % (var, self.variable_count, index))
		f.close()

	def _make_footer(self):


		ext = '.c'
		f = open(self.filename+ext,'a')
		f.write("\t}\n}\n\n")
		f.close()



	def _write(self,derivative_string):
		self._make_header()
		self._generate_expr(derivative_string)
		self._make_footer()