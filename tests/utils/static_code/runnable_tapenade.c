#ifdef _WIN32
    #include <windows.h>
#endif

#include <math.h>
#include <stdlib.h>
#include <inttypes.h>
#include <time.h>
#include <stdio.h>
#include <stdint.h>

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

void function_0_b(double a, double *ab, double b, double *bb, double c, double *cb, double d, double *db, double function_0b)
{
    double p = 0;
    double pb = 0.0;
    double temp;
    double temp0;
    double tempb;
    double tempb0;
    double function_0;
    pb = function_0b;
    temp = a * d - b * c;
    temp0 = 1.0 / temp;
    tempb = (temp0 + 1) * pb;
    tempb0 = -(temp0 * (a * a + b * b + c * c + d * d) * pb / temp);
    *ab = *ab + d * tempb0 + 2 * a * tempb;
    *db = *db + a * tempb0 + 2 * d * tempb;
    *bb = *bb + 2 * b * tempb - c * tempb0;
    *cb = *cb + 2 * c * tempb - b * tempb0;
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
    char *params_filename = argv[3];
    char *output_filename = argv[4];

    double *values = malloc(num_params * num_vars * sizeof(double));
    double *ders = malloc(num_params * num_vars * sizeof(double));

    read_file_to_array(params_filename, values, num_params, num_vars);

#ifdef _WIN32

    LARGE_INTEGER StartingTime, EndingTime, ElapsedMicroseconds;
    LARGE_INTEGER Frequency;

    QueryPerformanceFrequency(&Frequency);
    QueryPerformanceCounter(&StartingTime);

    // Activity to be timed

    // compute(values, num_params, ders);

    QueryPerformanceCounter(&EndingTime);
    ElapsedMicroseconds.QuadPart = EndingTime.QuadPart - StartingTime.QuadPart;

    // ElapsedMicroseconds.QuadPart *= 1000000;
    // ElapsedMicroseconds.QuadPart /= Frequency.QuadPart;

    double delta = (ElapsedMicroseconds.QuadPart) / (double)Frequency.QuadPart; // seconds

#else
    struct timespec tstart = {0, 0}, tend = {0, 0};
    clock_gettime(CLOCK_MONOTONIC, &tstart);
    for (int i = 0; i < num_params; i++) {
        double a = values[i* 4 + 0];
        double ab = 0;
        double b = values[i* 4 + 1];
        double bb = 0;
        double c = values[i* 4 + 2];
        double cb = 0;
        double d = values[i* 4 + 3];
        double db = 0;
        double function_0b = 1;
        function_0_b(a, &ab, b, &bb, c, &cb, d, &db, function_0b);
        ders[i * 4 + 0] = ab;
        ders[i * 4 + 1] = bb;
        ders[i * 4 + 2] = cb;
        ders[i * 4 + 3] = db;
    }
    clock_gettime(CLOCK_MONOTONIC, &tend);
    double delta = ((double)tend.tv_sec + 1.0e-9 * tend.tv_nsec) - ((double)tstart.tv_sec + 1.0e-9 * tstart.tv_nsec); // seconds
#endif

    FILE *fp;

    fp = fopen(output_filename, "w+");
    // printf("%f ", delta);
    fprintf(fp, "%f ", delta);

    for (int i = 0; i < num_params * num_vars; i++)
    {
        fprintf(fp, "%f ", ders[i]);
        // printf("%f", ders[i]);
    }
    fclose(fp);
    return 0;
}