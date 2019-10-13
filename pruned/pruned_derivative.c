void compute(double values[], int num_points, double ders[])
{

    for (int i = 0; i < num_points; ++i)
    {
        double k = values[i * 1 + 0];
        ders[i * 1 + 0] = 9 * k * k * k * k * k * k * k * k + 4 * k * k * k + 10.428571428571429 * k * k; // df/(k)
    }
}
