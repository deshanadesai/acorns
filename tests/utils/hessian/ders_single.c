void compute(double values[], int num_points, double ders[]){

	for(int i = 0; i < num_points; ++i)
	{
		double R = values[i* 1 + 0 ];
		ders[i*1+0]= ((R * (1 - R)) * (0) + 4 * (((1 - R) * (1) + R * (((0) - (1)))))); // df/(R) 
	}
}

