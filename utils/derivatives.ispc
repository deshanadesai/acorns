export void compute(uniform double values[], uniform int num_points, uniform double ders[]){

	foreach (i = 0 ... num_points)
	{
		ders[i*1+0] = 9*k*k*k*k*k*k*k*k+4*k*k*k+(66.0/7.0)*k*k+1;
