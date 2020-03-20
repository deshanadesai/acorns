void compute(double values[], int num_points, double ders[]){

	for(int i = 0; i < num_points; ++i)
	{
		double K = values[i* 2 + 0 ];
		double L = values[i* 2 + 1 ];
		ders[i*2+0]= (((K * (1 - K)) * (L * (1 - L))) * ((4 * (0) + 4 * (0))) + (4 * 4) * (((L * (1 - L)) * (((1 - K) * (1) + K * (((0) - (1))))) + (K * (1 - K)) * (((1 - L) * (0) + L * (((0) - (0)))))))); // df/(K) 
		ders[i*2+1]= (((K * (1 - K)) * (L * (1 - L))) * ((4 * (0) + 4 * (0))) + (4 * 4) * (((L * (1 - L)) * (((1 - K) * (0) + K * (((0) - (0))))) + (K * (1 - K)) * (((1 - L) * (1) + L * (((0) - (1)))))))); // df/(L) 
	}
}

