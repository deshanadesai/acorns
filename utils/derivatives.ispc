export void compute(uniform double values[], uniform int num_points, uniform double ders[]){

	foreach (i = 0 ... num_points)
	{
		double k = values[i* 1 + 0 ];
		ders[i*1+0] = ((((((k + (((k * k) * k) * k)) * (((((k * (1) + k * (1))) + ((k * (0) + 3 * (1))))) - ((4 * 1 - k * 0)/ (4 * 4))) - (((k * k) + (3 * k)) - (k / 4)) * ((1) + ((k * ((k * ((k * (1) + k * (1))) + (k * k) * (1))) + ((k * k) * k) * (1)))))/ ((k + (((k * k) * k) * k)) * (k + (((k * k) * k) * k)))) + ((k * ((k * ((k * ((k * (1) + k * (1))) + (k * k) * (1))) + ((k * k) * k) * (1))) + (((k * k) * k) * k) * (1))))) + ((((2 * k) + 1) * (((k - 3) * (((1) - (0))) + (k - 3) * (((1) - (0))))) + ((k - 3) * (k - 3)) * ((((k * (0) + 2 * (1))) + (0))))));
	}
}

