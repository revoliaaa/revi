import pandas as pd,numpy as np,re
def load_txt(path):
    rows={}
    for line in open(path,encoding='latin-1'):
        p=line.rstrip('\n').rstrip('\r').split('\t')
        if p[0].startswith('Time'): continue
        name=p[0].rsplit(' : ',1)[0].strip()
        vals=[]
        for x in p[1:65]:
            x=x.strip()
            try: vals.append(float(x))
            except: vals.append(np.nan)
        rows[name]=vals
    return pd.DataFrame(rows,index=range(2024,2088))
