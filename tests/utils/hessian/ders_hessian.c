void compute(double values[], int num_points, double ders[]){

	for(int i = 0; i < num_points; ++i)
	{
		double D = values[i* 1 + 0 ];
		ders[i*1+0]= (((0 * (((1 - D) * (1) + D * (((0) - (1))))) + (D * (1 - D)) * (0))) + (((((1 - D) * 1) + (D * (0 - 1))) * (0) + 4 * ((((1 * (((0) - (1))) + (1 - D) * (0))) + (((0 - 1) * (1) + D * (((0) - (0)))))))))); // df/(dDdD) 
	}
}

