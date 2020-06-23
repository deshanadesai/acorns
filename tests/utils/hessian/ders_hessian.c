void compute(double values[], int num_points, double ders[]){

	for(int i = 0; i < num_points; ++i)
	{
		double k = values[i* 1 + 0 ];
		ders[i*1+0]= (((((1 * ((-1*sin(k)*1)) + (cos(k)) * (0))) + ((1 * (((sin(k)) * ((-(0))) + ( -(1)) * ((cos(k)*1)))) + (( -(1)) * (sin(k))) * (0))))) + ((((2 * 1) + ((k * 0) * (log(k)))) * ((pow(k,((2 - 1)-1)) * ((2 - 1) * 1 + k * 0 * log(k)))) + (pow(k,(2 - 1))) * ((((1 * (0) + 2 * (0))) + (((log(k)) * ((0 * (1) + k * (0))) + (k * 0) * ((1/(k)*1))))))))); // df/(dkdk) 
	}
}

