export void compute(uniform double values[][2], uniform double ders[][2]){

	uniform long num_points = ((int) (sizeof (values) / sizeof (values)[0]));

	foreach (index = 0 ... num_points)
	{
		double k = values[index][0];
		double l = values[index][1];
		ders[index][0]= cos(k) * cos(k)*1 + sin(k) * -1*sin(k)*1 + (pow(k,(2-1) * (2 * 1 + k * 0 * log(k))));
		ders[index][1]= cos(k) * cos(k)*0 + sin(k) * -1*sin(k)*0 + (pow(k,(2-1) * (2 * 0 + k * 0 * log(k))));
	}
}

