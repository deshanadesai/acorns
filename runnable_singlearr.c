#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include "objs/derivatives_ispc.h"

#define N 100000
// void compute(double **values, long num_points, double **ders){

//     for(int i = 0; i < num_points; ++i)
//     {
//         double k = values[i][0];
//         ders[i][0]= cos(k) * cos(k)*1 + sin(k) * -1*sin(k)*1 + (pow(k,(2-1)) * (2 * 1 + k * 0 * log(k)));
//     }
// }



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
    printf("starting program");
    double values[N];
    // for (int i=0; i<N; i++) 
    //      args[i] = (double *)malloc(1 * sizeof(double));   
    printf("initialized first array"); 
    double ders[N];
//    for (int i=0; i<N; i++)
//         ders[i] = (double *)malloc(1 * sizeof(double));

    printf("reading file");
    char variable[] = "params.txt"; 
    // printf("Please enter the file name of the C program for scanning: ");
    // scanf("%s",variable);
    read_file_to_array(variable, values);
    printf("computing things");


    for(int i=0;i<N;i++){
        printf("%lf ", values[i]);
    }      

	  struct timespec tstart={0,0}, tend={0,0};
    struct timeval stop, start;
    clock_gettime(CLOCK_MONOTONIC, &tstart);
	
    compute(values, N, ders);


	clock_gettime(CLOCK_MONOTONIC, &tend);
	double delta = ((double)tend.tv_sec + 1.0e-9*tend.tv_nsec) - ((double)tstart.tv_sec + 1.0e-9*tstart.tv_nsec);
    printf("%f ", delta);

//   for(int i = 0; i < N; i++) {
//       printf("%f ", ders[i]);
//   }
   FILE *fp;

   fp = fopen("output.txt", "w");

   fprintf(fp, "%f ", delta);
   for(int i = 0; i < N; i++) {
       fprintf(fp, "%f ", ders[i]);
   }
   fclose(fp);
	return 0;
}
	
