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
   typedef Eigen::Matrix<double, 17, 1> Gradient;

   string output_filename = argv[1];
   cout << output_filename << endl;

   typedef DScalar1<double, Gradient> DScalar;

   int num_params = 8010;
   int num_vars = 17;

   Eigen::VectorXd args(num_params * num_vars);
   Eigen::VectorXd ders(num_params * num_vars);

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
       DiffScalarBase::setVariableCount(17);
		DScalar t(0, args[index * 17 + 0]), U(1, args[index * 17 + 1]), w(2, args[index * 17 + 2]), K(3, args[index * 17 + 3]), x(4, args[index * 17 + 4]), B(5, args[index * 17 + 5]), F(6, args[index * 17 + 6]), R(7, args[index * 17 + 7]), u(8, args[index * 17 + 8]), E(9, args[index * 17 + 9]), Z(10, args[index * 17 + 10]), Y(11, args[index * 17 + 11]), k(12, args[index * 17 + 12]), l(13, args[index * 17 + 13]), A(14, args[index * 17 + 14]), V(15, args[index * 17 + 15]), N(16, args[index * 17 + 16]);
		DScalar Fx = 4*4*4*4*4*4*4*4*4*4*4*4*4*4*4*4*4*((t * (1 - t))*(U * (1 - U))*(w * (1 - w))*(K * (1 - K))*(x * (1 - x))*(B * (1 - B))*(F * (1 - F))*(R * (1 - R))*(u * (1 - u))*(E * (1 - E))*(Z * (1 - Z))*(Y * (1 - Y))*(k * (1 - k))*(l * (1 - l))*(A * (1 - A))*(V * (1 - V))*(N * (1 - N)));
		ders[index * 17 + 0] = Fx.getGradient()(0);
		ders[index * 17 + 1] = Fx.getGradient()(1);
		ders[index * 17 + 2] = Fx.getGradient()(2);
		ders[index * 17 + 3] = Fx.getGradient()(3);
		ders[index * 17 + 4] = Fx.getGradient()(4);
		ders[index * 17 + 5] = Fx.getGradient()(5);
		ders[index * 17 + 6] = Fx.getGradient()(6);
		ders[index * 17 + 7] = Fx.getGradient()(7);
		ders[index * 17 + 8] = Fx.getGradient()(8);
		ders[index * 17 + 9] = Fx.getGradient()(9);
		ders[index * 17 + 10] = Fx.getGradient()(10);
		ders[index * 17 + 11] = Fx.getGradient()(11);
		ders[index * 17 + 12] = Fx.getGradient()(12);
		ders[index * 17 + 13] = Fx.getGradient()(13);
		ders[index * 17 + 14] = Fx.getGradient()(14);
		ders[index * 17 + 15] = Fx.getGradient()(15);
		ders[index * 17 + 16] = Fx.getGradient()(16);
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