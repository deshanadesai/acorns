#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>
  
#define N 1000000
void compute(double **values, long num_points, double **ders){

	for(int i = 0; i < num_points; ++i)
	{
		double k = values[i][0];
		ders[i][0]= cos(k) * cos(k)*1 + sin(k) * -1*sin(k)*1 + (pow(k,(2-1)) * (2 * 1 + k * 0 * log(k)));
	}
}

int main() {
	double **array1 = malloc(N * sizeof(double *));
	double **array2 = malloc(N * sizeof(double *));
	for(int i = 0; i < N; i++) {
   		array1[i] = malloc(2 * sizeof(double));
   		array2[i] = malloc(2 * sizeof(double));
	}

	for(int i = 0; i < N; i++) {
		array1[i][0] = 4.0;
	} 

	compute(array1, (long) N, array2);

	for(int i = 0; i < N; i++) {
        printf("%f\n", array2[i][0]);
    }

    return 0;
}