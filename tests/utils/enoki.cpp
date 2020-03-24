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
    int num_params = 4010;
    int num_vars = 3;
    Eigen::VectorXd args(num_params * num_vars);
	FloatX init_B = zero<FloatX>(num_params);
	FloatX init_a = zero<FloatX>(num_params);
	FloatX init_W = zero<FloatX>(num_params);
 
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
		init_B[i] = args[i * num_vars + 0];
		init_a[i] = args[i * num_vars + 1];
		init_W[i] = args[i * num_vars + 2];

    }

	FloatD B(init_B);
	FloatD a(init_a);
	FloatD W(init_W);
 
	set_requires_gradient(B);
	set_requires_gradient(a);
	set_requires_gradient(W);
 
    FloatD function = 4*4*4*((B * (1 - B))*(a * (1 - a))*(W * (1 - W))); // derivative

    auto start = high_resolution_clock::now();
    backward(function);
	FloatX grad_B = gradient(B);
	FloatX grad_a = gradient(a);
	FloatX grad_W = gradient(W);
 
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    outfile << (double)duration.count() / 1000000.0 << " ";
    for (int i = 0; i < num_params; i++)
    {
		outfile << grad_B[i] << " ";
		outfile << grad_a[i] << " ";
		outfile << grad_W[i] << " ";
 
    }
    outfile.close();
    return 0;
}