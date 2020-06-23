double cross_entropy(const double **a, const double **b){
double loss = 0;
loss = (loss) - ((b[0][0]) * (log((a[0][0]) + (0.00001))));
loss = (loss) - ((b[0][1]) * (log((a[0][1]) + (0.00001))));
loss = (loss) - ((b[1][0]) * (log((a[1][0]) + (0.00001))));
loss = (loss) - ((b[1][1]) * (log((a[1][1]) + (0.00001))));
return loss;
}