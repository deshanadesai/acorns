void cross_entropy(const double **a, const double **b, double *loss){
    for(int i=0; i<2; i++){
        for(int j=0; j<2; j++ ){
            *loss = *loss - (b[i][j] * log(a[i][j] + 0.00001));
        }
    }
}