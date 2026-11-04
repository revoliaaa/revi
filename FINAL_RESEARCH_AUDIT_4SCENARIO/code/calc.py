import pandas as pd,numpy as np
W='/tmp/claude-0/-home-user-revi/2fafe0e9-8133-579b-9506-9462c793243c/scratchpad/work/'
DT=0.0625
SC=['S1','S2','S3','S4USD3','S4USD6','S4USD10','S4USD15','S4USD20','S4USD35']
_c={}
def F(k):
    if k not in _c: _c[k]=pd.read_pickle(W+k+'_full.pkl')
    return _c[k]
def I(k,col,a,b):
    df=F(k); s=df.loc[(df.index>=a-1e-9)&(df.index<b-1e-9),col]
    return float(s.sum()*DT)
def V(k,col,t): return float(F(k).loc[float(t),col])
def Mann(k,col,a=2030,b=2055): df=F(k); return float(df.loc[[float(y) for y in range(a,b+1)],col].mean())
def Mint(k,col,a=2030,b=2055): return I(k,col,a,b+1)/(b+1-a)
