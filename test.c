#include <sys/time.h>
#include <stdio.h>
int main() {  
    struct timeval tv;
    gettimeofday(&tv, NULL); // timezone should be NULL
    printf("%d seconds\n", tv.tv_sec);
    return 0;
}