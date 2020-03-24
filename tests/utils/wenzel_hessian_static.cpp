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
   typedef Eigen::Matrix<double, 9, 1> Gradient;
   typedef Eigen::Matrix<double, 9, 9> Hessian;

   string output_filename = argv[1];
   cout << output_filename << endl;

   typedef DScalar2<double, Gradient, Hessian> DScalar;

   int num_params = 8010;
   int num_vars = 9;
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
       DiffScalarBase::setVariableCount(9);
		DScalar Q(0, args[index * 9 + 0]), K(1, args[index * 9 + 1]), l(2, args[index * 9 + 2]), M(3, args[index * 9 + 3]), a(4, args[index * 9 + 4]), z(5, args[index * 9 + 5]), g(6, args[index * 9 + 6]), N(7, args[index * 9 + 7]), k(8, args[index * 9 + 8]);
		DScalar Fx = 4*4*4*4*4*4*4*4*4*((Q * (1 - Q))*(K * (1 - K))*(l * (1 - l))*(M * (1 - M))*(a * (1 - a))*(z * (1 - z))*(g * (1 - g))*(N * (1 - N))*(k * (1 - k)));
		ders[index * 81 + 0] = Fx.getHessian()(0);
		ders[index * 81 + 1] = Fx.getHessian()(1);
		ders[index * 81 + 2] = Fx.getHessian()(2);
		ders[index * 81 + 3] = Fx.getHessian()(3);
		ders[index * 81 + 4] = Fx.getHessian()(4);
		ders[index * 81 + 5] = Fx.getHessian()(5);
		ders[index * 81 + 6] = Fx.getHessian()(6);
		ders[index * 81 + 7] = Fx.getHessian()(7);
		ders[index * 81 + 8] = Fx.getHessian()(8);
		ders[index * 81 + 9] = Fx.getHessian()(10);
		ders[index * 81 + 10] = Fx.getHessian()(11);
		ders[index * 81 + 11] = Fx.getHessian()(12);
		ders[index * 81 + 12] = Fx.getHessian()(13);
		ders[index * 81 + 13] = Fx.getHessian()(14);
		ders[index * 81 + 14] = Fx.getHessian()(15);
		ders[index * 81 + 15] = Fx.getHessian()(16);
		ders[index * 81 + 16] = Fx.getHessian()(17);
		ders[index * 81 + 17] = Fx.getHessian()(20);
		ders[index * 81 + 18] = Fx.getHessian()(21);
		ders[index * 81 + 19] = Fx.getHessian()(22);
		ders[index * 81 + 20] = Fx.getHessian()(23);
		ders[index * 81 + 21] = Fx.getHessian()(24);
		ders[index * 81 + 22] = Fx.getHessian()(25);
		ders[index * 81 + 23] = Fx.getHessian()(26);
		ders[index * 81 + 24] = Fx.getHessian()(30);
		ders[index * 81 + 25] = Fx.getHessian()(31);
		ders[index * 81 + 26] = Fx.getHessian()(32);
		ders[index * 81 + 27] = Fx.getHessian()(33);
		ders[index * 81 + 28] = Fx.getHessian()(34);
		ders[index * 81 + 29] = Fx.getHessian()(35);
		ders[index * 81 + 30] = Fx.getHessian()(40);
		ders[index * 81 + 31] = Fx.getHessian()(41);
		ders[index * 81 + 32] = Fx.getHessian()(42);
		ders[index * 81 + 33] = Fx.getHessian()(43);
		ders[index * 81 + 34] = Fx.getHessian()(44);
		ders[index * 81 + 35] = Fx.getHessian()(50);
		ders[index * 81 + 36] = Fx.getHessian()(51);
		ders[index * 81 + 37] = Fx.getHessian()(52);
		ders[index * 81 + 38] = Fx.getHessian()(53);
		ders[index * 81 + 39] = Fx.getHessian()(60);
		ders[index * 81 + 40] = Fx.getHessian()(61);
		ders[index * 81 + 41] = Fx.getHessian()(62);
		ders[index * 81 + 42] = Fx.getHessian()(70);
		ders[index * 81 + 43] = Fx.getHessian()(71);
		ders[index * 81 + 44] = Fx.getHessian()(80);
		ders[index * 81 + 45] = Fx.getHessian()(9);
		ders[index * 81 + 46] = Fx.getHessian()(18);
		ders[index * 81 + 47] = Fx.getHessian()(19);
		ders[index * 81 + 48] = Fx.getHessian()(27);
		ders[index * 81 + 49] = Fx.getHessian()(28);
		ders[index * 81 + 50] = Fx.getHessian()(29);
		ders[index * 81 + 51] = Fx.getHessian()(36);
		ders[index * 81 + 52] = Fx.getHessian()(37);
		ders[index * 81 + 53] = Fx.getHessian()(38);
		ders[index * 81 + 54] = Fx.getHessian()(39);
		ders[index * 81 + 55] = Fx.getHessian()(45);
		ders[index * 81 + 56] = Fx.getHessian()(46);
		ders[index * 81 + 57] = Fx.getHessian()(47);
		ders[index * 81 + 58] = Fx.getHessian()(48);
		ders[index * 81 + 59] = Fx.getHessian()(49);
		ders[index * 81 + 60] = Fx.getHessian()(54);
		ders[index * 81 + 61] = Fx.getHessian()(55);
		ders[index * 81 + 62] = Fx.getHessian()(56);
		ders[index * 81 + 63] = Fx.getHessian()(57);
		ders[index * 81 + 64] = Fx.getHessian()(58);
		ders[index * 81 + 65] = Fx.getHessian()(59);
		ders[index * 81 + 66] = Fx.getHessian()(63);
		ders[index * 81 + 67] = Fx.getHessian()(64);
		ders[index * 81 + 68] = Fx.getHessian()(65);
		ders[index * 81 + 69] = Fx.getHessian()(66);
		ders[index * 81 + 70] = Fx.getHessian()(67);
		ders[index * 81 + 71] = Fx.getHessian()(68);
		ders[index * 81 + 72] = Fx.getHessian()(69);
		ders[index * 81 + 73] = Fx.getHessian()(72);
		ders[index * 81 + 74] = Fx.getHessian()(73);
		ders[index * 81 + 75] = Fx.getHessian()(74);
		ders[index * 81 + 76] = Fx.getHessian()(75);
		ders[index * 81 + 77] = Fx.getHessian()(76);
		ders[index * 81 + 78] = Fx.getHessian()(77);
		ders[index * 81 + 79] = Fx.getHessian()(78);
		ders[index * 81 + 80] = Fx.getHessian()(79);

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