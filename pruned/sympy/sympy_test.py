from sympy import *
from sympy.utilities.codegen import codegen
import re
k = symbols('k')
expression = "(((((((k * (((((k * (1) + k * (1))) + ((k * (0) + 3 * (1))))) - ((4 * 1 - k * 0) / (4 * 4))) - ((k * k + (3 * k)) - (k / 4)) * 1) / k * k) + ((k * ((k * ((k * (1) + k * (1))) + k * k * (1))) + (k * k * k) * (1))))) + ((((22 / 7) * k) * ((k * (1) + k * (1))) + k * k * ((k * ((7 * 0 - 22 * 0) / (7 * 7)) + (22 / 7) * (1))))))) + ((k * ((k * ((k * ((k * ((k * ((k * ((k * ((k * (1) + k * (1))) + k * k * (1))) + (k * k * k) * (1))) + ((k * k * k) * k) * (1))) + (((k * k * k) * k) * k) * (1))) + ((((k * k * k) * k) * k) * k) * (1))) + (((((k * k * k) * k) * k) * k) * k) * (1))) + ((((((k * k * k) * k) * k) * k) * k) * k) * (1))))"




# index = c_expression.index("pow")



# print(c_expression)





def replace_all_pow(expression):
    expression = expression.replace(" ", "")
    while "pow" in expression:
        index_of_pow = expression.find("pow")
        first_index = expression.find("(", index_of_pow)
        last_index = expression.find(")", first_index)
        print("index of pow: {}, (: {}, ): {})".format(index_of_pow, first_index, last_index))

        var = expression[first_index + 1]
        exponent = int(expression[first_index + 3:last_index])
        multiplication_string = var
        for i in range(exponent-1):
            multiplication_string += "*{}".format(var)
        parentheses = expression[first_index:last_index+1]
        print(parentheses)
        expression = expression.replace(parentheses, multiplication_string)
        expression = expression.replace("pow", "", 1)
        print(expression)
    return expression

simple = collect(expression)
c_expression = ccode(simple)
print(c_expression)
deri = replace_all_pow(c_expression)
print(deri)