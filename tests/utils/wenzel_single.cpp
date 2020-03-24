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
   typedef Eigen::Matrix<double, 3, 1> Gradient;

   string output_filename = argv[1];
   cout << output_filename << endl;

   typedef DScalar1<double, Gradient> DScalar;

   int num_params = 4010;
   int num_vars = 3;

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
       DiffScalarBase::setVariableCount(3);
		DScalar B(0, args[index * 3 + 0]), a(1, args[index * 3 + 1]), W(2, args[index * 3 + 2]);
		DScalar Fx = 4*4*4*((B * (1 - B))*(a * (1 - a))*(W * (1 - W)));
		ders[index * 3 + 0] = Fx.getGradient()(0);
		ders[index * 3 + 1] = Fx.getGradient()(1);
		ders[index * 3 + 2] = Fx.getGradient()(2);
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