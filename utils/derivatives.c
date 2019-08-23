void compute(double values[], int num_points, double ders[]){

	for(int i = 0; i < num_points; ++i)
	{
		double k = values[i* 3 + 0 ];
		double j = values[i* 3 + 1 ];
		double l = values[i* 3 + 2 ];
		ders[i*3+0]= (((((cos(k)*1)) + ((-1*sin(j)*0)))) + ((pow(l,(2-1)) * (2 * 0 + l * 0 * log(l)))));
		ders[i*3+1]= (((((cos(k)*0)) + ((-1*sin(j)*1)))) + ((pow(l,(2-1)) * (2 * 0 + l * 0 * log(l)))));
		ders[i*3+2]= (((((cos(k)*0)) + ((-1*sin(j)*0)))) + ((pow(l,(2-1)) * (2 * 1 + l * 0 * log(l)))));
	}
}

