<<<<<<< HEAD
double cross_entropy(const double **a, const double **b){
=======
void cross_entropy(const double **a, const double **b){
>>>>>>> 785d05db8c2928f0b0c02b32265d28937e8c80ad
double loss = 0;
loss = (loss) - ((b[0][0]) * (log((a[0][0]) + (0.00001))));
loss = (loss) - ((b[0][1]) * (log((a[0][1]) + (0.00001))));
loss = (loss) - ((b[1][0]) * (log((a[1][0]) + (0.00001))));
loss = (loss) - ((b[1][1]) * (log((a[1][1]) + (0.00001))));
<<<<<<< HEAD
return loss;
=======
>>>>>>> 785d05db8c2928f0b0c02b32265d28937e8c80ad

}