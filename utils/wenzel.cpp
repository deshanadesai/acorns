
#include <iostream>
#include <fstream>
#include <string>
#include <Eigen/Cholesky>
#include "autodiff.h"
#include <chrono>

DECLARE_DIFFSCALAR_BASE();

using namespace std;
using namespace std::chrono;

int main(int argc, char **argv)
{
    string output_filename = argv[1];

    cout << output_filename << endl;

    typedef Eigen::Vector2d Gradient;
    typedef Eigen::Matrix2d Hessian;
    typedef DScalar2<double, Gradient, Hessian> DScalar;

    Eigen::VectorXd x(2010);

    std::ifstream file("test_params.txt");
    int i = 0;
    for (std::string line; std::getline(file, line);)
    {
        x(i) = stod(line.c_str());
        i++;
    }
    file.close();

    ofstream outfile;
    outfile.open(output_filename);

    auto start = high_resolution_clock::now();

    for (int i = 0; i < 2010; i++)
    {
        /* There are two independent variables */
        DiffScalarBase::setVariableCount(2);
        DScalar k(0, x[i]);
        DScalar Fx = sin(k) + cos(j) + pow(l, 2);
        outfile << Fx.getGradient()(0) << " ";
    }

    auto stop = high_resolution_clock::now();

    auto duration = duration_cast<microseconds>(stop - start);
    outfile << (double)duration.count() / 1000000.0;

    outfile.close();

    return 0;
}