#ifndef ADDEBUG_INCLUDED
#define ADDEBUG_INCLUDED

void adDebugTgt_init(double epsilon, double seed, int tested_process) ;
void adDebugTgt_call(char *unitname, int traced, int forcetraced) ;
void adDebugTgt_exit() ;
int adDebugTgt_here(char* placename, int forcetraced) ;

void adDebugTgt_initReal4(char* varname, float *indep, float *indepd) ;
void adDebugTgt_initReal8(char* varname, double *indep, double *indepd) ;
void adDebugTgt_initReal4Array(char* varname, float *indep, float *indepd, int length) ;
void adDebugTgt_initReal8Array(char* varname, double *indep, double *indepd, int length) ;
void adDebugTgt_concludeReal4(char *varname, float dep, float depd) ;
void adDebugTgt_concludeReal8(char *varname, double dep, double depd) ;
void adDebugTgt_concludeReal4Array(char *varname, float *tvar, float *tvard, int length) ;
void adDebugTgt_concludeReal8Array(char *varname, double *tvar, double *tvard, int length) ;
void adDebugTgt_conclude() ;
void adDebugTgt_passiveReal4(char *varname, float var) ;
void adDebugTgt_passiveReal8(char *varname, double var) ;
void adDebugTgt_passiveReal4Array(char *varname, float *var, int length) ;
void adDebugTgt_passiveReal8Array(char *varname, double *var, int length) ;
void adDebugTgt_testReal4(char *varname, float var, float vard) ;
void adDebugTgt_testReal8(char *varname, double var, double vard) ;
void adDebugTgt_testReal4Array(char *varname, float *var, float *vard, int length) ;
void adDebugTgt_testReal8Array(char *varname, double *var, double *vard, int length) ;
void adDebugTgt_display(char *placename) ;

void adDebugBwd_init(double errmax, double seed) ;
void adDebugBwd_call(char *funcname, int deltadepth) ;
void adDebugBwd_exit() ;
int adDebugBwd_here(char* placename) ;

void adDebugFwd_init(double errmax, double seed) ;
void adDebugFwd_call(char *funcname) ;
void adDebugFwd_exit() ;
int adDebugFwd_here(char* placename) ;

void adDebugAdj_rwReal4(float *vard) ;
void adDebugAdj_rwReal8(double *vard) ;
void adDebugAdj_rReal4(float *vard) ;
void adDebugAdj_rReal8(double *vard) ;
void adDebugAdj_wReal4(float *vard) ;
void adDebugAdj_wReal8(double *vard) ;
void adDebugAdj_rwReal4Array(float *vard, int length) ;
void adDebugAdj_rwReal8Array(double *vard, int length) ;
void adDebugAdj_rReal4Array(float *vard, int length) ;
void adDebugAdj_rReal8Array(double *vard, int length) ;
void adDebugAdj_wReal4Array(float *vard, int length) ;
void adDebugAdj_wReal8Array(double *vard, int length) ;
void adDebugAdj_rwDisplay(char *placename, int indent) ;
void adDebugAdj_rDisplay(char *placename, int indent) ;
void adDebugAdj_wDisplay(char *placename, int indent) ;
void adDebugAdj_skip(char *placename) ;
void adDebugAdj_conclude() ;

#endif
