from sympy import * 

g = symbols('g')
func = 4*((g * (1 - g)))
der = diff(func)
print(der)