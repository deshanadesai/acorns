#include <math.h>

void f(char * restrict joe){}

int main(void)
{
    unsigned int long k = 4;
    int p = sin(k)*cos(k)+pow(k,2);
    return 0;
}
