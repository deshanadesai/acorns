#include <iostream>
#include <fstream>
#include <string>
#include <Eigen/Cholesky>
#include "headers/autodiff.h"
#include <chrono>

DECLARE_DIFFSCALAR_BASE();
using namespace std;
using namespace std::chrono;
int main(int argc, char **argv)
{
   typedef Eigen::Matrix<double, 1, 1> Gradient;
   typedef Eigen::Matrix<double, 1, 1> Hessian;

   string output_filename = argv[1];
   cout << output_filename << endl;

   typedef DScalar2<double, Gradient, Hessian> DScalar;

   int num_params = 10;
   int num_vars = 1;

   Eigen::VectorXd args(num_params * num_vars);
   Eigen::VectorXd ders(num_params * num_vars);

   std::ifstream file("./tests/utils/params.txt");
   int i = 0;
   for (std::string line; std::getline(file, line);)
   {
       args(i) = stod(line.c_str());
       i++;
   }
   file.close();

   ofstream outfile;
   outfile.open(output_filename);

   auto start = high_resolution_clock::now();
   for (int index = 0; index < num_params; index++)
   {
       /* There are two independent variables */
       DiffScalarBase::setVariableCount(1);
		DScalar k(0, args[index * 1 + 0]);
		DScalar Fx = 4*((k * (1 - k)));
		ders[index * 1 + 0] = Fx.getGradient()(0);
   }

   auto stop = high_resolution_clock::now();
   auto duration = duration_cast<microseconds>(stop - start);
   outfile << (double)duration.count() / 1000000.0 << " ";
   for (int i = 0; i < num_params * num_vars; i++)
   {
        ostringstream ss;
        ss.precision(3);
       ss << fixed << ders[i];
       outfile << ss.str() << " ";
   }

   outfile.close();

   return 0;
}