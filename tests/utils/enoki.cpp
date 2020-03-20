#include <iostream>
#include <fstream>
#include <chrono>
#include <string>
#include <Eigen/Cholesky>
#include <enoki/array.h>
#include <enoki/autodiff.h>
#include <enoki/autodiff.cpp>

/* Don't forget to include the 'enoki' namespace */
using namespace enoki;
using namespace std;
using namespace std::chrono;

/* Static float array (the suffix "P" indicates that this is a fixed-size packet) */
using FloatP = Packet<float, 4>;

/* Dynamic float array (vectorized via FloatP, the suffix "X" indicates arbitrary length) */
using FloatX = DynamicArray<FloatP>;

using FloatD = DiffArray<FloatX>;

int main(int argc, char **argv)
{
    int num_params = 30010;
    int num_vars = 2;
    Eigen::VectorXd args(num_params * num_vars);
	FloatX init_K = zero<FloatX>(num_params);
	FloatX init_L = zero<FloatX>(num_params);
 
    string output_filename = argv[1];
    ofstream outfile;
    outfile.open(output_filename);

    std::ifstream file("params.txt");

    int i = 0;
    for (std::string line; std::getline(file, line);)
    {
        args(i) = stod(line.c_str());
        i++;
    }
    file.close();
    for (int i = 0; i < num_params; i++)
    {
		init_K[i] = args[i * num_vars + 0];
		init_L[i] = args[i * num_vars + 1];

    }

	FloatD K(init_K);
	FloatD L(init_L);
 
	set_requires_gradient(K);
	set_requires_gradient(L);
 
    FloatD function = 4*4*((K * (1 - K))*(L * (1 - L))); // derivative

    auto start = high_resolution_clock::now();
    backward(function);
	FloatX grad_K = gradient(K);
	FloatX grad_L = gradient(L);
 
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    outfile << (double)duration.count() / 1000000.0 << " ";
    for (int i = 0; i < num_params; i++)
    {
		outfile << grad_K[i] << " ";
		outfile << grad_L[i] << " ";
 
    }
    outfile.close();
    return 0;
}