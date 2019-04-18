#include <math.h>

void f(char * restrict joe){}

double to_diff(double k,double l)
{
    unsigned int long c = 4;
    double p = sin(k)*cos(k)+pow(k,2);
    return p;
}

int main(){
    double k = 4.0;
    double l = 5.6;
    to_diff(k,l);
}
