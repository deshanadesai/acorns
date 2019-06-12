#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#define N 1000
 #define num_vars 1
void compute(double values[], int num_points, double ders[]){

	for(int i = 0; i < num_points; ++i)
	{
		double k = values[i* 1 + 0 ];
		ders[i*1+0]= (((k * (((((k * (1) + k * (1))) + ((k * (0) + 3 * (1))))) - ((4 * 1 - k * 0)/ (4 * 4))) - (((k * k) + (3 * k)) - (k / 4)) * 1)/ (k * k)) + ((k * ((k * ((k * (1) + k * (1))) + (k * k) * (1))) + ((k * k) * k) * (1))));
	}
}

void read_file_to_array(char* filename, double *args) {
    FILE *file = fopen (filename, "r" );

    if ( file != NULL ) {


    char line [ 200 ]; 
    int i = 0;        

    for(int i=0;i<N*num_vars;i++){
        fscanf(file, "%lf", &args[i]);
//        printf("%f ", args[i]);
    }

    fclose ( file );
    } else {
    	perror ( filename ); /* why didn't the file open? */
    }
}
int main() {
	double values[N*num_vars];
	double ders[N*num_vars];
	char variable[] = "utils/params.txt"; 
	read_file_to_array(variable, values);

	struct timespec tstart={0,0}, tend={0,0};
    struct timeval stop, start;
    clock_gettime(CLOCK_MONOTONIC, &tstart);
	
    compute(values, N, ders);


	clock_gettime(CLOCK_MONOTONIC, &tend);
	double delta = ((double)tend.tv_sec + 1.0e-9*tend.tv_nsec) - ((double)tstart.tv_sec + 1.0e-9*tstart.tv_nsec);
    printf("%f ", delta);
	FILE *fp;

	fp = fopen("utils/output.txt", "w+");

    fprintf(fp, "%f ", delta);
	for(int i = 0; i < N*num_vars; i++) {
        fprintf(fp, "%f ", ders[i]);
    }
	fclose(fp);
	return 0;
}
	