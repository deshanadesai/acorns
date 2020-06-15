#include <stdio.h>
#include <output/test_grad_forward.c>
#include <output/test_grad_reverse.c>
#include <output/test_hessian_forward.c>
#include <output/test_hessian_reverse.c>



int main(){ 
    int size_ders = 2; 
    int hess_size_ders = 3;
    double grad_fwd[size_ders]; 
    double grad_rev[size_ders];
    double hess_fwd[hess_size_ders]; 
    double hess_rev[hess_size_ders]; 
    double values[2] = {2.0, 3.0}; 
    int num_points = 1; 
    
    compute_grad_forward(values, num_points, grad_fwd); 
    compute_grad_reverse(values, num_points, grad_rev); 
    compute_hessian_forward(values, num_points, hess_fwd); 
    compute_hessian_reverse(values, num_points, hess_rev); 
    
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
             
    
   printf("Writing to ./output/files/compute_hess_forward.txt\n");    
   fp = fopen("./output/files/compute_hess_forward.txt", "w+");
   for(int i=0;i<hess_size_ders;i++){ 
     fprintf(fp, "%lf \n", hess_fwd[i]); 
    } 
    fclose(fp);
            
    
   printf("Writing to ./output/files/compute_hess_reverse.txt\n");    
   fp = fopen("./output/files/compute_hess_reverse.txt", "w+");
   for(int i=0;i<hess_size_ders;i++){ 
     fprintf(fp, "%lf \n", hess_rev[i]); 
    } 
    fclose(fp);             
}