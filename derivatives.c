void compute(double **values, long num_points, double **ders){

	for(int i = 0; i < num_points; ++i)
	{
		double k = values[i][0];
		ders[i][0]= cos(k) * cos(k)*1 + sin(k) * -1*sin(k)*1 + (pow(k,(2-1)) * (2 * 1 + k * 0 * log(k)));
	}
}

