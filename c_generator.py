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

	def __init__(self, filename = 'c_code.c', points = 2):
		self.indent_level = 0
		self.filename=filename
		self.points = 2
		self.count = 0

	def _make_indent(self):
		return ' ' * self.indent_level

	def _make_header(self):
		f = open(self.filename,'w')
		f.write("#include <math.h>\n\n")
		funcdecl = "double *compute(double values[], int count){\n\n\
double *ders;\nders = malloc(count * sizeof(*ders));\n\n";
		f.write(funcdecl)
		f.close()

	def _generate_expr(self, var, derivative_string):
		f = open(self.filename,'a')
		f.write("double "+var+" = values["+str(self.count)+"];\n")
		f.write("ders["+str(self.count)+"]"+"= "+derivative_string+";\n\n")
		f.close()		
		self.count += 1


	def _make_footer(self):
		# return
		f = open(self.filename,'a')
		f.write("return ders; \n}\n\n")
		funcdecl = "int main(){\n\n"
		funcbody = "int i, count = "+str(self.points)+";\ndouble *ders; \n\
double values["+str(self.points)+"] = {4.5,6.4};\n\n\
ders = compute(values, count);\n"
		funcprint = "printf(\"Printing values: \");\n\
for(i = 0 ; i < count ; i++) { \n\
		printf(\"%f \", ders[i]);\n\
	}\n\n\
free(ders);\n\
printf(\"\\n\\n\");\n\nreturn 0;\n\n}"
		f.write(funcdecl)
		f.write(funcbody)
		f.write(funcprint)
		f.close()	

	def _write(self,derivative_string):
		self._make_header()
		self._generate_expr(derivative_string)
		self._make_footer()