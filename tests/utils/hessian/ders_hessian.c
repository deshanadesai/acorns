void compute(double values[], int num_points, double ders[]){

	for(int i = 0; i < num_points; ++i)
	{
		double g = values[i* 1 + 0 ];
		ders[i*1+0]= (((0 * (((1 - g) * (1) + g * (((0) - (1))))) + (g * (1 - g)) * (0))) + (((((1 - g) * 1) + (g * (0 - 1))) * (0) + 4 * ((((1 * (((0) - (1))) + (1 - g) * (0))) + (((0 - 1) * (1) + g * (((0) - (0)))))))))); // df/(dgdg) 
	}
}

