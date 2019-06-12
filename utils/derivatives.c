void compute(double values[], int num_points, double ders[]){

	for(int i = 0; i < num_points; ++i)
	{
		double k = values[i* 1 + 0 ];
		ders[i*1+0]= (((k * (((((k * (1) + k * (1))) + ((k * (0) + 3 * (1))))) - ((4 * 1 - k * 0)/ (4 * 4))) - (((k * k) + (3 * k)) - (k / 4)) * 1)/ (k * k)) + ((k * ((k * ((k * (1) + k * (1))) + (k * k) * (1))) + ((k * k) * k) * (1))));
	}
}

