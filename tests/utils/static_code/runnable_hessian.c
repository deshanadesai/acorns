#ifdef _WIN32
#include <windows.h>
#endif

#include <math.h>
#include <stdlib.h>
#include <inttypes.h>
#include <time.h>
#include <stdio.h>
#include <stdint.h>
#include "../headers/derivatives_hessian.h"

void read_file_to_array(char *filename, double *args, int num_params, int num_vars)
{
    FILE *file = fopen(filename, "r");

    if (file != NULL)
    {

        char line[200];
        int i = 0;

        for (int i = 0; i < num_params * num_vars; i++)
        {
            fscanf(file, "%lf", &args[i]);
        }

        fclose(file);
    }
    else
    {
        perror(filename); /* why didn't the file open? */
    }
}

/*
    Expects command line arguments: num_params num_vars params_filename output_filename
*/
int main(int argc, char *argv[])
{

    printf("I am running...");

    // read command line arguments
    char *ptr;

    int num_params = (int)strtol(argv[1], &ptr, 10);
    int num_vars = (int)strtol(argv[2], &ptr, 10);
    int num_ders = (num_vars * num_vars);
    char *params_filename = argv[3];
    char *output_filename = argv[4];

    double *values = malloc(num_params * num_vars * sizeof(double));
    double *ders = malloc(num_params * num_ders * sizeof(double));

    read_file_to_array(params_filename, values, num_params, num_vars);

#ifdef _WIN32

    LARGE_INTEGER StartingTime, EndingTime, ElapsedMicroseconds;
    LARGE_INTEGER Frequency;

    QueryPerformanceFrequency(&Frequency);
    QueryPerformanceCounter(&StartingTime);

    // Activity to be timed
    compute(values, num_params, ders);

    QueryPerformanceCounter(&EndingTime);
    ElapsedMicroseconds.QuadPart = EndingTime.QuadPart - StartingTime.QuadPart;

    // ElapsedMicroseconds.QuadPart *= 1000000;
    // ElapsedMicroseconds.QuadPart /= Frequency.QuadPart;

    double delta = (ElapsedMicroseconds.QuadPart) / (double)Frequency.QuadPart; // seconds

#else
    struct timespec tstart = {0, 0}, tend = {0, 0};
    clock_gettime(CLOCK_MONOTONIC, &tstart);
    compute(values, num_params, ders);
    clock_gettime(CLOCK_MONOTONIC, &tend);
    double delta = ((double)tend.tv_sec + 1.0e-9 * tend.tv_nsec) - ((double)tstart.tv_sec + 1.0e-9 * tstart.tv_nsec); // seconds
#endif

    FILE *fp;

    fp = fopen(output_filename, "w+");
    printf("Time: %f ", delta);
    fprintf(fp, "%f ", delta);

    for (int i = 0; i < num_params * num_ders; i++)
    {
        fprintf(fp, "%f ", ders[i]);
        // printf("\nUs: %f", ders[i]);
    }
    fclose(fp);
    return 0;
}
