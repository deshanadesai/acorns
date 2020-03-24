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
    int num_params = 2010;
    int num_vars = 4;
    Eigen::VectorXd args(num_params * num_vars);
	FloatX init_a = zero<FloatX>(num_params);
	FloatX init_b = zero<FloatX>(num_params);
	FloatX init_c = zero<FloatX>(num_params);
	FloatX init_d = zero<FloatX>(num_params);
 
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
		init_a[i] = args[i * num_vars + 0];
		init_b[i] = args[i * num_vars + 1];
		init_c[i] = args[i * num_vars + 2];
		init_d[i] = args[i * num_vars + 3];

    }

	FloatD a(init_a);
	FloatD b(init_b);
	FloatD c(init_c);
	FloatD d(init_d);
 
	set_requires_gradient(a);
	set_requires_gradient(b);
	set_requires_gradient(c);
	set_requires_gradient(d);
 
    FloatD function = (a*a+b*b+c*c+d*d)*(1+1/((a*d-b*c)*(a*d-b*c))); // derivative

    auto start = high_resolution_clock::now();
    backward(function);
	FloatX grad_a = gradient(a);
	FloatX grad_b = gradient(b);
	FloatX grad_c = gradient(c);
	FloatX grad_d = gradient(d);
 
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    outfile << (double)duration.count() / 1000000.0 << " ";
    for (int i = 0; i < num_params; i++)
    {
		outfile << grad_a[i] << " ";
		outfile << grad_b[i] << " ";
		outfile << grad_c[i] << " ";
		outfile << grad_d[i] << " ";
 
    }
    outfile.close();
    return 0;
}