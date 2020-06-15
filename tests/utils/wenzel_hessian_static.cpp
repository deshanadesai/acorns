#include <iostream>
#include <fstream>
#include <string>
#include <Eigen/Cholesky>
#include "../headers/autodiff.h"
#include <chrono>

DECLARE_DIFFSCALAR_BASE();
using namespace std;
using namespace std::chrono;
int main(int argc, char **argv)
{
   typedef Eigen::Matrix<double, 2, 1> Gradient;
   typedef Eigen::Matrix<double, 2, 2> Hessian;

   string output_filename = argv[1];
   cout << output_filename << endl;

   typedef DScalar2<double, Gradient, Hessian> DScalar;

   int num_params = 6010;
   int num_vars = 2;
   int num_ders = num_vars * num_vars;

   Eigen::VectorXd args(num_params * num_vars);
   Eigen::VectorXd ders(num_params * num_ders);

   std::ifstream file("./tests/utils/hessian/params.txt");
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
		ders[index * 4 + 0] = Fx.getHessian()(0);
		ders[index * 4 + 1] = Fx.getHessian()(1);
		ders[index * 4 + 2] = Fx.getHessian()(3);
		ders[index * 4 + 3] = Fx.getHessian()(2);

   }

   auto stop = high_resolution_clock::now();
   auto duration = duration_cast<microseconds>(stop - start);
   outfile << (double)duration.count() / 1000000.0 << " ";
   for (int i = 0; i < num_ders * num_params; i++)
   {
        ostringstream ss;
        ss.precision(3);
       ss << fixed << ders[i];
       outfile << ss.str() << " ";
   }

   outfile.close();

   return 0;
}