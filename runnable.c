#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>
void compute(const double values[][2], long num_points, double ders[][2]){

	for(int i = 0; i < num_points; ++i)
	{
		double k = values[i][0];
		ders[i][0]= cos(k) * cos(k)*1 + sin(k) * -1*sin(k)*1 + (pow(k,(2-1)) * (2 * 1 + k * 0 * log(k)));
	}
}


int main(int argc, char *argv[]) {
	double args[argc-1][2];
	for(int i = 1; i < argc; i++) {
		args[i-1][0] = atof(argv[i]);
	}
		long num_points = ((int) (sizeof (args) / sizeof (args)[0]));

	double ders[1000][2];

	struct timeval stop, start;
	gettimeofday(&start, NULL);
	long long start_ms = (((long long)start.tv_sec)*1000)+(start.tv_usec/1000);
	compute(args, num_points, ders);
	gettimeofday(&stop, NULL);
	long long stop_ms = (((long long)stop.tv_sec)*1000)+(stop.tv_usec/1000);
	printf("start: %lu", start_ms);
	printf("stop: %lu", stop_ms);
	long long delta = stop_ms - start_ms;
	FILE *fp;

	fp = fopen("output.txt", "w+");

    fprintf(fp, "%lu ", delta);
	for(int i = 0; i < ( (int) sizeof(ders) / sizeof(ders[0]) ); i++) {
        fprintf(fp, "%f ", ders[i][0]);
    }
	fclose(fp);
	return 0;
}
	