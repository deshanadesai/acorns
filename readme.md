### Readme


# Sample Run

1. python3 forward_diff.py file.c 'p'  --vars "k,l" -func "to_diff"
2. clang c_code.c -o c_code or ispc c_code.ispc -o c_code.o
3. ./c_code (but this doesn’t have main function, so can add or create a new main file which calls this function and run).



# To do

* Expressions with parenthesis traversal
* Optimize making new expressions with full AST’s. Memory usage can be optimized.
* eval() method builds duplicate trees. Optimize.
* Deal with Multiple derivative variables.