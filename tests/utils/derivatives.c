void compute(double values[], int num_points, double ders[]){

	for(int i = 0; i < num_points; ++i)
	{
		double T = values[i* 1 + 0 ];
		ders[i*1+0]= ((T * (1 - T)) * (0) + 4 * (((1 - T) * (1) + T * (((0) - (1)))))); // df/(T) 
	}
}

