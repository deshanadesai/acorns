#include <der_0.h>
#include <stdio.h>
#include <math.h>

int main(int argc, char** argv) {

    int num_vars = 1;
    float step_size = 0.01;
    float step_tolerance = 0.00001;
    int max_iterations = 10000;

    double vals[1] = {6.0};
    double ders[1] = {0.0};
    int num_pts = 1;
    int iteration = 0;

    for (int i = 0; i < max_iterations; i++) {

        iteration = i;

        // calculate derivative
        compute(vals, num_pts, ders);

        float step = step_size * ders[0];
        vals[0] -= step;

        if (fabs(step) <= step_tolerance)
            break;
    }

    printf("Minimum: %f\n", vals[0]);
    printf("Iterations: %d\n", iteration);
    return 0;
}