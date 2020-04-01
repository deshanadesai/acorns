void compute(double values[], int num_points, double ders[]){

	for(int i = 0; i < num_points; ++i)
	{
		double a = values[i* 4 + 0 ];
		double b = values[i* 4 + 1 ];
		double c = values[i* 4 + 2 ];
		double d = values[i* 4 + 3 ];
		ders[i*4+0]= ((1 + (1 / ((a * d) - (b * c)))) * ((((((((a * (1) + a * (1))) + ((b * (0) + b * (0))))) + ((c * (0) + c * (0))))) + ((d * (0) + d * (0))))) + ((((a * a) + (b * b)) + (c * c)) + (d * d)) * (((0) + ((((a * d) - (b * c)) * 0 - 1 * (((d * (1) + a * (0))) - ((c * (0) + b * (0)))))/ (((a * d) - (b * c)) * ((a * d) - (b * c))))))); // df/(a) 
		ders[i*4+1]= ((1 + (1 / ((a * d) - (b * c)))) * ((((((((a * (0) + a * (0))) + ((b * (1) + b * (1))))) + ((c * (0) + c * (0))))) + ((d * (0) + d * (0))))) + ((((a * a) + (b * b)) + (c * c)) + (d * d)) * (((0) + ((((a * d) - (b * c)) * 0 - 1 * (((d * (0) + a * (0))) - ((c * (1) + b * (0)))))/ (((a * d) - (b * c)) * ((a * d) - (b * c))))))); // df/(b) 
		ders[i*4+2]= ((1 + (1 / ((a * d) - (b * c)))) * ((((((((a * (0) + a * (0))) + ((b * (0) + b * (0))))) + ((c * (1) + c * (1))))) + ((d * (0) + d * (0))))) + ((((a * a) + (b * b)) + (c * c)) + (d * d)) * (((0) + ((((a * d) - (b * c)) * 0 - 1 * (((d * (0) + a * (0))) - ((c * (0) + b * (1)))))/ (((a * d) - (b * c)) * ((a * d) - (b * c))))))); // df/(c) 
		ders[i*4+3]= ((1 + (1 / ((a * d) - (b * c)))) * ((((((((a * (0) + a * (0))) + ((b * (0) + b * (0))))) + ((c * (0) + c * (0))))) + ((d * (1) + d * (1))))) + ((((a * a) + (b * b)) + (c * c)) + (d * d)) * (((0) + ((((a * d) - (b * c)) * 0 - 1 * (((d * (0) + a * (1))) - ((c * (0) + b * (0)))))/ (((a * d) - (b * c)) * ((a * d) - (b * c))))))); // df/(d) 
	}
}
