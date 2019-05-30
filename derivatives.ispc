export void compute(uniform double values[], uniform int num_points, uniform double ders[]){

	foreach (i = 0 ... num_points)
	{
		double k = values[i];
		ders[i] = cos(k) * cos(k)*1 + sin(k) * -1*sin(k)*1 + (pow(k,(2-1)) * (2 * 1 + k * 0 * log(k)));
	}
}

