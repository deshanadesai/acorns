void compute(const double values[][2], double ders[][2]){

	long num_points = ((int) (sizeof (values) / sizeof (values)[0]));

	for(int i = 0; i < num_points; ++i)
	{
		double k = values[i][0];
		double l = values[i][1];
		ders[i][0]= cos(k) * cos(k)*1 + sin(k) * -1*sin(k)*1 + (pow(k,(2-1) * (2 * 1 + k * 0 * log(k))));
		ders[i][1]= cos(k) * cos(k)*0 + sin(k) * -1*sin(k)*0 + (pow(k,(2-1) * (2 * 0 + k * 0 * log(k))));
	}
}

