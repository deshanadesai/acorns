#include <math.h>

double *compute(double values[], int count){

double *ders;
ders = malloc(count * sizeof(*ders));

double k = values[0];
ders[0]= cos(k) * cos(k)*1 + sin(k) * -1*sin(k)*1 + (pow(k,(2-1) * (2 * 1 + k * 0 * log(k)))) + l * 0 + l * 0 - l * 1 + k * 0;

double l = values[1];
ders[1]= cos(k) * cos(k)*0 + sin(k) * -1*sin(k)*0 + (pow(k,(2-1) * (2 * 0 + k * 0 * log(k)))) + l * 1 + l * 1 - l * 0 + k * 1;

return ders; 
}

int main(){

int i, count = 2;
double *ders; 
double values[2] = {4.5,6.4};

ders = compute(values, count);
printf("Printing values: ");
for(i = 0 ; i < count ; i++) { 
		printf("%f ", ders[i]);
	}

free(ders);
printf("\n\n");

return 0;

}