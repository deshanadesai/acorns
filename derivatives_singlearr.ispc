export void compute(uniform double values[], uniform int num_points, uniform double ders[]){
	 double x = 0;

	 for(int i=0;i<num_points;i++){
	     double k = values[i];
	     print("k = %\n",k);	 
	 }
	 foreach (i = 0 ... num_points)
	 {
	 	 print("i = %\n",i);
	     double k = values[i];
	     print("k = %\n",k);
	     ders[i]= cos(k) * cos(k)*1 + sin(k) * -1*sin(k)*1 + (pow(k,(2-1)) * (2 * 1 + k * 0 * log(k)));
	     x = cos(k) * cos(k)*1 + sin(k) * -1*sin(k)*1 + (pow(k,(2-1)) * (2 * 1 + k * 0 * log(k)));
	     print("%\n",x);
	     print("=======\n");
	 }

}

