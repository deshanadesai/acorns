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
   int num_params = 2010;
   int num_vars = 2;
   Eigen::VectorXd args(num_params * num_vars);
   Eigen::VectorXd ders(num_params * num_vars);
   std::ifstream file("utils/params.txt");
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
       DiffScalarBase::setVariableCount(2);
		DScalar k(0, args[index * 2 + 0]), j(1, args[index * 2 + 1]);
		DScalar Fx = ((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k*j;
		ders[index * 2 + 0] = Fx.getGradient()(0);
		ders[index * 2 + 1] = Fx.getGradient()(1);
   }
   auto stop = high_resolution_clock::now();
   auto duration = duration_cast<microseconds>(stop - start);
   outfile << (double)duration.count() / 1000000.0 << " ";
   for (int i = 0; i < num_params * num_vars; i++)
   {
       outfile << ders[i] << " ";
   }
   outfile.close();
   return 0;
}