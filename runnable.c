#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#define N 10
void compute(const double values[][2], long num_points, double ders[][2]){

	for(int i = 0; i < num_points; ++i)
	{
		double k = values[i][0];
		ders[i][0]= cos(k) * cos(k)*1 + sin(k) * -1*sin(k)*1 + (pow(k,(2-1)) * (2 * 1 + k * 0 * log(k)));
	}
}


int main(int argc, char *argv[]) {
	double args[N][2];
	for(int i = 0; i < N; i++) {
		args[i][0] = atof(argv[i]);
	}
	long num_points = ((int) (sizeof (args) / sizeof (args)[0]));

	double ders[N][2];

	struct timespec tstart={0,0}, tend={0,0};
    clock_gettime(CLOCK_MONOTONIC, &tstart);
	struct timeval stop, start;
	compute(args, num_points, ders);
	clock_gettime(CLOCK_MONOTONIC, &tend);
	double delta = ((double)tend.tv_sec + 1.0e-9*tend.tv_nsec) - ((double)tstart.tv_sec + 1.0e-9*tstart.tv_nsec);
	FILE *fp;

	fp = fopen("output.txt", "w+");

    fprintf(fp, "%f ", delta);
	for(int i = 0; i < ( (int) sizeof(ders) / sizeof(ders[0]) ); i++) {
        fprintf(fp, "%f ", ders[i][0]);
    }
	fclose(fp);
	return 0;
}
	