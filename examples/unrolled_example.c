<<<<<<< HEAD
double cross_entropy(const double **a, const double **b){
=======
void cross_entropy(const double **a, const double **b){
>>>>>>> 785d05db8c2928f0b0c02b32265d28937e8c80ad
	double loss = 0;
    for(int i=0; i<2; i++){
        for(int j=0; j<2; j++ ){
        	for(int k=0;k<1;k++){
            loss = loss - (b[i][j] * log(a[i][j] + 0.00001));
        }
        }
    }
    return loss;
}