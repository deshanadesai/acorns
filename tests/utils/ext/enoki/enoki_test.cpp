#include <iostream>
#include <fstream>
#include <enoki/array.h>
#include <enoki/autodiff.h>
#include <enoki/autodiff.cpp>

/* Don't forget to include the 'enoki' namespace */
using namespace enoki;
using namespace std;
// using StrArray = Array<std::string, 2>;
using FloatC = DynamicArray<double>;

/* Static float array (the suffix "P" indicates that this is a fixed-size packet) */
using FloatP = Packet<float, 4>;

/* Dynamic float array (vectorized via FloatP, the suffix "X" indicates arbitrary length) */
using FloatX = DynamicArray<FloatP>;

using FloatD = DiffArray<FloatX>;

int main(int argc, char **argv)
{
    FloatX c = zero<FloatX>(53594);
    std::ifstream file("params.txt");
    int i = 0;
    for (std::string line; std::getline(file, line);)
    {
        c[i] = stod(line.c_str());
        i++;
    }
    file.close();
    cout << c << endl;
    FloatD a(c);
    set_requires_gradient(a);

    FloatD b = cos(a);
    backward(b);
    std::cout << gradient(a) << std::endl;
    return 0;
}