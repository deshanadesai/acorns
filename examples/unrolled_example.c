double cross_entropy(const double **a, const double **b){
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