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

	def __init__(self, filename = 'c_code', variable_count = 1, derivative_count = 1, split = False):
		self.indent_level = 0
		self.filename=filename
		self.variable_count = variable_count # number of variables
		self.derivative_count = derivative_count # number of derivatives
		self.count = 0
		self.split = split

		f = open(self.filename+'.c','w')
		f.close()



	def _make_indent(self):
		return ' ' * self.indent_level


	def _make_header(self, output_func, file_pointer):

		ext = '.c'

		print("Overwrite previous header files: ",self.filename)
		f = open(self.filename+'.h','w')
			
		f.write("void "+output_func+"(double values[], int num_points, double ders[]);")
		f.close()
            

		file_pointer.write("void "+output_func+"(double values[], int num_points, double ders[]){\n\n")
		file_pointer.write("\tfor(int i = 0; i < num_points; ++i)\n\t{\n") # iterate over
		return file_pointer		


	def _generate_expr(self, var, derivative_string, index, mirrored_index = None, file_pointer = None):
		base = ''
		if type(var) is list:
			base = 'd'+ 'd'.join(var)
		elif type(var) is str:
			base = var

		file_pointer.write("\t\tders[i*"+str(self.derivative_count)+"+"+str(index)+"]"+"= "+derivative_string+"; // {} \n".format('df/('+base+')'))
		if index != mirrored_index and mirrored_index:
			file_pointer.write("\t\tders[i*"+str(self.derivative_count)+"+"+str(mirrored_index)+"]"+"= ders[i*"+str(self.derivative_count)+"+"+str(index)+"]; // {} \n".format('df/('+base+')'))


		self.count += 1
		return file_pointer


	def _generate_copy(self, var, pointer_index, index, file_pointer=None):

		base = ''
		if type(var) is list:
			base = 'd'+ 'd'.join(var)
		elif type(var) is str:
			base = var

		file_pointer.write("\t\tders[i*"+str(self.derivative_count)+"+"+str(index)+"]"+"= ders[i*"+str(self.derivative_count)+"+"+str(pointer_index)+"]; // {} \n".format('df/('+base+')'))
		
		self.count += 1
		return file_pointer

	def _declare_vars(self, var, index, file_pointer=None):


		ext = '.c'
		file_pointer.write("\t\tdouble %s = values[i* %d + %d ];\n" % (var, self.variable_count, index))
		return file_pointer

	def _make_footer(self, file_pointer):


		ext = '.c'
		file_pointer.write("\t}\n}\n\n")
		file_pointer.close()



	def _write(self,derivative_string):
		self._make_header()
		self._generate_expr(derivative_string)
		self._make_footer()