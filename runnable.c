#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include "objs/derivatives_ispc.h"
#define N 100000
void read_file_to_array(char* filename, double *args) {
    FILE *file = fopen (filename, "r" );

    if ( file != NULL ) {


    char line [ 200 ]; 
    int i = 0;        

    for(int i=0;i<N;i++){
        fscanf(file, "%lf", &args[i]);
//        printf("%f ", args[i]);
    }

    fclose ( file );
    } else {
    	perror ( filename ); /* why didn't the file open? */
    }
}
int main() {
	double values[N];
	double ders[N];
	char variable[] = "params.txt"; 
	read_file_to_array(variable, values);

	struct timespec tstart={0,0}, tend={0,0};
    struct timeval stop, start;
    clock_gettime(CLOCK_MONOTONIC, &tstart);
	
    compute(values, N, ders);


	clock_gettime(CLOCK_MONOTONIC, &tend);
	double delta = ((double)tend.tv_sec + 1.0e-9*tend.tv_nsec) - ((double)tstart.tv_sec + 1.0e-9*tstart.tv_nsec);
    printf("%f ", delta);
	FILE *fp;

	fp = fopen("us_output.txt", "w+");

    fprintf(fp, "%f ", delta);
	for(int i = 0; i < N; i++) {
        fprintf(fp, "%f ", ders[i]);
    }
	fclose(fp);
	return 0;
}
	
