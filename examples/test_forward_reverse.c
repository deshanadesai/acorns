#include <stdio.h>
#include <output/test_grad_forward.c>
#include <output/test_grad_reverse.c>



int main(){ 
    int size_ders = 1; 
    int hess_size_ders = 3;
    double grad_fwd[size_ders]; 
    double grad_rev[size_ders];

    double values[1] = {0.5}; 
    int num_points = 1; 
    
    compute_grad_forward(values, num_points, grad_fwd); 
    compute_grad_reverse(values, num_points, grad_rev); 
    
   FILE *fp;
   
   printf("Writing to ./output/files/compute_grad_forward.txt\n");
   fp = fopen("./output/files/compute_grad_forward.txt", "w+");
   for(int i=0;i<size_ders;i++){ 
     fprintf(fp, "%lf \n", grad_fwd[i]); 
    } 
    fclose(fp);
    
             
   printf("Writing to ./output/files/compute_grad_reverse.txt\n");             
   fp = fopen("./output/files/compute_grad_reverse.txt", "w+");
   for(int i=0;i<size_ders;i++){ 
     fprintf(fp, "%lf \n", grad_rev[i]); 
    } 
    fclose(fp);
    
}