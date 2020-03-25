void compute(double values[], int num_points, double ders[]){

	for(int i = 0; i < num_points; ++i)
	{
		double a = values[i* 2 + 0 ];
		double p = values[i* 2 + 1 ];
		ders[i*2+0]= (((((p * ((a * ((a * ((a * (1) + a * (1))) + (a * a) * (1))) + ((a * a) * a) * (1))) + (((a * a) * a) * a) * (0))) + (((p * p) * 0 - 1 * (p * (0) + p * (0)))/ ((p * p) * (p * p))))) - ((a * (p * ((p * 0 - 1 * 0)/ (p * p)) + (1 / p) * (0)) - ((1 / p) * p) * 1)/ (a * a))); // df/(a) 
		ders[i*2+1]= (((((p * ((a * ((a * ((a * (0) + a * (0))) + (a * a) * (0))) + ((a * a) * a) * (0))) + (((a * a) * a) * a) * (1))) + (((p * p) * 0 - 1 * (p * (1) + p * (1)))/ ((p * p) * (p * p))))) - ((a * (p * ((p * 0 - 1 * 1)/ (p * p)) + (1 / p) * (1)) - ((1 / p) * p) * 0)/ (a * a))); // df/(p) 
	}
}


 int main(){ 
    int size_ders = 2; 
    double ders[size_ders]; 
    double values[2] = {2.0, 3.0}; 
    int num_points = 1; 
    compute(&values, num_points, &ders); 
    for(int i=0;i<size_ders;i++){ 
      printf("%lf \n", ders[i]);   
     } 
 }
