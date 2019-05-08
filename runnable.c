#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#define N 10
void compute(double **values, long num_points, double **ders){

	for(int i = 0; i < num_points; ++i)
	{
		double k = values[i][0];
		ders[i][0]= cos(k) * cos(k)*1 + sin(k) * -1*sin(k)*1 + (pow(k,(2-1)) * (2 * 1 + k * 0 * log(k)));
	}
}

void read_file_to_array(char* filename, double **args) {
    FILE *file = fopen ( filename, "r" );
    if ( file != NULL ) {
    	char line [ 200 ]; 
   		int i = 0;
    	while ( fgets ( line, sizeof line, file ) != NULL )  {
      		args[i][0] = atof(line);
      		i++;
        }
        fclose ( file );
    } else {
    	perror ( filename ); /* why didn't the file open? */
    }
}
int main(int argc, char *argv[]) {
	double **args = malloc(N * sizeof(double *));
	double **ders = malloc(N * sizeof(double *));
	for(int i = 0; i < N; i++) {
   		args[i] = malloc(2 * sizeof(double));
   		ders[i] = malloc(2 * sizeof(double));
	}

	read_file_to_array(argv[1], args);
	compute(args, (long) N, ders);
	struct timespec tstart={0,0}, tend={0,0};
    clock_gettime(CLOCK_MONOTONIC, &tstart);
	struct timeval stop, start;
	compute(args, (long) N, ders);
	clock_gettime(CLOCK_MONOTONIC, &tend);
	double delta = ((double)tend.tv_sec + 1.0e-9*tend.tv_nsec) - ((double)tstart.tv_sec + 1.0e-9*tstart.tv_nsec);
	FILE *fp;

	fp = fopen("us_output.txt", "w+");

    fprintf(fp, "%f ", delta);
	for(int i = 0; i < N; i++) {
        fprintf(fp, "%f ", ders[i][0]);
    }
	fclose(fp);
	return 0;
}
	