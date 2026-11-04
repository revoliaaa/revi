import sys; sys.path.insert(0,sys.argv[1])
from vload import load_txt
import pandas as pd,numpy as np
E=sys.argv[2]
pairs={'S1':'Skenario1.txt','S2':'Skenario2.txt','S3':'Skenario3.txt','S4USD6':'Skenario4USD6.txt','S4USD10':'Skenario4USD10.txt','S4USD15':'Skenario4USD15.txt','S4USD35':'Untitled.txt','BENEFIT':'benefit allocation.txt'}
rows=[]
for k,t in pairs.items():
    v=load_txt(f'{E}/{t}'); p=pd.read_pickle(f'{k}.pkl')
    common=[c for c in v.columns if c in p.columns]
    miss=[c for c in v.columns if c not in p.columns]
    tot=same=0; worst=[]
    for c in common:
        a=v[c].values; b=pd.to_numeric(p[c],errors='coerce').values
        ok=np.isclose(a,b,rtol=5e-6,atol=1e-9)|(np.isnan(a)&np.isnan(b))
        tot+=len(a); same+=ok.sum()
        if not ok.all():
            rel=np.nanmax(np.abs(a-b)/np.maximum(np.abs(a),1e-9))
            worst.append((rel,c))
    worst.sort(reverse=True)
    rows.append(dict(run=k,file=t,vars_export=len(v.columns),vars_matched=len(common),missing=len(miss),values=tot,identical_6sig=same,pct=100*same/tot,n_vars_with_diff=len(worst),worst=';'.join(f'{c}({r:.2e})' for r,c in worst[:4])))
    if miss: print(k,'missing in pysd:',miss[:5])
df=pd.DataFrame(rows); print(df.to_string()); df.to_csv('pysd_vs_vensim.csv',index=False)
