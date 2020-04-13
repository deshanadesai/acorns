void compute(double values[], int num_points, double ders[]){

	for(int i = 0; i < num_points; ++i)
	{
		double k = values[i* 1 + 0 ];
		ders[i*1+0]= (((((cos(k)*1)) + ((-1*sin(k)*1)))) + ((pow(k,(2-1)) * (2 * 1 + k * 0 * log(k))))); // df/(k) 
	}
}

