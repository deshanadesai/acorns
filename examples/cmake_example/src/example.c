#include <stdio.h>
#include "../ders/der_1.h"

int main(int argc, char* argv) {

    int num_vars = 1;
    int num_pts = 10;
    double vals[10] = {1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0};
    double ders[10] = {0};

    compute(vals, num_pts, ders);

    for(int i = 0; i < num_vars * num_pts; i++) {
        printf("Ders[%d]: %f\n", i, ders[i]);
    }

    return 0;

}