
import generate_function

if __name__ == '__main__':

    functions = []

    import random, string
    functions = []
    alphabets = list(string.ascii_lowercase)
    alphabets.remove('i')

    # for k in range(1, 10):
    #     function = generate_function.gen_other(k)
    #     functions.append(function)
    #     print(function)

    for k in range(2,11):
        temp = [generate_function.generate_poly(k,alphabets[0:5],20,[]), alphabets[0:5]]
        print(k)
        print(temp)
        functions.append(temp)

    for i, function in enumerate(functions):
        with open('sympy.txt', 'r') as file:
            sympy = file.read()  
            sympy_file = open("sympy_files/sympy_{}.py".format(i), "w+")
            # func_string = "{}".format(function[0])
            vars = ", ".join(str(x) for x in function[1])
            vars_str = "\'" + str(vars) + "\'"
            py_code = sympy % (str(function[1]), vars, vars_str, function[0])
            sympy_file.write(py_code)
            sympy_file.close()
